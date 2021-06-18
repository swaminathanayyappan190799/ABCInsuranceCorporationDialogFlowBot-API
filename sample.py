# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:46:18 2021

@author: swaminathan.ayyappan
"""

from flask import Flask,request

sample=Flask(__name__)

@sample.route('/webhook',methods=['POST'])
def webhook():
    files=request.get_json(silent=True,force=True)
    query_result=files.get("queryResult")
    #intent=query_result.get("intent").get("displayName")
    if query_result.get('action')=='WelcomeIntent.WelcomeIntent-yes.ReportingPropertyClaim-custom':
        policynumber=str(query_result.get("parameters").get("policynumber"))
        print(policynumber)
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

"""
if __name__=="__main__":
    sample.run(debug=True)
        
"""
if __name__=="__main__":
    sample.run(host='0.0.0.0',port=8080)

