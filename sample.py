# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:46:18 2021

@author: swaminathan.ayyappan
"""

from flask import Flask,request
import os

sample=Flask(__name__)

@sample.route('/webhook',methods=['POST'])
def home():
    files=request.get_json(silent=True,force=True)
    fulfillment_text=''
    query_result=files.get("queryResult")
    intent=query_result.get("intent").get("displayName")
    if intent == 'PolicyIDCollection':
        policynumber=query_result.get("parameters").get("policynumber")
        fulfillment_text="The Policy Id you mentioned here is "+policynumber+" Is that one is correct ?"
    return {
        "fulfillmentText":str(fulfillment_text)
            }
"""
if __name__=="__main__":
    sample.run(debug=True)
        
"""
if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    app.run(debug=False, port=port, host='0.0.0.0')
