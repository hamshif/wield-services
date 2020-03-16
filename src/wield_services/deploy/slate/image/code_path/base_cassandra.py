#!/usr/bin/env python
"""
Author: Gideon Bar
"""
import json
import os
import traceback
from enum import Enum

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

    def __init__(self, host, keyspace, table_name, with_logger=True, with_session=True, batch_size=50):

        self.host = host
        self.keyspace = keyspace
        self.table_name = table_name
        self.batch_size = batch_size
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

        if self.upsert_count > self.batch_size:

            print(f"upsert count:  {self.upsert_count}")
            self.upsert_count = 0
            self.session.execute(self.batch)
            self.batch.clear()
            self.log.info(f'Intermediate Batch Insert Completed {self.table_name}')


def list_tables(conf, keyspace, table_name):

    table = BaseTable(host=conf.host, keyspace=keyspace, table_name=table_name)

    table.list_tables()


def reset(conf, table_name, keyspace='grids'):

    table = BaseTable(
        host=conf.host,
        keyspace=keyspace,
        table_name=table_name
    )

    table.list_keyspaces()

    table.del_keyspace()
    table.list_keyspaces()

    table = BaseTable(host=conf.host, keyspace=keyspace, table_name=table_name)

    # grid.create_table()
    # everything(conf, table_name)


def del_table(conf, table_name, keyspace):

    # print(table_name)
    grid = BaseTable(
        host=conf.host,
        keyspace=keyspace,
        table_name=table_name,
    )

    grid.del_table()


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")

    _conf = ConfigFactory.parse_file('./Cassandra.conf')

    _conf.dir_path = dir_path

    cassandra_conf = ConfigFactory.parse_file('./Grids.conf')

    _conf.tables = cassandra_conf

    _keyspace = 'grids'

    _table_name = 'PROBESTART'
    # #
    # _depth = 1
    #
    # list_tables(conf=_conf, keyspace=_keyspace, table_name=_table_name)
    # del_table(conf=_conf, keyspace=_keyspace, table_name=_table_name)
    # list_tables(conf=_conf, keyspace=_keyspace, table_name=_table_name)




#




