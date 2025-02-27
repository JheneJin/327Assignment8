from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta
import time

DBName = "traffic" #Use this to change which Database we're accessing
connectionURL = "mongodb+srv://aidanmara:helloWorld@assignment7.oxdb33x.mongodb.net/?retryWrites=true&w=majority&appName=Assignment7" #Put your database URL here
sensorTable = "traffic data" #Change this to the name of your sensor data table

def QueryToList(query):
  
  pass; #TODO: Convert the query that you get in this function to a list and return it
  #HINT: MongoDB queries are iterable

def QueryDatabase() -> []:
	global DBName
	global connectionURL
	global currentDBName
	global running
	global filterTime
	global sensorTable
	cluster = None
	client = None
	db = None
	try:
		cluster = connectionURL
		client = MongoClient(cluster)
		db = client[DBName]
		print("Database collections: ", db.list_collection_names())

		#We first ask the user which collection they'd like to draw from.
		sensorTable = db[sensorTable]
		print("Table:", sensorTable)

		#We convert the cursor that mongo gives us to a list for easier iteration.
		timeCutOff = datetime.now() - timedelta(minutes=5)

		oldDocuments = QueryToList(sensorTable.find({"time":{"$gte":timeCutOff}}))
		currentDocuments = QueryToList(sensorTable.find({"time":{"$lte":timeCutOff}}))


		print("Current Docs:",currentDocuments)
		print("Old Docs:",oldDocuments)

		sensorTable = {}

		for item in currentDocuments:
			currSense = 0

			for i2 in item.payload:
				if type(i2) == int:
					i2 = currSense

			sensorTable[item.payload.device_asset_uid].update(list(sensorTable[item.payload.device_asset_uid]).append(i2))

		for key in sensorTable.keys():
			size = len(sensorTable[key])
			sensorTable[key].update(sum(sensorTable[key])/size)

		sortedKeys = list(sorted(sensorTable, key=lambda k: sensorTable[k]))

		return sortedKeys


	except Exception as e:
		print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		exit(0)

