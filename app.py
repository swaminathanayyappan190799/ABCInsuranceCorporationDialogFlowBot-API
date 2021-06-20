# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 21:18:11 2021

@author: swaminathan.ayyappan
"""
from flask import Flask,request

app=Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    files=request.get_json(silent=True,force=True)
    fulfillment_text=''
    query_result=files.get("queryResult")
    intent=query_result.get("intent").get("displayName")
    parameters=query_result.get('parameters')
    if intent == 'PolicynumberGathering':
        policy_number=parameters.get('policynumber')
        fulfillment_text=str('Please verify your policy number which is '+str(policy_number))
    return {
        'fulfillmentText':fulfillment_text
            }

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
