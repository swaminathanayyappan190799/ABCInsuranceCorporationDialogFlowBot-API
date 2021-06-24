# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 21:18:11 2021

@author: swaminathan.ayyappan
"""
from flask import Flask,request
import pymongo

connection="mongodb+srv://swaminathan:sam240@cluster-1.grijs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app=Flask(__name__)
client=pymongo.MongoClient(connection)

Database=client.get_database('ABCInsuranceCorporation')
Collection=Database.Customer_Details
Conversationcollection=Database.Conversations

#Function to store policy number globally.
def policy(number):
    policy.variable=str(number).upper()
    
#Function to save the conversation inside DB.
def StoreConversations(Id,request,response,intent):
    single_convo={'ResponseID':Id,
                  'Intent':intent,
                  'User':request,
                  'Bot':response}
    Conversationcollection.insert_one(single_convo)
    
    
    
#Webhook to give response to user from bot.
@app.route('/webhook',methods=['POST'])
def webhook():
    files=request.get_json(silent=True,force=True)
    query_result=files.get("queryResult")
    fulfillment_text=query_result.get('fulfillmentText')
    responseId=files.get('responseId')
    query_text=query_result.get('queryText')
    intent=query_result.get("intent").get("displayName")
    parameters=query_result.get('parameters')
    if intent == 'PolicynumberGathering':
        policy_number=parameters.get('policynumber')
        policy(policy_number)
        fulfillment_text=str('Please verify your policy number which is '+str(policy_number))
    elif intent == 'AddressDisplay':
        number=policy.variable
        query=Collection.find({'PolicyNumber':number})
        for records in query:
          address=str(records.get('Location'))
        fulfillment_text='Is this about the property in this location :'+str(address)
    elif intent == 'ReasonForClaim':
        policynumber=policy.variable
        query=Collection.find({'PolicyNumber':policynumber})
        for records in query:
            repname=str(records.get('RepresentativeName'))
            repnumber=str(records.get('RepresentativeContactNumber'))
        fulfillment_text="Okay. Your claims representative's name is "+repname+" . His contact number is "+repnumber+". Would you like me to repeat that information?"
    StoreConversations(responseId,query_text,fulfillment_text,intent)
    return {
        'fulfillmentText':fulfillment_text
            }
    

if __name__ == '__main__':
    app.run(debug=True,port=8080)
