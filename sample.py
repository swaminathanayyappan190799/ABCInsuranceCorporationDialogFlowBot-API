# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:46:18 2021

@author: swaminathan.ayyappan
"""

from flask import Flask,request

sample=Flask(__name__)

@sample.route('/webhook',methods=['POST'])
def home():
    files=request.get_json(silent=True,force=True)
    #fulfillment_text=''
    query_result=files.get("queryResult")
    intent=query_result.get("intent").get("displayName")
    if intent == 'PolicyIDCollection':
        policynumber=query_result.get("parameters").get("policynumber")
    return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "The Policy Id you mentioned here is: "+policynumber
                        ]

                    }
                },
                {
                    "text": {
                        "text": [
                            "Is that policy number is correct ?"
                        ]

                    }
                }
            ]
        }
""""
if __name__=="__main__":
    sample.run(debug=True)
        
"""
if __name__=="__main__":
    sample.run(host='0.0.0.0',port=8080)
