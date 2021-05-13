from igraph import Graph, load
import pandas as pd
import numpy as np
from itertools import chain, product
from collections import Counter, defaultdict
from operator import methodcaller

from datetime import datetime, timedelta
from copy import deepcopy
import re

import unicodedata


def nrm(s, t='NFKC'):
    return unicodedata.normalize(t, s)

g = load('graph.graphml')

df = pd.read_excel('BN-BG-HN-VP.xlsx')
commune = df['Xã/Phường'].values
district = df['Quận/Huyện'].values
province = df['Tỉnh/TP'].values



def get_datetime(s):
    return datetime.strptime(s, "%d/%m/%Y")


def read_patient(path):
    return pd.read_csv(path)


def extract_data(df, start_date, end_date):
    col = df.columns[0]
    for idx, row in df.iterrows():
        print(row.values.tolist()[0])


def get_by_date(df, start_date, end_date):
    dframe = []
    for idx, row in df.iterrows():
        if get_datetime(row[0]) >= start_date and get_datetime(
                row[0]) <= end_date:
            dframe.append(row.values.tolist())
    return pd.DataFrame(dframe, columns=df.columns)


def get_init_position(df, start_date, end_date):
    dframe = get_by_date(df, start_date, end_date)
    return dframe.groupby(["Xã/Phường", "Quận/Huyện",
                           "Tỉnh/TP"]).count()["MCB"].to_dict()


def generate_init(g, starts, n_samples):
    p_id = []
    #     print(starts)
    for k, v in starts.items():
        try:
            p_id.append([[
                g.vs.find(commune=k[0],
                          district=k[1],
                          province=k[2]).index
            ] for _ in range(v)])
        except:
            print(k, v)

    init_state = []
    for pid in p_id:
        for pidd in pid:
            init_state.append(pidd)

    n_samples = n_samples

    return [deepcopy(init_state) for _ in range(n_samples)]


def random_walk(g, start, n_samples, n_steps):
    walks_tracking = generate_init(g, start, n_samples)
    for walk in walks_tracking:
        for i in range(len(walk)):
            try:
                r_walk = g.random_walk(walk[i][0], n_steps, mode="ALL")
                walk[i] = r_walk
            except:
                print(walk[i])
    return np.array(walks_tracking)


def walk_simulation(g, dt, n_samples, n_steps, start_date, end_date):
    starts = get_init_position(dt, start_date, end_date)
    walks_tracking = generate_init(g, starts, n_samples)

    return random_walk(g, starts, n_samples, n_steps)


def loop(g, dt, n_samples, n_steps, start_date, end_date, time_window_size=15):
    start = get_datetime(start_date) - timedelta(days=time_window_size)
    end = get_datetime(end_date)
    result = {}
    while start + timedelta(days=time_window_size) <= end:
        end_tmp = start + timedelta(days=time_window_size)
        tmp = walk_simulation(g, dt, n_samples, n_steps, start, end_tmp)
        result[datetime.strftime(end_tmp, "%d/%m/%Y")] = tmp
        start += timedelta(days=1)
    return result


def get_loc_tuple(g):
    loc = {}
    for v in g.vs:
        comm = v["commune"]
        dist = v["district"]
        tmp = (comm, dist)
        loc[tmp] = [comm, dist]
    return loc

# def result_processing(g, result):
#     provinces = pd.read_csv('input/maps/provinces.csv').values.tolist()
#     provinces = list(chain.from_iterable(provinces))
#     result_clone = deepcopy(result)
# #     print(result_clone[:100])
#     result_clone = list(chain.from_iterable(result_clone))
#     result_clone = list(chain.from_iterable(result_clone))
#     res = Counter(result_clone)

#     loc_list = {}
    
    
#     for k, v in res.items():
#         province = g.vs[k]["province"]
#         loc_list[province] = v

#     for p in provinces:
#         if p not in loc_list.keys():
#             loc_list[p] = 0

#     ddff = {}
#     for k, v in loc_list.items():
#         ddff[k] = v
#     return ddff

def result_processing(result):
    result_clone = deepcopy(result)
    try:
        result_clone = result_clone.reshape([
            1,
            len(result_clone[0]) * len(result_clone) * len(result_clone[0][0])
        ])[0]
        res = Counter(result_clone)
    except:
        res = {k: 0 for k in range(1, 581)}

    loc_list = {}

    for k, v in res.items():
        comm = g.vs[k]["commune"]
        dist = g.vs[k]["district"]
        prov = g.vs[k]['province']
        loc_list[tuple([comm, dist, prov])] = v

    for c, d, p in zip(commune, district, province):
        if tuple([c, d, p]) not in loc_list.keys():
            loc_list[tuple([c, d, p])] = 0

    ddff = {}
    for k, v in loc_list.items():
        ddff[k] = v
    return ddff


def merge_dict(*d):
    # initialise defaultdict of lists
    dd = defaultdict(list)

    # iterate dictionary items
    dict_items = map(methodcaller("items"), (tuple([*d])))
    for k, v in chain.from_iterable(dict_items):
        dd[k].extend([v])
    return dd


def storage_processing(results):
    final = {}
    tmp = []
    columns = ["Xa/Phuong", "Quan/Huyen", "Tinh/TP"]
    for date, val in results.items():
        tmp.append(result_processing(val))
        columns.append(date)
    final = merge_dict(*tmp)
    for k, v in final.items():
        final[k].insert(0, k[0])
        final[k].insert(1, k[1])
        final[k].insert(2, k[2])
    return final, columns


def get_dataframe(final, col):
    data = pd.DataFrame.from_dict(final).values
    for i in range(2, len(data)):
        try:
            data[i] = list(map(lambda x: int(x) * 100 / sum(data[i]), data[i]))
        except:
            pass
    risk_evaluation = pd.DataFrame(data.transpose(), columns=col)
    return risk_evaluation


def gen_csv(results):
    final, columns = storage_processing(results)

    risk = get_dataframe(final, columns)
    #     risk.to_csv("output/BacNinh_commune.csv", index=False)
    risk.to_excel("commune.xls", index=False)

    #     (risk.groupby(by=["Quan/Huyen"]).sum()).to_csv("output/BacNinh_district.csv")
    (risk.groupby(by=["Quan/Huyen"]).sum()
     ).to_excel("district.xls")
    (risk.groupby(
        by=["Tinh/TP"]).sum()).to_excel("province.xls")
    return True


patients = pd.read_excel('Grooo.xls')
comm = patients['Xã/Phường'].values
dist = patients['Quận/Huyện'].values
prv = patients['Tỉnh/TP'].values

comm = list(map(nrm, comm))
dist = list(map(nrm, dist))
prv = list(map(nrm, prv))

patients['Xã/Phường'] = comm
patients['Quận/Huyện'] = dist
patients['Tỉnh/TP'] = prv


risk_result = loop(g, patients, 10000, 20, "8/5/2021", "18/5/2021", 6)
gen_csv(risk_result)