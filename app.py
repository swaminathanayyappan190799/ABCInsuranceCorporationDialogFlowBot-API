# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 09:09:26 2021

@author: swaminathan.ayyappan
"""
from flask import Flask,request
from pymongo import MongoClient

app=Flask(__name__)

"""
@app.route('/')
def home():
    return "Hi swaminathan"
"""

@app.route('/webhook',methods=['POST'])
def webhook():
    files=request.get_json(silent=True,force=True)
    fulfillment_text,PolicyNumber,repname,repnumber=('','','','')
    query_result=files.get("queryResult")
    intent=query_result.get("intent").get("displayName")
    db=DataBaseConnection()
    if intent == 'PolicyIDCollection':
        policynumber=query_result.get("parameters").get("policynumber")
        fulfillment_text="The Policy Id you mentioned here is "+policynumber+"Is that one is correct ?"
        PolicyNumber=policynumber
    elif intent == 'PolicyIDCollection - yes':
        #policynumber=query_result.get("parameters").get("policynumber")
        query=db.find({'PolicyNumber':PolicyNumber})
        Location=''
        for documents in query:
            Location=str(documents['Location'])
        fulfillment_text="Is this about the property in the location : \n"+str(Location)
    elif intent == 'DescriptionAboutDamage':
        query=db.find({'PolicyNumber':PolicyNumber})
        for documents in query:
            repname=str(documents['RepresentativeName'])
            repnumber=str(documents['RepresentativeContactNumber'])
        fulfillment_text="Okay we have got your reason for claim , your claim's representative is :"+repname+" , and contact them at this number:"+repnumber+", do you want me to repeat it one more time"
    elif intent == "DescriptionAboutDamage - yes":
        query=db.find({'PolicyNumber':PolicyNumber})
        for documents in query:
            repname=str(documents['RepresentativeName'])
            repnumber=str(documents['RepresentativeContactNumber'])
        fulfillment_text="Your claim representative is :"+repname+" and their contact number is :"+repnumber+" , have you got the information ?"
    return {
        "fulfillmentText":str(fulfillment_text)
            }

def DataBaseConnection():
    connection=MongoClient("mongodb+srv://swaminathan:sam240@cluster-1.grijs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    database=connection.get_database("ABCINsuranceCorporation")
    collection=database.get_collection("Customer_Details")
    return collection

if __name__=="__main__":
    app.run(debug=True)
