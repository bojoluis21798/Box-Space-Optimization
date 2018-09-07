import numpy as np
import sys
from copy import deepcopy
from itertools import combinations

def findBestModels(passed_models, target):
    models = passed_models[1:] # remove None type
    results = []
    for x in range(len(models)):
        results.extend(
            [   
                combo for combo in combinations(models , x)  
                    if sum((model.solidVolume for model in combo)) == target
            ]   
        )
    if len(results) == 0 and sum((model.solidVolume for model in models)) == target:
        results.append(models)
    elif len(results) == 0:
        combis = []
        for x in range(len(models) + 1):
            combis.extend(
                [
                    combo for combo in combinations(models, x)
                        if sum((model.solidVolume for model in combo)) < target and sum((model.solidVolume for model in combo)) > 0
                ]
            )
        
        maxsum = 0
        maxcombi = []
        for combi in combis:
            temp = sum((model.solidVolume for model in combi))
            if temp > maxsum:
                maxsum = temp
                maxcombi = combi
        results.append(maxcombi)
    final = list(results[0])
    final.sort(key = lambda x: x.solidVolume, reverse = True)
    return final