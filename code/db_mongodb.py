import pymongo
from pymongo import MongoClient
import json

#--------------------------------writing csv file----------------------------------------
def convert_to_csv(data):
    
    dicti = data[0]
    #print(list(dicti.keys()))
    column = list(dicti.keys())

    with open("output.csv","w",newline="") as f:  # python 2: open("output.csv","wb")
        cw = csv.DictWriter(f,column,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(data)

    return


#----------------------------------writing json file---------------------------------------
def convert_to_json(data):

    final = json.dumps(data, indent=2)

    fl = open('output.json', 'w')
    fl.write(final)
    fl.close()

    return




#-------------------------------------upload data-------------------------------------------------------
def import_data_to_mongo(db_name , filepath,cluster_name = "db1"):
	st = "mongodb+srv://somyalalwani:ayush123@cluster0.hknle.mongodb.net/db1?retryWrites=true&w=majority"
	cluster = pymongo.MongoClient(st)
	#print(cluster)

	db = cluster[cluster_name]

	print(db.list_collection_names())

	if db_name in db.list_collection_names():
		return

	collection = db[db_name]

	with open(filepath) as f:
		data = json.load(f)
		for row in data:
			#print(row)
			#print("------------------------------------------------------")
			collection.insert_one(row)
	cluster.close()
	return


#---------------------------------------simple query----------------------------------------------
def query_call_mongodb1(db_name,x,y,z,cluster_name = "db1"): #select * from db_name where xyz
	#where x="age",y="<", z="12"
	#print("wow")
	st = "mongodb+srv://somyalalwani:ayush123@cluster0.hknle.mongodb.net/db1?retryWrites=true&w=majority"
	cluster = pymongo.MongoClient(st)
	db = cluster[cluster_name]
	table1 = db[db_name]
	#print(x,y,z)
	if y=="==" or y=="eq":
		#print("equal")
		search_query = {x:z}
	elif y==">":
		#print("heyy")
		search_query = {x:{"$gt":z}}
	elif y==">=":
		search_query = { x:{"$gte":z}}
	elif y == "<":
		search_query = {x:{"$lt":z}}
	elif y=="<=":
		search_query = {x: { "$lte":z}}
	elif y=="!=" or y=="not equal":
		search_query = {x: { "$ne":z}}
	
	result1 = table1.find(search_query)
	#print(type(result1))
	final_result = []
	for record in result1:
		#print(record)
		if '_id' in record:
			del record['_id']
		final_result.append(record)
	# print("-------------------------------------------------------------")
	# print(type(final_result[0]))
	# print("-------------------------------------------------------------")
	return final_result




#---------------------------------------------get column function----------------------------------
def get_columns(filepath):
	l=[]
	f = open(filepath, 'r')
	lines = f.readlines()
	f.close()
	for x in lines:
		x = x.strip()
		#print(x)
		l.append(x)
	del lines
	#print("------------------------------")
	#print(l)
	return l

#--------------------------------------------------complex query code----------------------------
def complex_query_call_mongodb(query,cluster_name = "db1"):
	print(cluster_name)
	query = str(query)
	print(query)
	x = query.split(".",1)
	db_name = x[0].strip()
	query = x[1]

	try:
		st = "mongodb+srv://somyalalwani:ayush123@cluster0.hknle.mongodb.net/db1?retryWrites=true&w=majority"
		cluster = pymongo.MongoClient(st)
		db = cluster[cluster_name]
		

		table1 = db[db_name]
		final_result = []

		st =('result1 = table1.'+query+"\n"
            "for record in result1:\n"
            "\tif '_id' in record:\n"
            "\t\tdel record['_id']\n"
            "\tfinal_result.append(record)"
            )
		exec(st)
		print(final_result)
		return final_result

	except:
		final_result = -1
	
	return final_result






'''

def query_call_mongodb2(db_name,x,y,z,col_name,cluster_name = "db1"): #select col_name from db_name where xyz
	#where x="age",y="<", z="12"
	st = "mongodb+srv://somyalalwani:ayush123@cluster0.hknle.mongodb.net/db1?retryWrites=true&w=majority"
	cluster = pymongo.MongoClient(st)
	db = cluster[cluster_name]
	table1 = db[db_name]
	
	if y=="==" or y=="eq":
		print("equal")
		search_query = {x:z}
	elif y==">":
		search_query = {x:{"$gt":z}}
	elif y==">=":
		search_query = { x:{"$gte":z}}
	elif y == "<":
		search_query = {x:{"$lt":z}}
	elif y=="<=":
		search_query = {x: { "$lte":z}}
	elif y=="!=" or y=="not equal":
		search_query = {x: { "$ne":z}}
	
	result1 = table1.find(search_query)
	for record in result1:
		print(record[col_name])
	return

'''