#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
# genDiagram
#
# Generate diagram and place it in a hoverfly simulation file
# - Assumes there is a file in place called simulationTemplate.json with <<DIAGRAM_BODY>>
###############################################################################
import fire
import os
import json
from shutil import copyfile
import random
import math

def generate(nodeType1Count, nodeType2Count, nodeType3Count, edgeCount, distribution):

    nodes = []
    edges = []

    diagram={"d": {"diagram": {"nodes": nodes, "edges": edges}}}

    for i in range(nodeType1Count):
            nodes.append({"position":{
                    "y": 0,
                    "x": 0},
                "data":{
                    "type": "Type1",
                    "name": "type1_" + str(i),
                    "id": "type1_" + str(i)}})

    for i in range(nodeType2Count):
            nodes.append({"position":{
                    "y": 0,
                    "x": 0},
                "data":{
                    "type": "Type2",
                    "name": "type2_" + str(i),
                    "id": "type2_" + str(i)}})

    for i in range(nodeType3Count):
            nodes.append({"position":{
                    "y": 0,
                    "x": 0},
                "data":{
                    "type": "Type3",
                    "name": "type3_" + str(i),
                    "id": "type3_" + str(i)}})

    for i in range(edgeCount):
            edges.append({"data": {
                "target": targetNodeString(i, nodeType2Count, nodeType3Count),
                "source": sourceNodeString(i, nodeType1Count, edgeCount, distribution)}
                })

    # Store off the original json version of the diagram
    with open("diagram.json", "w") as outfile:
        json.dump(diagram, outfile, indent=4, sort_keys=True)

    # Escape double quotes, remove newlines and spaces so it can go into the hoverfly simulation file
    clean = open('diagram.json').read().replace('\n', '').replace('"', '\\"').replace(' ','')

    templateFile = open('simulationTemplate.json', 'r+')
    target = templateFile.read().replace('<<DIAGRAM_BODY>>', clean)
    targetFile = open('simulationTarget.json', 'w')
    targetFile.write(target)
    targetFile.close()
    templateFile.close()

# Treat type2 and type3 nodes as targets
# Randomly pick a type2 or type3 node as the target
# Kind of assumes that there are equal numbers of each to pick from
def targetNodeString(i, nodeType2Count, nodeType3Count):
    if(nodeType2Count != 0 and nodeType3Count !=0):
        targetNode = random.choice(['type2_', 'type3_'])
        value = i % (nodeType2Count if targetNode == 'type2_' else nodeType3Count)
        return targetNode + str(value)
    elif (nodeType2Count != 0):
        return 'type2_' + str(i % nodeType2Count)
    else:
        return 'type3_' + str(i % nodeType3Count)

# Treat type1 nodes as sources
# This is pure hackery
# - passing cluster for distribution *might* help generate a cluster of connected things
def sourceNodeString(i, nodeType1Count, edgeCount, distribution):
    if(i < int(edgeCount/10) and distribution == 'cluster'):
        modValue = int(round(nodeType1Count/100))
        print("cluster1 modValue", modValue)
        value = str(i % modValue)
        print("cluster1 ", value)
        return "type1_" + value
    elif (distribution == 'cluster'):
        value = str(i - int(edgeCount/100) + int(nodeType1Count/100))
        print("cluster2 ", value)
        return "type1_" + value
    else:
        return "type1_" + str(i % nodeType1Count)

def main():
    # Fire exposes the input parameters to the generate method via the command line
    fire.Fire(generate)

if __name__ == '__main__':
    main()
