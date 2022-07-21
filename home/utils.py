import base64
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from io import BytesIO


crimes = pd.read_csv(os.path.join(os.getcwd(), "processed_data", "crime.csv"))
mp = gpd.read_file(os.path.join(os.getcwd(), 'map','India.shp'))

def generateMap(india_map, state):
    state_map = india_map[india_map["statename"]==state]
    fig, ax = plt.subplots(1, figsize=(8, 8))
    plt.xticks(rotation=90)
    ax = state_map.plot(ax=ax)
    state_map.apply(lambda x: ax.annotate(text=x["distname"], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)

def exportMap():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    map_graph_png = buffer.getvalue()
    map_graph = base64.b64encode(map_graph_png)
    map_graph = map_graph.decode('utf-8')
    buffer.close()
    return map_graph


def generateHeatMap(india_map, df, state, crime):
    plt.switch_backend('AGG')
    state_map = india_map[india_map["statename"]==state]
    heat_map = state_map.merge(df, on=["distname", "statename"])
    fig, ax = plt.subplots(1, figsize=(15, 15))
    plt.xticks(rotation=90)
    plt.title(f'{crime} in {state}')
    ax = heat_map.plot(column=crime, cmap="Reds", linewidth=0.4, ax=ax, edgecolor="0.4")
    heat_map.apply(lambda x: ax.annotate(text=x["distname"], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
    bar_info = plt.cm.ScalarMappable(cmap="Reds", norm=plt.Normalize(vmin=0, vmax=120))
    bar_info._A = []
    cbar = fig.colorbar(bar_info)
    map_g = exportMap()
    return map_g

def getDataFromCsv(act="IPC"):
    dirs = {"Arms Act": 'arms_act.csv', "Gunda Act": 'gunda_act.csv',"IPC": 'ipc.csv'}
    data = pd.read_csv(os.getcwd() + "/processed_data/"+dirs[act])
    cols = data.columns[3:]
    return data, cols

def getSelectOpts():
    dirs = {"Arms Act": 'arms_act.csv', "Gunda Act": 'gunda_act.csv',"IPC": 'ipc.csv'}
    sops = {}
    for act in dirs:
        data = pd.read_csv(os.getcwd() + "/processed_data/"+dirs[act])
        cols = data.columns[3:]
        sops[act] = list(cols)
    return sops

def final(act="IPC", crime="ARSON", state="Uttar Pradesh"):
    crime = crime.upper()
    mp = gpd.read_file(os.getcwd() + '/map/India.shp')
    try:
        arson, cols = getDataFromCsv(act)
    except:
        raise
        return False
    if crime not in cols:
        return False
    states = arson.statename.unique()
    
    if state not in states:
        return False
    try:
        return generateHeatMap(mp, arson, state, crime)
    except:
        raise
        return False