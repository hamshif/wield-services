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
            load_balancing_policy=RoundRobinPolicy(),
            protocol_version=3
        )
        self.session = self.cluster.connect(None)

        self.log.info(f"creating keyspace: {self.keyspace}")
        self.session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
                WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '2' }}
                """)

        self.log.info(f"setting keyspace: {self.keyspace}")
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

        rows = self.session.execute(f"SELECT keyspace_name FROM system_schema.keyspaces")
        if keyspace in [row[0] for row in rows]:
            self.log.info("dropping existing keyspace: {keyspace}")
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


class PointGrid(BaseTable):

    def __init__(self, host, table_name):
        super().__init__(host, 'grids', table_name)

    def create_table(self):
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
        self.session.execute(c_sql)
        self.log.info(f"{self.table_name} Table verified !!!")

    # lets do some batch insert
    def insert_data(self, data=None):
        insert_cql_cmd = self.session.prepare(f"INSERT INTO  {self.table_name} (x, y, z, point_name , point_value) VALUES (?,?,?,?,?)")

        print(f"insert_cql_cmd:\n{insert_cql_cmd}")

        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        if data is None:

            for i in range(-5, 20, 1):

                batch.add(insert_cql_cmd, (i, 8, 27, 'Grandma', 0))
                batch.add(insert_cql_cmd, (i, 8, 27, 'BugsBunney', 0))
                batch.add(insert_cql_cmd, (i, 8, 27, 'ElmoreFud', 0))
                batch.add(insert_cql_cmd, (i, 8, 27, 'Kishkashta', 0))

        else:

            print("fabulous")
            statement_count = 0

            for key, value in data.items():

                for k, v in value.items():

                    x, y, z = key.split(',')

                    # print(f"x: {x}, y: {y}, z: {z}, point_name: {k}, point_value: {v}")

                    batch.add(insert_cql_cmd, (int(x), int(y), int(z), k, int(v)))

                    statement_count += 1

                    if statement_count > 200:
                        statement_count = 0
                        self.session.execute(batch)
                        batch.clear()
                        self.log.info('Intermediate Batch Insert Completed')

        self.session.execute(batch)
        # self.log.info('Batch Insert Completed')

    def everything(self, pr=True):

        rows = self.select_data1(pr=False)

        point_grid = {}

        count = 0

        for row in rows:

            point = f"{str(row.x)},{str(row.y)},{str(row.x)}"

            if point not in point_grid.keys():
                point_grid[point] = {}

            point_grid[point][row.point_name] = row.point_value

        if pr:
            for point in point_grid.items():

                print(point)

                count += 1

                if count > 100:
                    break

        print(f"{self.table_name} has {len(point_grid)} points")

        return point_grid


def poc(conf):

    grid = PointGrid(conf.host)

    grid.list_keyspaces()

    grid.del_keyspace()
    grid.list_keyspaces()

    # grid.create_table()
    # grid.insert_data()
    # rows = grid.select_data(pr=True)
    #
    # print(rows)


def demo(conf, table_name):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")

    origin_name = f'{dir_path}/{table_name}'

    a = f'{origin_name}.json'

    with open(a) as json_file:
        data = json.load(json_file)

        grid = PointGrid(conf.host, table_name)
        #
        grid.list_keyspaces()
        #
        # grid.del_keyspace()
        # grid.list_keyspaces()

        grid.create_table()
        grid.insert_data(data)
        rows = grid.select_data1(pr=True)


def everything(conf, table_name='electric'):

    grid = PointGrid(conf.host, table_name)

    point_grid = grid.everything()

    return point_grid


def list_tables(conf):

    grid = PointGrid(conf.host)

    grid.list_tables()


def reset(conf, table_name):

    grid = PointGrid(conf.host, table_name)

    grid.list_keyspaces()

    grid.del_keyspace()
    grid.list_keyspaces()

    grid = PointGrid(conf.host, table_name)

    grid.create_table()
    # everything(conf, table_name)


if __name__ == '__main__':

    _conf = ConfigFactory.parse_file('./Cassandra.conf')

    _table_name = 'HOTSPOTGRID'

    # demo(_conf, _table_name)
    # poc(_conf)

    everything(_conf, _table_name)

    # list_tables(_conf)

    # reset(_conf, _table_name)





