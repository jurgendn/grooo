from collections import Counter, OrderedDict
from itertools import chain

import numpy as np
import scipy.stats as ss
import sqlalchemy as sql


def create_connection(path='sqlite:///database.db'):
    """Create connection to database

    Args:
        path (str, optional): Path to database.
                    Defaults to 'sqlite:///database.db'.

    Returns:
        (tuple): Return conn, engine, metadata
    """
    engine = sql.create_engine(path, encoding='utf8')
    conn = engine.connect()
    metadata = sql.MetaData()
    return conn, engine, metadata


def get_connection(table: str, metadata, engine):
    """[summary]

    Args:
        table (str): Table name in Database
        metadata: metadata from create_connection
        engine: engine from create_connection

    Returns:
        Table: table from db
    """
    return sql.Table(table, metadata, autoload=True, autoload_with=engine)


user_types = {
    -1: 'Unlabeled Users',
    0: 'Trusted Users',
    1: 'Estate Spammers',
    2: 'LoanSpam',
    3: 'DebtSpam',
    4: 'CheatSpam',
    5: 'EstateSpam',
    6: 'Others'
}


def get_node_list(graph):
    """Get node list from graph

    Args:
        graph (Graph - python_igraph): Python iGraph instance

    Returns:
        dict: node by types
    """
    nodes_list = {}
    for k, v in user_types.items():
        nodes_list[v] = [v.index for v in graph.vs if v['Type'] == k]
    return nodes_list


def get_call_rank(graph, nodes_list):
    ranks_by_type = {}
    for k, v in nodes_list.items():
        ranks_by_type[k] = list(graph.pagerank(v,
                                               weights=graph.es['weights']))
    return ranks_by_type


def get_confidence_interval(sample, alpha=0.95):
    return np.around(
        ss.poisson.interval(alpha, np.mean(sample), np.var(sample, ddof=1)), 4)


def scale_up(sample, scale_factor=1e5):
    return list(map(lambda x: x * scale_factor, sample))


def set_edges_weight(graph, total_duration_per_users: dict):
    """Normalize weight

    Args:
        graph (python-igraph.Graph): Graph
        total_duration_per_users (dict): Duration each users made
    """
    for e in graph.es:
        source = graph.vs[e.source]['name']
        e['weights'] = e['weights'] / total_duration_per_users[source]
    return True
