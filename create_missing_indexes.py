import json
import sys
import requests
from requests.auth import HTTPDigestAuth
import argparse


parser = argparse.ArgumentParser();
parser.add_argument("-u", "--public-key", help="Atlas Project Public API Key", type=str, required=True)
parser.add_argument("-p", "--private-key", help="Atlas Project Private API Key",type=str, required=True)
parser.add_argument("-g", "--project-id", help="Atlas Project ID",type=str, required=True)
parser.add_argument("-c", "--cluster-name", help="Atlas Cluster name" ,type=str, required=True)
parser.add_argument("-y", "--yes", help="Agree to build", action='store_true')
parser.add_argument("--verbose", "-v", help="Verbose output", action='store_true')

args = parser.parse_args()

user=args.public_key
passw=args.private_key
project_id=args.project_id
cluster_name=args.cluster_name
agree=args.yes

def create_index(db, collection, indexes):
	headers = {'Accept': 'application/json',  'Content-Type': 'application/json'}
	url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+project_id+"/clusters/"+cluster_name+"/index"

	data = {}
	keys = []
	for index_key, value in indexes['keys'].items():
		keyItem = {}
		keyItem[index_key] = value
		keys.append(keyItem)
		data = { "db":db,"collection": collection,"keys": keys }
	if "options" in indexes and indexes["options"]:
		if "unique" in indexes["options"]:
			sys.stderr.write ("Indexes with unique option cannot be built using the API\n")
			sys.stderr.write ("See: https://docs.atlas.mongodb.com/data-explorer/indexes#optional-specify-the-index-options\n")
			sys.stderr.write ("Please create the following index manually:\n")
			data["options"] = indexes["options"]
			print (data)
			return;
		else: 
			data["options"] = indexes["options"]
		
	result = requests.post( url, json=data, auth=HTTPDigestAuth(user, passw), headers=headers)
	print (result.json())
	

def create_indexes(indexes):
	for collection,indexList in indexes.items():
		for index in indexList:
			print ("creating ",index, " on ", collection)
			create_index("dvr", collection, index)

def yes_no(answer):
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])
     
    while True:
        choice = input().lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           print ("Please respond with 'yes' or 'no'")

with open("current.json", "r") as file1:
	current = json.load(file1)
with open("required.json", "r") as file2:
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
	if agree: 
		create_indexes(missingIndexes)
	else:
		print("Do you want to create these indexes?")
		if yes_no("Do you want to create these indexes?"):
			create_indexes(missingIndexes)
else: 
	sys.stdout.write("Indexes are all in place for this reployment\n")