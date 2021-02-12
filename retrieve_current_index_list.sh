#!/usr/bin/env bash


while getopts u:p:c:d: flag
do
	case "${flag}" in 
		u) USERNAME=${OPTARG};;
		p) PASSWORD=${OPTARG};;
		c) CLUSTER_ADDRESS=${OPTARG};;
		d) DB_NAME=${OPTARG};;
	esac;
done	

if [ -z "$USERNAME" ]; then 
	echo "DB Username is required"
fi

if [ -z "$PASSWORD" ]; then 
	echo "DB Password is required"
fi

if [ -z "$CLUSTER_ADDRESS" ]; then 
	echo "Cluster Address is required"
fi

if [ -z "$DB_NAME" ]; then 
	echo "DB name is required"
fi

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ] || [ -z "$CLUSTER_ADDRESS" ] || [ -z "$DB_NAME" ]; then 
	echo "retrieve_current_index_list.sh -u <username> -p <password> -c <atlas-cluster-uri-no-db> -d <dbname>"
	exit
fi

if [ -f "current.json" ]; then
   echo "Found an old copy of in this folder, would you like to remove it else it will be overwritten"
   rm -i current.json
fi

mongo "$CLUSTER_ADDRESS/$DB_NAME" --password $PASSWORD --username $USERNAME --eval "db.getCollectionNames().forEach(function (collectionName){ var indexes = db[collectionName].getIndexes(); print (JSON.stringify({"collectionName": collectionName,"indexes": indexes})) })" | grep "collectionName" | sed s/\{\"\$numberLong\"\:\"1\"\}/1/g | sed s/\{\"\$numberLong\"\:\"-1\"\}/-1/g | jq -r -s > current.json;

if [ -f current.json ]; then 
	echo "Current indexes stored in current.json"
fi

