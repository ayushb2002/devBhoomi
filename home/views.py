from django.shortcuts import render
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os

from .utils import final, getSelectOpts

# Load States and District Data
state_district_df = pd.read_json(os.path.join(os.getcwd(), 'data.json'))

states = list(state_district_df.name)

def getDistricts(name: str) -> list[str]:
    return list(state_district_df.loc[state_district_df.name == name].districts)

def index(request):
    states.sort()
    return render(request, "home/index.html", {"states": states})

def getStateMap(request, state=''):
    if request.method == "GET":
        stateSend = ' '.join([i.capitalize() for i in state.split('-')]).strip()
        optDict = getSelectOpts()
        if stateSend not in states:
            return render(request, 'errors/404.html', {"error": "State not Found"}) 
        
        return render(request, 'app/state.html', {"state": stateSend, "acts": list(optDict.keys()), "crimes": list(optDict.values())})
    else:
        return render(request, 'errors/405.html', {"error": "Method not Allowed"})

def sendMap(request, state=''):
    if request.method == "POST":
        stateSend = ' '.join([i.capitalize() for i in state.split('-')]).strip()
        print(stateSend)
        if stateSend not in states:
            return render(request, 'errors/404.html', {"error": "State not Found"}) 
        optDict = getSelectOpts()
        act = request.POST['act']
        if (act not in optDict.keys()):
            return render(request, 'errors/404.html', {"error": "Act not Found"}) 
        crime = request.POST['crime']
        if crime not in optDict[act]:
            return render(request, 'errors/404.html', {"error": "Crime not Found"}) 
        map_g = final(act, crime, stateSend)
        return render(request, 'app/state.html', {"state": stateSend, "crime": crime, "act": act, "map": map_g, "acts": list(optDict.keys()), "crimes": list(optDict.values())})
    else:
        return render(request, 'errors/405.html', {"error": "Method not Allowed"})