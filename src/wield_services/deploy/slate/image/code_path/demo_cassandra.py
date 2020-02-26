#!/usr/bin/env python
"""
Author: Gideon Bar
"""
import logging
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, BatchStatement
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
        self.cluster = Cluster([self.host])
        self.session = self.cluster.connect(None)

        self.log.info("creating keyspace...")
        self.session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
                WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '2' }}
                """)

        self.log.info("setting keyspace...")
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

    def del_keyspace(self, keyspace):

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


class PointGrid(BaseTable):

    def __init__(self, host, keyspace, table_name):
        super().__init__(host, keyspace, table_name)

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
    def insert_data(self):
        insert_sql = self.session.prepare(f"INSERT INTO  {self.table_name} (x, y, z, point_name , point_value) VALUES (?,?,?,?,?)")
        batch = BatchStatement()

        for i in range(-5, 20, 1):

            batch.add(insert_sql, (i, 8, 27, 'Grandma', 0))
            batch.add(insert_sql, (i, 8, 27, 'BugsBunney', 0))
            batch.add(insert_sql, (i, 8, 27, 'ElmoreFud', 0))
            batch.add(insert_sql, (i, 8, 27, 'Kishkashta', 0))

        self.session.execute(batch)
        self.log.info('Batch Insert Completed')


if __name__ == '__main__':

    _conf = ConfigFactory.parse_file('./Cassandra.conf')

    grid = PointGrid(_conf.host, 'grids', 'point_grid')

    grid.list_keyspaces()

    # grid.del_keyspace(grid.keyspace)
    # grid.list_keyspaces()

    grid.create_table()
    grid.insert_data()
    rows = grid.select_data(pr=True)


