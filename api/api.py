from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
import jsonpickle
import ast

from rq import Queue
from rq.job import Job
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
    job_id = params["job_id"]

    inputs = inputs.split(',')

    print("term: " , term)
    print("courses: " , inputs)

    if job_id:
        print("job already in queue")
        redis_conn = django_rq.get_connection('default')
        job = Job.fetch(job_id, connection=redis_conn)
        print("fetched job")

    else:
        print("create new job")
        job = django_rq.enqueue(entry, term, inputs)
        print("job id: " + job.id)

    if (job.result):
        res = job.result
        res_encoded = []
        for courses in res:
            temp = []
            for course in courses:
                course_encoded = jsonpickle.encode(course, unpicklable=False)
                temp.append(ast.literal_eval(course_encoded))
            res_encoded.append(temp)

        data = {
            'status': 'success',
            'data': res_encoded
        }

        return Response(data)
    
    data = {
        'status': 'processing',
        'job_id': job.id
    }

    return JsonResponse(data)

