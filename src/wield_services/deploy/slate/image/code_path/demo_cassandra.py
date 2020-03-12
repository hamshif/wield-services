#!/usr/bin/env python
"""
Author: Gideon Bar
"""
import json
import os
import traceback

from time import sleep

import logging
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, BatchStatement
from cassandra.policies import RoundRobinPolicy
from cassandra.query import SimpleStatement
from pyhocon import ConfigFactory

import rx
from rx import operators as ops
import concurrent.futures


class BaseTable:

    def __init__(self, host, keyspace, table_name, with_logger=True, with_session=True):

        self.host = host
        self.keyspace = keyspace
        self.table_name = table_name
        self.cql_create_table = None
        self.batch = None
        self.upsert_cql_cmd = None
        self.prepared_upsert_cql_cmd = None
        self.upsert_count = 0

        if with_logger:
            self.set_logger()
        else:
            self.log = None

        if with_session:
            self.create_session()
        else:
            self.cluster = None
            self.session = None

    def __del__(self):
        self.cluster.shutdown()

    def create_session(self):
        self.cluster = Cluster(
            [self.host],
            # load_balancing_policy=RoundRobinPolicy(),
            # protocol_version=65
        )
        self.session = self.cluster.connect(None)

        # self.log.info(f"creating keyspace: {self.keyspace}")
        self.session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
                WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '2' }}
                """)

        # self.log.info(f"keyspace: {self.keyspace} verified")
        self.session.set_keyspace(self.keyspace)

    def get_session(self):
        return self.session

    # How about Adding some log info to see what went wrong
    def set_logger(self):
        log = logging.getLogger()
        log.setLevel('INFO')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        log.addHandler(handler)
        self.log = log

    def list_keyspaces(self):

        rows = self.session.execute(f"SELECT keyspace_name FROM system_schema.keyspaces")

        [print(row) for row in rows]

    def select_data(self, limit=50, pr=False):
        rows = self.session.execute(f'select * from {self.table_name} limit {limit};')

        if pr:
            [print(row) for row in rows]

        return rows

    def select_all(self, pr=False, where_args=None):

        if where_args is None:
            where_clause = ''

        rows = self.session.execute(f'select * from {self.table_name};')

        if pr:
            [print(row) for row in rows]

        return rows

    def del_keyspace(self, keyspace=None):

        if keyspace is None:
            keyspace = self.keyspace

        if self.cluster is not None:
            self.cluster.shutdown()
        self.cluster = Cluster([self.host])
        self.session = self.cluster.connect(None)

        rows = self.session.execute(f"SELECT keyspace_name FROM system_schema.keyspaces", timeout=20)
        if keyspace in [row[0] for row in rows]:
            self.log.info(f"dropping existing keyspace: {keyspace}")
            self.session.execute(f"DROP KEYSPACE {keyspace}")
        else:
            self.log.info(f"could'nt find keyspace: {keyspace}")

    def list_tables(self, keyspace=None):

        if keyspace is None:
            keyspace = self.keyspace

        self.cluster = Cluster([self.host])
        self.session = self.cluster.connect(None)

        tables = self.cluster.metadata.keyspaces['grids']
        # cmd = f"DESCRIBE KEYSPACES;"
        #
        # print(cmd)
        #
        # tables = self.session.execute(cmd)
        #

        print(f"meta data:\n{tables.__dict__}")

        for table in tables.__dict__['tables']:
            print(table)

            column = tables.__dict__['tables'][table].__dict__['columns'].items()

            [print(f'column: {i}   {i[1]}') for i in column]

    def del_table(self):

        res = self.session.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        print(res)

    def create_table(self):

        self.log.info(f"Creating table {self.table_name} with this statement:\n{self.cql_create_table}")
        self.session.execute(self.cql_create_table)
        self.log.info(f"{self.table_name} Table verified !!!")

    def maybe_upsert_batch(self, upsert):

        # print(f"klook  {upsert}")
        self.batch.add(self.prepared_upsert_cql_cmd, upsert)
        self.upsert_count += 1

        if self.upsert_count > 50:
            self.upsert_count = 0
            self.session.execute(self.batch)
            self.batch.clear()
            self.log.info(f'Intermediate Batch Insert Completed {self.table_name}')


class ProteinTable(BaseTable):

    def __init__(self, host, keyspace, table_name):

        super().__init__(host, keyspace, table_name)

        self.cql_create_table = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            chunk_index int,
            amino_acid_index int,
            atom_index int,
            atom text,
            PRIMARY KEY (chunk_index, amino_acid_index, atom_index)
        )
        """

        self.upsert_cql_cmd = f"INSERT INTO  {self.table_name} (chunk_index, amino_acid_index, atom_index, atom) VALUES (?,?,?,?)"

        self.batch = None

    def insert_data(self, data=None):

        self.prepared_upsert_cql_cmd = self.session.prepare(self.upsert_cql_cmd)

        print(f"insert_cql_cmd:\n{self.upsert_cql_cmd}")

        self.batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        if data is None:

            for i in range(1, 20, 1):

                upsert = (i, 8, 27, "ATOM     66  C   GLY A   6       0.160   0.603  -2.018  1.00 22.22   \n")
                self.batch.add(self.upsert_cql_cmd, upsert)
        else:

            for k1, v1 in data.items():

                for k2, v2 in v1.items():

                    for k3, v3 in v2.items():

                        upsert = (int(k1), int(k2), int(k3), v3)

                        self.maybe_upsert_batch(upsert)

        self.session.execute(self.batch)

    def everything(self, pr=True):

        protein = {}

        rows = self.select_all(pr=False)

        count = 0

        first_row = rows[0]

        for row in rows:

            if row.chunk_index not in protein:

                protein[row.chunk_index] = {}

            if row.amino_acid_index not in protein[row.chunk_index]:

                protein[row.chunk_index][row.amino_acid_index] = {}

            if row.atom_index not in protein[row.chunk_index][row.amino_acid_index]:

                protein[row.chunk_index][row.amino_acid_index][row.atom_index] = {}

            protein[row.chunk_index][row.amino_acid_index][row.atom_index] = row.atom

            if pr and count < 10:

                print(
                    f"{self.table_name}: {row.chunk_index}: {row.amino_acid_index}: {row.atom_index}:     "
                    f"{protein[row.chunk_index][row.amino_acid_index][row.atom_index]}"
                )

                count += 1

        print(
            f"\n{self.table_name} Received {len(protein[row.chunk_index])} protein chunks. "
            f"{len(protein[first_row.chunk_index][first_row.amino_acid_index])} Atoms per chunk"
        )

        return protein


