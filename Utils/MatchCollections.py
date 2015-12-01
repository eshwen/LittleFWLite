
from Utils.DeltaR import *

def matchObjectCollection(recoObjects,matchCollection,deltaRMax = 0.5):

    pairs = {}

    for recoObject in recoObjects:
        recoObject.matched = False
    for match in matchCollection:
        match.matched = False

    if len(recoObjects)==0:
        return pairs
    if len(matchCollection)==0:
        # return {recoObject:None for recoObject in recoObjects}
        return dict( zip(recoObjects, [None]*len(recoObjects)) )

    allPairs = [(deltaR2 (recoObject.eta(), recoObject.phi(), match.eta(), match.phi()), (recoObject, match)) for recoObject in recoObjects for match in matchCollection]
    allPairs.sort()

    deltaR2Max = deltaRMax * deltaRMax
    for dR2, (recoObject, match) in allPairs:
        if dR2 > deltaR2Max:
            break
        if dR2 < deltaR2Max and recoObject.matched == False and match.matched == False:
            recoObject.matched = True
            match.matched = True
            pairs[recoObject] = match

    for recoObject in recoObjects:
        if recoObject.matched == False:
            pairs[recoObject] = None

    return pairs
