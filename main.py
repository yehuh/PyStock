# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 22:08:07 2022

@author: yehuh
"""
import GetWorkedDay

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    real_work_day = GetWorkedDay.GetWorkedDay(5)
    
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return str(real_work_day[0])