class PointGrid(BaseTable):
    """
    PointGrid is a generalised Cassandra table structure for 3D spatial data.
    Supports 3 depths of nested dictionaries:

     depth 1 example:
        "25,17,11": 90,

     depth 2 example:
        "2,26,19": {
            "CA": -0.366544987779325,

     depth 3 example:
        "10,15,2": {
            "ENERGY": {
                "O": 0.149137080210051,

     Supports these permutations:

          point not primary key example
           "-0.101104097941006": "5,21,9",

          value list:
              "2,27,9": [
                    -1.57804254779772,
                    -2.62220264769739
                ],

    """

    def __init__(self, host, table_name, depth=1, point_primary_key=True, value_list=False):
        """
        hocon config example:

        spatial_grids: [

            # grid name, grid depth, point is key, value is list

              [bugs_bunny, 1, true, false]
              [elmore_fud, 1, true, true]
              [duffy_duck, 2, true, false]
              [road_runner, 3, true, false]
        ]

        :param host: the url of Cassandra for connection
        :type host: str
        :param table_name:
        :type table_name: str
        :param depth: the amount of:
            [nested keys to value / dicts to flatten when upserting / dicts to nest when deserialising]
        :type depth: int
        :param point_primary_key: are the point values combined part of the primary key
        :type point_primary_key: bool
        :param value_list: is value a list of doubles defaults to false and double
        :type value_list: bool
        """

        if depth > 3 or depth < 1:
            raise ValueError(f'Supports 3 depth values of nested dictionaries 1, 2, 3 you entered {depth}')

        super().__init__(host, 'grids', table_name)
        self.upsert_count = 0
        self.depth = depth
        self.point_primary_key = point_primary_key
        self.value_list = value_list

        # TODO ponder creating statement variables in separate objects
        #  this is a mess too many permutations
        if self.depth == 1:

            self.upsert_cql_cmd1 = f"INSERT INTO  {self.table_name} (x, y, z, point_value) VALUES (?,?,?,?)"

            if self.point_primary_key:

                if self.value_list:
                    self.cql_create_table = f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        x int,
                        y int,
                        z int,
                        point_value list<double>,
                        PRIMARY KEY (x, y, z)
                    )
                    """
                else:
                    self.cql_create_table = f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        x int,
                        y int,
                        z int,
                        point_value double,
                        PRIMARY KEY (x, y, z)
                    )
                    """

            else:

                self.cql_create_table = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    x int,
                    y int,
                    z int,
                    point_value text,
                    PRIMARY KEY (point_value)
                )
                """

        elif self.depth == 2:

            self.upsert_cql_cmd1 = f"INSERT INTO  {self.table_name} (x, y, z, point_name , point_value) VALUES (?,?,?,?,?)"

            self.cql_create_table = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                x int,
                y int,
                z int,
                point_name text,
                point_value double,
                PRIMARY KEY (x, y, z, point_name)
            )
            """

        elif self.depth == 3:

            self.upsert_cql_cmd1 = f"INSERT INTO  {self.table_name} (x, y, z, point_type, point_name , point_value) VALUES (?,?,?,?,?,?)"

            self.cql_create_table = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                x int,
                y int,
                z int,
                point_type text,
                point_name text,
                point_value double,
                PRIMARY KEY (x, y, z, point_type, point_name)
            )
            """

        # lets do some batch insert
    def insert_data(self, data=None):

        self.prepared_upsert_cql_cmd = self.session.prepare(self.upsert_cql_cmd1)

        print(f"insert_cql_cmd:\n{self.prepared_upsert_cql_cmd}")

        self.batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        if data is None:

            for i in range(-5, 20, 1):

                if self.depth == 1:

                    upsert = (i, 8, 27, 0)
                    self.batch.add(self.prepared_upsert_cql_cmd, upsert)

                elif self.depth == 2:

                    for key_tup in ['Grandma', 'BugsBunny', 'ElmoreFud', 'Kishkashta']:

                        upsert = (i, 8, 27, key_tup, 0)
                        self.batch.add(self.prepared_upsert_cql_cmd, upsert)

                elif self.depth == 3:

                    for key_tup in [('toon', 'Grandma'), ('superHero', 'BugsBunny'), ('Human', 'ElmoreFud'), ('Human', 'Kishkashta')]:

                        upsert = (i, 8, 27, key_tup[0], key_tup[1], 0)
                        self.batch.add(self.prepared_upsert_cql_cmd, upsert)

        else:

            for k, v in data.items():

                if self.point_primary_key:
                    x, y, z = k.split(',')
                else:
                    x, y, z = v.split(',')

                if self.depth == 1:

                    if self.point_primary_key:

                        upsert = None

                        if self.value_list:

                            upsert = (int(x), int(y), int(z), v)

                        else:

                            upsert = (int(x), int(y), int(z), int(v))

                        # print(f"upsert tuple: {upsert}")
                        self.maybe_upsert_batch(upsert)

                    else:

                        upsert = (int(x), int(y), int(z), k)
                        self.maybe_upsert_batch(upsert)

                    continue

                elif self.depth == 2 or self.depth == 3:

                    for k1, v1 in v.items():

                        if self.depth == 2:

                            # print(f"x: {x}, y: {y}, z: {z}, point_name: {k1}, point_value: {v1}")
                            upsert = (int(x), int(y), int(z), k1, int(v1))

                            self.maybe_upsert_batch(upsert)

                            continue

                        elif self.depth == 3:

                            if isinstance(v1, str):
                                upsert = (int(x), int(y), int(z), k1, v1, None)
                                self.maybe_upsert_batch(upsert)
                            else:
                                for k2, v2 in v1.items():
                                    # print(f"x: {x}, y: {y}, z: {z}, point_type: {k1}, point_name: {k2}, point_value: {v2}")

                                    upsert = (int(x), int(y), int(z), k1, k2, int(v2))

                                    self.maybe_upsert_batch(upsert)

                                    continue

        self.session.execute(self.batch)
        # self.log.info('Batch Insert Completed')

    # def deserialize_row(self):

    def everything(self, pr=True):

        rows = self.select_all(pr=False)

        point_grid = {}

        count = 0

        for row in rows:

            # print(f"{row}")

            point = f"{str(row.x)},{str(row.y)},{str(row.x)}"

            if self.depth > 1:

                if point not in point_grid.keys():
                    point_grid[point] = {}

                if self.depth == 2:

                    point_grid[point][row.point_name] = row.point_value

                elif self.depth == 3:

                    if row.point_type not in point_grid[point].keys():
                        point_grid[point][row.point_type] = {}

                    point_grid[point][row.point_type][row.point_name] = row.point_value

            else:
                point_grid[point] = row.point_value

            if pr and count < 10:

                print(f"{point}:   {point_grid[point]}")

                count += 1

        print(f"{self.table_name} has {len(point_grid)} points")

        return point_grid


def everything_point(conf, table_name, depth, point_primary_key, value_list):

    grid = PointGrid(
        host=conf.host,
        table_name=table_name,
        depth=depth,
        point_primary_key=point_primary_key,
        value_list=value_list
    )

    point_grid = grid.everything()

    return point_grid


def list_tables(conf, table_name):

    grid = PointGrid(conf.host, table_name)

    grid.list_tables()


def reset(conf, table_name):

    grid = PointGrid(
        host=conf.host,
        table_name=table_name
    )

    grid.list_keyspaces()

    grid.del_keyspace()
    grid.list_keyspaces()

    grid = PointGrid(conf.host, table_name)

    # grid.create_table()
    # everything(conf, table_name)


def get_file_names():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")

    grid_names = []
    for (dirpath, dirnames, filenames) in os.walk(f'{dir_path}/COMPACT'):

        grid_names.extend(filenames)
        break

    # print(grid_names)

    return grid_names


def create_point_table(conf, table_name, depth, point_primary_key, value_list):

    grid = PointGrid(
        host=conf.host,
        table_name=table_name,
        depth=depth,
        point_primary_key=point_primary_key,
        value_list=value_list
    )

    grid.create_table()

    # grid.everything()

    return f"created:  {table_name}"


def populate_point_table(conf, full_path, table_name, depth, point_primary_key, value_list):

    print(f"table name: {table_name} depth: {depth} full path: {full_path}")

    with open(full_path) as json_file:

        try:
            data = json.load(json_file)

            grid = PointGrid(
                host=conf.host,
                table_name=table_name,
                depth=depth,
                point_primary_key=point_primary_key,
                value_list=value_list
            )
            #
            # grid.list_keyspaces()
            #
            # grid.del_keyspace()
            # grid.list_keyspaces()

            # grid.create_table()
            grid.insert_data(data)
            # rows = grid.select_data1(pr=True)

        except Exception as e:
            print(f"Error occurred while trying to run bash command: {e}")

            return f'failed {table_name}'

        return f'populated {table_name}'


def populate_point_tables_from_files(conf):

    grid_tuples = []
    table_tuples = get_table_tuples_from_conf(conf)

    # TODO find out how to use rx to combine and group by

    for (dirpath, dirnames, filenames) in os.walk(f'{conf.dir_path}/COMPACT'):

        for file_name in filenames:

            full_name = f'{dirpath}/{file_name}'
            g = file_name.replace('.json', '')
            # print(full_name)

            for t in table_tuples:

                if t[0] == g:
                    grid_tuple = (g, t[1], full_name, t[2], t[3])

                    grid_tuples.append(grid_tuple)
                    break

    [print(f'grid_tuple: {grid_tuple}') for grid_tuple in grid_tuples]

    source_files = rx.from_(grid_tuples)

    max_threads = 5

    with concurrent.futures.ProcessPoolExecutor(max_threads) as executor:

        obs_files = source_files.pipe(

            # ops.concat(source_tuples),
            # ops.reduce(lambda acc, y: acc.append[y]),

            # ops.group_by(lambda x: x[0]),
            # ops.map(lambda grp: type(grp)),

            # ops.
            # ops.reduce(lambda acc, b: acc.append(b)),

            # ops.zip(source_files, source_tuples),
            # ops.filter(lambda grid_tuple: '.json' in grid_tuple),
            # ops.map(lambda file_name: file_name.replace('.json', '')),
            ops.flat_map(
                lambda grid_tup: executor.submit(
                    populate_point_table,
                    conf,
                    grid_tup[2],
                    grid_tup[0],
                    grid_tup[1],
                    grid_tup[3],
                    grid_tup[4],
                )
            )
        )

        # composed.subscribe(create_table)
        obs_files.subscribe(lambda value: print(f"Received {value}"))


def get_table_tuples_from_conf(conf):

    cassandra_conf = ConfigFactory.parse_file('./Grids.conf')

    grid_type_tups = []

    [grid_type_tups.append((grid[0], grid[1], grid[2], grid[3])) for grid in cassandra_conf.spatial_grids]

    return grid_type_tups


def create_point_tables(conf):

    grid_type_tuples = get_table_tuples_from_conf(conf)

    source = rx.from_(grid_type_tuples)

    max_threads = 5

    with concurrent.futures.ProcessPoolExecutor(max_threads) as executor:
        composed = source.pipe(
            ops.flat_map(lambda gt: executor.submit(create_point_table, conf, gt[0], gt[1], gt[2], gt[3]))
            # ops.map(lambda grid_tuple: grid_tuple)
        )
        # composed.subscribe(create_table)
        composed.subscribe(lambda value: print(f"Received {value}"))


def check_grids(conf):

    grid_type_tuples = get_table_tuples_from_conf(conf)

    snooze = 5

    for grid_tuple in grid_type_tuples:

        print(f"snoozing for {snooze} before checking {grid_tuple[0]} table")
        sleep(snooze)
        everything_point(conf, grid_tuple[0], grid_tuple[1], grid_tuple[2], grid_tuple[3])


def global_test(conf):

    snooze = 3

    print("Deleting grids keyspace and all tables ...")
    reset(conf, "table_name")

    print(f"short sleep or {snooze} and listing tables ...")
    sleep(snooze)
    list_tables(conf, "table_name")

    print(f"short sleep or {snooze} then creating tables and listing them ...")
    sleep(snooze)
    create_point_tables(conf)
    list_tables(conf, "HOTSPOTGRID")

    print(f"short sleep or {snooze} then populating tables ...")
    sleep(snooze)
    populate_point_tables_from_files(conf)

    print(f"short sleep or {snooze} then checking tables content ...")
    sleep(snooze)
    check_grids(_conf)


def check_protein_table(conf, table_name):

    protein_table = ProteinTable(
        host=conf.host,
        keyspace='grids',
        table_name=table_name
    )

    protein = protein_table.everything()

    return f"created:  {table_name}"


def test_proteins(conf):

    snooze = 5

    print("Deleting grids keyspace and all tables ...")
    reset(conf, "table_name")

    print(f"short sleep or {snooze} and listing tables ...")
    sleep(snooze)
    list_tables(conf, "table_name")

    print(f"short sleep or {snooze} then creating tables and listing them ...")
    sleep(snooze)
    all_protein_tables(conf, create_protein_table)
    list_tables(conf, "table_name")

    print(f"short sleep or {snooze} then populating tables ...")
    sleep(snooze)
    all_protein_tables(conf, populate_protein_table)

    print(f"short sleep or {snooze} then checking tables content ...")
    sleep(snooze)
    all_protein_tables(conf, check_protein_table)


def del_table(table_name, conf, depth, point_primary_key=True):

    # print(table_name)
    grid = PointGrid(
        conf.host,
        table_name,
        depth=depth,
        point_primary_key=point_primary_key
    )

    grid.del_table()


def create_protein_table(conf, protein_name):

    protein_table = ProteinTable(
        host=conf.host,
        keyspace='grids',
        table_name=protein_name
    )

    protein_table.create_table()

    return f"created:  {protein_name}"


def populate_protein_table(conf, table_name):

    full_path = f"{conf.dir_path}/COMPACT/{table_name}.json"

    print(f"table name: {table_name} full path: {full_path}")

    with open(full_path) as json_file:

        try:
            data = json.load(json_file)

            table = ProteinTable(
                host=conf.host,
                keyspace='grids',
                table_name=table_name,
            )

            table.insert_data(data)

        except Exception as e:
            print(f"Error occurred while trying to run bash command: {e}")

            return f'failed {table_name}'

        return f'populated {table_name}'


def all_protein_tables(conf, f_protein):

    cassandra_conf = ConfigFactory.parse_file('./Grids.conf')

    source = rx.from_(cassandra_conf.proteins)

    max_threads = 5

    with concurrent.futures.ProcessPoolExecutor(max_threads) as executor:
        composed = source.pipe(
            ops.flat_map(lambda protein_name: executor.submit(f_protein, conf, protein_name))
            # ops.map(lambda grid_tuple: grid_tuple)
        )
        # composed.subscribe(create_table)
        composed.subscribe(lambda value: print(f"Received {value}"))


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")

    _conf = ConfigFactory.parse_file('./Cassandra.conf')

    _conf.dir_path = dir_path

    global_test(_conf)

    # _table_name = 'PROBESTART'
    #
    # _depth = 1
    #
    # create_point_table(_table_name, _conf, depth=_depth, point_primary_key=False)
    # list_tables(_conf, _table_name)
    # del_table(_table_name, _conf, depth=_depth, point_primary_key=False)
    # list_tables(_conf, _table_name)
    #
    # populate_point_table(
    #     conf=_conf,
    #     full_path=_full_path,
    #     table_name=_table_name,
    #     depth=_depth,
    #     point_primary_key=False
    # )
    # everything_point(_conf, _table_name, _depth, True, False)
    #
    # tups = get_table_tuples_from_conf(_conf)
    #
    # check_grids(_conf)
    #
    # everything_point(_conf, _table_name, 2)

    # test_proteins(_conf)


#




