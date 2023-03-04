import ipaddress
from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
import datetime



day = datetime.datetime.now()
app = Flask(__name__)
heading = day.strftime("%d")+"-"+day.strftime("%B")+"-"+day.strftime("%Y") +" My Diary"
title = "My Diary"
user_id = "kamal"
page_id = ""

client = MongoClient("mongodb+srv://user:user_pin@dbcluster.frhqp.mongodb.net/?retryWrites=true&w=majority") #host uri
db = client.dairy    #Select the database
todos = db.data #Select the collection name

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/dairyupdate", methods=['POST'])
def dairyupdate():
	txt = request.values.get("textarea")
	page = todos.find_one({"iden":day.strftime("%d")+"-"+day.strftime("%B")+"-"+day.strftime("%Y")+user_id})
	id =page['_id']
	todos.update_one({"_id":ObjectId(id)}, {'$set':{"text":txt}})
	redir=redirect_url()	

	return redirect(redir)

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Tasks
	todos_l = todos.find_one({"iden":day.strftime("%d")+"-"+day.strftime("%B")+"-"+day.strftime("%Y")+user_id})
	print(todos_l)
	a2="active"
	page_id=todos_l
	if todos_l==None:
		todos_l = todos.insert_one({"iden":day.strftime("%d")+"-"+day.strftime("%B")+"-"+day.strftime("%Y")+user_id})
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a3="active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	# todos.insert
	todos.insert_one({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	todos.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()
