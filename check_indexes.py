#!/usr/bin/env python3

import json
import sys
import argparse

parser = argparse.ArgumentParser();
parser.add_argument("-c", "--current_path", help="Path to the current indexes json file from retrieve_current_index_list.sh", type=str, required=True)
parser.add_argument("-r", "--required_path", help="Path to the required indexes json file from the application repo",type=str, required=True)
parser.add_argument("--verbose", "-v", help="Verbose output")

args = parser.parse_args()

current_indexes_path=args.current_path
required_indexes_path=args.required_path

with open(current_indexes_path, "r") as file1:
	current = json.load(file1)
with open(required_indexes_path, "r") as file2:
	requiredIndexes = json.load(file2)

currentIndexes = {}
currentIndexCatalog = {}
for collectionInfo in current:
	currentIndexes[collectionInfo['collectionName']] = []
	currentIndexCatalog[collectionInfo['collectionName']] = []
	for index in collectionInfo['indexes']:
		tmpIndex = {"options": {"name": index["name"]}, "keys": index['key']}
		if "unique" in index:
			tmpIndex["options"]["unique"] = index["unique"]
		currentIndexes[collectionInfo['collectionName']].append(tmpIndex)
		currentIndexCatalog[collectionInfo['collectionName']].append(index['key'])
		
missingIndexes = {};
missingIndexFound = False;

for (collection, indexes) in requiredIndexes.items():
	missingIndexes[collection] = []
	for index in indexes: 
		if collection not in currentIndexCatalog.keys() or index["keys"] not in currentIndexCatalog[collection]:
			missingIndexFound = True
			missingIndexes[collection].append(index)

if missingIndexFound:
	sys.stderr.write("The following indexes are missing:\n")
	for collection,indexes in missingIndexes.items():
		if len(indexes) > 0:
			sys.stderr.write(collection+":\n")
			sys.stderr.write(json.dumps(indexes)+"\n")
	sys.stderr.write("Please run the Index creation script locally before attempting a redeployment\n")
else: 
	sys.stdout.write("Indexes are all in place for this reployment\n")