from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
import jsonpickle
import ast

from .main import main

@api_view(['GET'])
def schedules(request):

    # AT LEAST 2 Courses
    # inputs = ['CMPUT174', 'ECON281']
    # term = '1690 - Fall Term 2019' 

    params = request.query_params.dict()
    term = params["term"]
    inputs = params["courses"]
    inputs = inputs.split(',')

    print("term: " , term)

    res = main(term, inputs)
    res_encoded = []
    for courses in res:
        temp = []
        for course in courses:
            course_encoded = jsonpickle.encode(course, unpicklable=False)
            temp.append(ast.literal_eval(course_encoded))
        res_encoded.append(temp)

    # for courses in res_encoded:
    #     for course in courses:
    #         print(course)

    return Response(res_encoded)