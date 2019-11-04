from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
import jsonpickle
import ast

from rq import Queue
import django_rq

from .work import entry

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
    print("courses: " , inputs)

    # job = q.enqueue(work, term, inputs)
    job = django_rq.enqueue(entry, term)

    print("job id: " + job.id)
    print("job status: " + job.get_status())

    while(not job.result):
        print(job.get_status())

    print("job status: " + job.get_status())
    print(job.result)

    res = job.result
    # res = work(term, inputs)
    res_encoded = []
    # for courses in res:
    #     temp = []
    #     for course in courses:
    #         course_encoded = jsonpickle.encode(course, unpicklable=False)
    #         temp.append(ast.literal_eval(course_encoded))
    #     res_encoded.append(temp)

    # for courses in res_encoded:
    #     for course in courses:
    #         print(course)

    return Response(job.result)