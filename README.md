# Index Management for Atlas projects

Running an application that make use of MongoDB Atlas for a backing infrastructure pose an interesting problem for managing indexes. MongoDB generally reccommends managing the required indexes as part of the applicaiton repository. 

During the release cycle a test can be run to check if all th required indexes exists. If there are missing indexes the release needs to stop and no applciaiton changes should be completed. 

The indexes can be created via the Atlas API or the Atlas Console.

The project creates a set of scripts that can be used by CI/CD tools to enforce the abotve recommendations. 


## Retrieve current indexes for all collections of the provided database

```
python3 get_indexes.py -u <USERNAME> -p <PASSWORD> -d <DB_NAME> -c <CLUSTER_ADDR>
```

## Check required indexes vs the current indexes

```
python3 check_indexes.py -c current.json -r required.json
```

## Check will attempt to create the missing indexes makinguse of the Atlas API.

```
python3 create_missing_indexes.py  -u <Atlas Public API Key> -p <Atlas Private API Key> -g <Atlas Project ID> -c <Cluster Name>
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
        "<KEY3>": 'hashed'
      }
    }
  ]
}
```