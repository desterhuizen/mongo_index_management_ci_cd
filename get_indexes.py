import json
import sys
import argparse
from pymongo import MongoClient
from bson.json_util import dumps, loads 
import time

parser = argparse.ArgumentParser();
parser.add_argument("-u", "--username", help="DB Username", type=str, required=True)
parser.add_argument("-p", "--password", help="DB Password",type=str, required=True)
parser.add_argument("-d", "--db-name", help="Databasea Name",type=str, required=True)
parser.add_argument("-c", "--cluster-addr", help="Cluster address" ,type=str, required=True)
parser.add_argument("-y", "--yes", help="Agree to build", action='store_true')
parser.add_argument("--verbose", "-v", help="Verbose output", action='store_true')

args = parser.parse_args()

username=args.username
password=args.password
db_name=args.db_name
cluster_address=args.cluster_addr
agree=args.yes

retry_count=0
while retry_count < 5:
	try:
		print ("Connecting to: "+cluster_address)
		client = MongoClient(cluster_address, username=username, password=password, tls=True )
		db = client[db_name]

		collection_name_list = db.list_collection_names()

		currentIndexes = [];
		for collection_name in collection_name_list:
			IndexItem = {
				"collectionName" : collection_name,
				"indexes": db[collection_name].list_indexes()
			}
			currentIndexes.append(IndexItem)

		with open('current.json', 'w') as file: 
		    file.write(dumps(currentIndexes)) 
		break
	except: 
		retry_count +=1 ;
		print ("Could not connect retrying in "+str(10 * retry_count)+" seconds")		
		time.sleep(10*retry_count)
		if (retry_count == 5):
			sys.stdout.write("Could not connect to the cluster aborting")

