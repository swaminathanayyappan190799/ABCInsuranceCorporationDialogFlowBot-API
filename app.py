# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 17:54:59 2021

@author: swaminathan.ayyappan
"""
#Importing Essential Libraries
from flask import Flask,request,make_response
from flask_cors import cross_origin
import json
from pymongo import MongoClient


#Initializing the flask application.
app=Flask(__name__)

#Getting data from dialogflow
@app.route('/webhook',methods=['POST'])
@cross_origin
def webhook():
    files=request.get_json(silent=True,force=True)
    results=ProcessFiles(files)
    results=json.dumps(results,indent=4)
    print(results)
    r = make_response(results)
    r.headers['Content-Type'] = 'application/json'
    return r

#Processing the request from dialogflow.
def ProcessFiles(files):
    database=DatabaseConnection()
    result=files.get('queryResult')
    intent=result.get("intent").get("displayName")
    parameters=result.get("parameters")
    PolicyNumber=parameters.get("PolicyNumber")
    query=database.find({'PolicyNumber':PolicyNumber})
    if intent == 'PolicyNumberGathering':
        webhook_message="The policy number you mentioned is"+PolicyNumber+"Is that correct ?"
        
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhook_message
                        ]

                    }
                },
            ]
        }
    if intent == 'PolicyNumberConfirmation - yes':
        for i in query:
            Location=i['Location']
        webhook_message="Is this about the property in this location :"+Location
        
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhook_message
                        ]

                    }
                },
            ]
        }
    if intent == 'DescriptionAboutDamage':
        for j in query:
            RepName=j['RepresentativeName']
            RepNum=j['RepresentativeContactNumber']
        webhook_message="Okay we got the reason for your claim , your claim representative name is :"+RepName+" and contact them at this number:"+RepNum+", do you want me to repeat it one more time"    
 
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhook_message
                        ]

                    }
                },
            ]
        }
    if intent == 'DescriptionAboutDamage - yes':
        for j in query:
            RepName=j['RepresentativeName']
            RepNum=j['RepresentativeContactNumber']
        webhook_message="your claim representative name is :"+RepName+" and contact them at this number:"+RepNum
        
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhook_message
                        ]

                    }
                },
            ]
        }   
#MongoDB Atlas connection        
def DatabaseConnection():
    dbconnection=MongoClient("mongodb+srv://swaminathan:sam240@cluster-1.grijs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db=dbconnection.get_database('ABCInsuranceCorporation')
    collection=db.get_collection('Customer_Details')
    return collection

if __name__ == '__main__':
    app.run(port=5000,debug=True)
    
        



