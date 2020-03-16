#!/usr/bin/env python
"""
Author: Gideon Bar
"""
import json
import os
import sys
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

_dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"current working dir: {_dir_path}")
sys.path.insert(0, _dir_path)

from base_cassandra import *


KEYSPACE = 'grids'


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

    def __init__(self, host, table_name, keyspace=KEYSPACE, depth=1, point_primary_key=True, value_list=False):
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

        super().__init__(host=host, keyspace=KEYSPACE, table_name=table_name)
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
        keyspace=KEYSPACE,
        table_name=table_name,
        depth=depth,
        point_primary_key=point_primary_key,
        value_list=value_list
    )

    point_grid = grid.everything()

    return point_grid


def create_point_table(conf, table_name, depth, point_primary_key, value_list):

    grid = PointGrid(
        host=conf.host,
        keyspace=KEYSPACE,
        table_name=table_name,
        depth=depth,
        point_primary_key=point_primary_key,
        value_list=value_list
    )

    grid.create_table()

    # grid.everything()

    return f"created:  {table_name}"


def populate_point_table(conf, table_name, depth, point_primary_key, value_list):

    full_path = f"{conf.dir_path}/COMPACT/{table_name}.json"

    print(f"table name: {table_name} full path: {full_path}")

    print(f"table name: {table_name} depth: {depth} full path: {full_path}")

    with open(full_path) as json_file:

        try:
            data = json.load(json_file)

            grid = PointGrid(
                host=conf.host,
                keyspace=KEYSPACE,
                table_name=table_name,
                depth=depth,
                point_primary_key=point_primary_key,
                value_list=value_list
            )

            grid.insert_data(data)

        except Exception as e:
            print(f"Error occurred while trying to run bash command: {e}")

            return f'failed {table_name}'

        return f'populated {table_name}'


def test_point_grids(conf):

    snooze = 5

    print("Deleting grids keyspace and all tables ...")
    reset(conf, "table_name")

    print(f"short sleep or {snooze} and listing tables ...")
    sleep(snooze)
    list_tables(conf=conf, keyspace=KEYSPACE, table_name="table_name")

    print(f"short sleep or {snooze} then creating tables and listing them ...")
    sleep(snooze)
    all_point_tables(conf, create_point_table)
    list_tables(conf=conf, keyspace=KEYSPACE, table_name="table_name")

    print(f"short sleep or {snooze} then populating tables ...")
    sleep(snooze)
    all_point_tables(conf, populate_point_table)

    grid_type_tuples = conf.tables.spatial_grids

    for grid_tup in grid_type_tuples:

        print(f"short sleep or {snooze} then checking tables content ...")
        sleep(snooze)

        everything_point(conf, grid_tup[0], grid_tup[1], grid_tup[2], grid_tup[3])


def all_point_tables(conf, f_point):

    grid_type_tuples = conf.tables.spatial_grids

    print(grid_type_tuples)

    source_files = rx.from_(grid_type_tuples)

    max_threads = 5

    with concurrent.futures.ProcessPoolExecutor(max_threads) as executor:

        obs_files = source_files.pipe(

            ops.flat_map(
                lambda grid_tup: executor.submit(
                    f_point,
                    conf,
                    grid_tup[0],
                    grid_tup[1],
                    grid_tup[2],
                    grid_tup[3],
                )
            )
        )
        obs_files.subscribe(lambda value: print(f"Received {value}"))


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")

    _conf = ConfigFactory.parse_file('./Cassandra.conf')

    _conf.dir_path = dir_path

    cassandra_conf = ConfigFactory.parse_file('./tables.conf')

    _conf.tables = cassandra_conf

    _keyspace = KEYSPACE
    test_point_grids(_conf)

    _table_name = 'PROBESTART'
    # #
    # _depth = 1
    #
    # create_point_table(_table_name, _conf, depth=_depth, point_primary_key=False)
    # list_tables(conf=_conf, keyspace=_keyspace, table_name=_table_name)
    # del_table(conf=_conf, keyspace=_keyspace, table_name=_table_name)
    # list_tables(conf=_conf, keyspace=_keyspace, table_name=_table_name)
    #
    # everything_point(_conf, _table_name, _depth, True, False)
    #
    # everything_point(_conf, _table_name, 2)



#




