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

    def select_data1(self, pr=False, where_args=None):

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
    """

    def __init__(self, host, table_name, depth=1, point_primary_key=True):

        if depth > 3 or depth < 1:
            raise ValueError(f'Supports 3 depth values of nested dictionaries 1, 2, 3 you entered {depth}')

        super().__init__(host, 'grids', table_name)
        self.upsert_count = 0
        self.depth = depth
        self.point_primary_key = point_primary_key

    def create_table(self):

        c_sql = 'mistake'

        if self.depth == 1:

            if self.point_primary_key:

                c_sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    x int,
                    y int,
                    z int,
                    point_value double,
                    PRIMARY KEY (x, y, z)
                )
                """

            else:

                c_sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    x int,
                    y int,
                    z int,
                    point_value text,
                    PRIMARY KEY (point_value)
                )
                """

        elif self.depth == 2:

            c_sql = f"""
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

            c_sql = f"""
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

        self.session.execute(c_sql)
        self.log.info(f"{self.table_name} Table verified !!!")

    def maybe_upsert_batch(self, upsert):

        self.batch.add(self.upsert_cql_cmd, upsert)
        self.upsert_count += 1

        if self.upsert_count > 100:
            self.upsert_count = 0
            self.session.execute(self.batch)
            self.batch.clear()
            self.log.info(f'Intermediate Batch Insert Completed {self.table_name}')

        # lets do some batch insert
    def insert_data(self, data=None):

        if self.depth == 1:

            self.upsert_cql_cmd = self.session.prepare(
                f"INSERT INTO  {self.table_name} (x, y, z, point_value) VALUES (?,?,?,?)"
            )
        elif self.depth == 2:
            self.upsert_cql_cmd = self.session.prepare(
                f"INSERT INTO  {self.table_name} (x, y, z, point_name , point_value) VALUES (?,?,?,?,?)"
            )
        elif self.depth == 3:
            self.upsert_cql_cmd = self.session.prepare(
                f"INSERT INTO  {self.table_name} (x, y, z, point_type, point_name , point_value) VALUES (?,?,?,?,?,?)"
            )
        # else:
        #     ec

        print(f"insert_cql_cmd:\n{self.upsert_cql_cmd}")

        self.batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        if data is None:

            for i in range(-5, 20, 1):

                if self.depth == 1:

                    upsert = (i, 8, 27, 0)
                    self.batch.add(self.upsert_cql_cmd, upsert)

                elif self.depth == 2:

                    for key_tup in ['Grandma', 'BugsBunny', 'ElmoreFud', 'Kishkashta']:

                        upsert = (i, 8, 27, key_tup, 0)
                        self.batch.add(self.upsert_cql_cmd, upsert)

                elif self.depth == 3:

                    for key_tup in [('toon', 'Grandma'), ('superHero', 'BugsBunny'), ('Human', 'ElmoreFud'), ('Human', 'Kishkashta')]:

                        upsert = (i, 8, 27, key_tup[0], key_tup[1], 0)
                        self.batch.add(self.upsert_cql_cmd, upsert)

        else:

            for k, v in data.items():

                if self.point_primary_key:
                    x, y, z = k.split(',')
                else:
                    x, y, z = v.split(',')

                if self.depth == 1:

                    if self.point_primary_key:
                        upsert = (int(x), int(y), int(z), int(v))
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

        rows = self.select_data1(pr=False)

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

            if pr and count < 100:

                print(point_grid[point])

                count += 1

        print(f"{self.table_name} has {len(point_grid)} points")

        return point_grid


def everything(conf, table_name, depth, point_primary_key):

    grid = PointGrid(
        host=conf.host,
        table_name=table_name,
        depth=depth,
        point_primary_key=point_primary_key
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


def create_table(conf, table_name, depth, point_primary_key):

    grid = PointGrid(
        host=conf.host,
        table_name=table_name,
        depth=depth,
        point_primary_key=point_primary_key
    )

    grid.create_table()

    # grid.everything()

    return f"created:  {table_name}"


def create_tables_from_json_files(conf):

    file_names = get_file_names()

    source = rx.from_(file_names)

    # print(type(source))

    max_threads = 5

    with concurrent.futures.ProcessPoolExecutor(max_threads) as executor:

        composed = source.pipe(
            ops.filter(lambda file_name: '.json' in file_name),
            ops.map(lambda file_name: file_name.replace('.json', '')),
            ops.flat_map(lambda grid_name: executor.submit(create_table, grid_name, conf))
        )
        # composed.subscribe(create_table)
        composed.subscribe(lambda value: print(f"Received {value}"))


def populate_table(conf, full_path, table_name, depth, point_primary_key):

    print(f"table name: {table_name} depth: {depth} full path: {full_path}")

    with open(full_path) as json_file:

        try:
            data = json.load(json_file)

            grid = PointGrid(conf.host, table_name, depth=depth, point_primary_key=point_primary_key)
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


def populate_tables_from_files(conf):

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
                    grid_tuple = (g, t[1], full_name, t[2])

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
                    populate_table,
                    conf,
                    grid_tup[2],
                    grid_tup[0],
                    grid_tup[1],
                    grid_tup[3],
                )
            )
        )

        # composed.subscribe(create_table)
        obs_files.subscribe(lambda value: print(f"Received {value}"))


def get_table_tuples_from_conf(conf):

    grid_conf = ConfigFactory.parse_file('./Grids.conf')

    grid_type_tups = []

    [grid_type_tups.append((grid[0], grid[1], grid[2])) for grid in grid_conf.point_grids]

    return grid_type_tups


def create_tables(conf):

    grid_type_tuples = get_table_tuples_from_conf(conf)

    source = rx.from_(grid_type_tuples)

    max_threads = 5

    with concurrent.futures.ProcessPoolExecutor(max_threads) as executor:
        composed = source.pipe(
            ops.flat_map(lambda gt: executor.submit(create_table, conf, gt[0], gt[1], gt[2]))
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
        everything(conf, grid_tuple[0], grid_tuple[1], grid_tuple[2])


def global_test(conf):

    snooze = 3

    print("Deleting grids keyspace and all tables ...")
    reset(conf, "table_name")

    print(f"short sleep or {snooze} and listing tables ...")
    sleep(snooze)
    list_tables(conf, "table_name")

    print(f"short sleep or {snooze} then creating tables and listing them ...")
    sleep(snooze)
    create_tables(conf)
    list_tables(conf, "HOTSPOTGRID")

    print(f"short sleep or {snooze} then populating tables ...")
    sleep(snooze)
    populate_tables_from_files(conf)

    print(f"short sleep or {snooze} then checking tables content ...")
    sleep(snooze)
    check_grids(_conf)


def del_table(table_name, conf, depth, point_primary_key=True):

    # print(table_name)
    grid = PointGrid(
        conf.host,
        table_name,
        depth=depth,
        point_primary_key=point_primary_key
    )

    grid.del_table()


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")

    _conf = ConfigFactory.parse_file('./Cassandra.conf')

    _conf.dir_path = dir_path

    global_test(_conf)

    # create_tables_from_json_files(_conf)

    _table_name = 'POINTS'
    #
    # _full_path = f'{dir_path}/COMPACT/{_table_name}.json'
    #
    _depth = 3

    # create_table(_table_name, _conf, depth=_depth, point_primary_key=False)
    # list_tables(_conf, _table_name)
    # del_table(_table_name, _conf, depth=_depth, point_primary_key=False)
    # list_tables(_conf, _table_name)

    # populate_table(
    #     conf=_conf,
    #     full_path=_full_path,
    #     table_name=_table_name,
    #     depth=_depth,
    #     point_primary_key=False
    # )
    # everything(_conf, _table_name, _depth, True)

    # tups = get_table_tuples_from_conf(_conf)

    # check_grids(_conf)


    # poc(_conf)
    #
    # everything(_conf, _table_name, 2)

    # populate_tables_from_files(_conf)

    # reset(_conf, _table_name)

    # create_tables(_conf)
    # list_tables(_conf, _table_name)
#




