from django.http import HttpResponse, JsonResponse
import json
import os
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
import sys, imp
import numpy as  np

sys.path.append('E:\\project\\2021_Project\\AlgorithmPythonWeb\\xmodule\\')
sys.path.append('E:\\project\\2021_Project\\AlgorithmPythonWeb\\log\\')
scriptPath = 'E:\\project\\2021_Project\\AlgorithmPythonWeb\\customize\\'
sys.path.append(scriptPath)

import logconfig

logconfig.log_init()

import dmc, pid


def test(request):
    if (request.method == 'POST'):
        print('body=%s', request.body)
        out = {'data': {}, 'msg': '', 'status': 200}
        return JsonResponse(out)
    else:

        context = {}


def load(module_name, module_path):
    '''使用imp的两个函数find_module，load_module来实现动态调用Python脚本。如果发现异常，需要解除对文件的占用'''
    fp, pathname, description = imp.find_module(module_name, [module_path])
    try:
        return imp.load_module(module_name, fp, pathname, description)
    finally:
        if fp:
            fp.close()

def narrayConvert(value):
        return value.tolist() if type(value) == np.ndarray else value

def listConvert(value):
        return np.array(value) if type(value) == list else value


def contrl_dmc(request):
    try:
        requestdata = json.loads(request.body)

        input_data = requestdata['input']
        context = requestdata['context']
        data = dmc.main(input_data, context)
        resp = {'data': data, 'context': context, 'msg': '', 'status': 200}
        return JsonResponse(resp)
    except Exception as e:
        logging.error('%s' % traceback.format_exc())
        return JsonResponse({'msg': '%s' % traceback.format_exc(), 'status': 123456})


def contrl_pid(request):
    try:
        requestdata = json.loads(request.body)
        input_data = requestdata['input']
        context = requestdata['context']
        data = pid.main(input_data, context)
        resp = {'data': data, 'context': context, 'msg': '', 'status': 200}
        return JsonResponse(resp)
    except Exception as e:
        logging.error(e)
        return JsonResponse({'msg': '%s' % traceback.format_exc(), 'status': 123456})


def contrl_customize(request):
    try:
        requestdata = json.loads(request.body)

        modelId = requestdata['modelId']
        input_data = requestdata['input']
        context = requestdata['context']
        scriptcontext = requestdata['pythoncontext']
        # 文件存储
        pyFile = open("%s.py" % modelId, "w+")
        try:
            pyFile.write(scriptcontext)
            pyFile.flush()
        finally:
            if pyFile:
                pyFile.close()

        do = load(modelId, scriptPath)
        result = do.main(input_data, context)
        for key,value in context.items():
            context[key]=narrayConvert(value)
        resp = {'data': result, 'context': context, 'msg': '', 'status': 200}
        return JsonResponse(resp)
    except Exception as e:
        logging.error(e)
        return JsonResponse({'msg': '%s' % traceback.format_exc(), 'status': 123456})
