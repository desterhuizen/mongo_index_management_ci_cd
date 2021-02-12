# Index Management for Atlas projects

Running and application that make use of MongoDB Atlas for a backing infrastructure pose an interesting problem for managing indexes. MongoDB Professional services generally reccommends managing the required indexes as part of the applicaiton repository. 

During the release cycle a test can be run to check if all th required indexes exists. If there are missing indexes the release need to stop and not applciaiton changes should be completed. 

The indexes can be created via the Atlas API or the Atlas Console.

The project creates a set of scripts that can be used by CI/CD tools to enforce the abotve recommendations. 


## Retrieve current indexes for all collections of the provided database

The order of input variables are fixed!!!

```
retrieve_current_index_list.sh <username> <password> <atlas-cluster-uri-no-db> <dbname>
```

## Check required indexes vs the current indexes

```
python3 check_indexes.py -c current.json -r required.json
```

## Check will attempt to create the missing indexes makinguse of the Atlas API.

```
create_missing_indexes.py  -u <Atlas Public API Key> -p <Atlas Private API Key> -g <Atlas Project ID> -c <Cluster Name>
```

## Required.json structure

The required indexes are defined as a JSON document that contains a single document with a fields for each collection. Each collection contains an array of indexes to be created. Each indxe contains a "keys" and optionally an "options" field.
```
{
 "<COLLECTION1>": [
    {
      "keys":{
        "<KEY>": 1
      }
    },
    {
      "keys":{
        "<KEY1>": 1,
    	"<KEY2>": 1
      }
    }
  ],
  "<COLLECTION2>": [
    {
      "keys":{
        "<KEY1>": 1,
        "<KEY2>": 1,
        "<KEY3>": 'hashed'
      }
    }
  ]
}
```