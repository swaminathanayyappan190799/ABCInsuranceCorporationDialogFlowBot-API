# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 17:16:40 2021

@author: swaminathan.ayyappan
"""
from flask import Flask,request,make_response
from flask_cors import cross_origin
import json
from pymongo import MongoClient

app=Flask(__name__)

@app.route('/webhook',methods=['POST'])
@cross_origin
def webhook():
    DialogFlowRequest=request.get_json(force=True,silent=True)
    DialogFlowResult=ProcessResult(DialogFlowRequest)
    DialogFlowResult=json.dumps(DialogFlowResult,indent=4)
    print(DialogFlowResult)
    r=make_response(DialogFlowResult)
    r.headers['Content-Type']='application/json'
    return r

def ProcessResult(DialogFlowRequest):
    query_result=DialogFlowRequest.get("queryResult")
    intent = query_result.get("intent").get("displayName")
    parameters=query_result.get("parameters")
    policynumber=parameters.get("PolicyNumber")
    dbconn=DatabaseConnection()
    query=dbconn.find({'PolicyNumber':policynumber})
    for records in query:
        address=records['Location']
        RepName=records['RepresentativeName']
        RepNumber=records['RepresentativeContactNumber']
    if intent == 'PropertyClaim':
        message='The Policy number you said is '+policynumber+'is that correct ?'
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            message
                        ]

                    }
                },
            ]
        }
    elif intent == 'InsuranceNumberConfirmationAndPropertySpecification':
        message='Please verify whether the policy number belongs to this property '+address
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            message
                        ]

                    }
                },
            ]
        }
    elif intent == 'DescriptionAboutDamage':
        message="Okay we have got your reason for claim , your claim's representative is :"+RepName+", and contact them at this number:"+RepNumber+", do you want me to repeat it one more time"
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            message
                        ]

                    }
                },
            ]
        }
    elif intent == 'DescriptionAboutDamage - yes':
        message="Your claim representative is :"+RepName+" and their contact number is :"+RepNumber+"have you got the information"
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            message
                        ]

                    }
                },
            ]
        }


#MongoDB Atlas Connection
def DatabaseConnection():
    connect=MongoClient("mongodb+srv://swaminathan:sam240@cluster-1.grijs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    database=connect.get_database('ABCInsuranceCorporation')
    collection=database.get_collection('Customer_Details')
    return collection

if __name__ =="__main__":
    app.run(port=5000,debug=True)