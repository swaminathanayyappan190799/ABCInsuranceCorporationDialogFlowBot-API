# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 07:51:27 2021

@author: swaminathan.ayyappan
"""
from flask import Flask,request,make_response
from flask_cors import cross_origin
import json
#from pymongo import MongoClient

sample=Flask(__name__)

@sample.route('/webhook',methods=['POST'])
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
    #policynumber=parameters.get("PolicyNumber")
    if intent == 'PropertyNumberCollecting':
        policynumber=parameters.get("PolicyNumber")
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



if __name__ =="__main__":
    sample.run(port=5000,debug=True)