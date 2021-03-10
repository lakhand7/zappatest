from django.shortcuts import render

# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
# from rest_framework.permissions import IsAunthenticated
import json

import pandas as pd
import warnings
import operator
warnings.filterwarnings('ignore')
from MyApp.Recommendation_Output import *


class users(APIView):

    def get(self):
        pass

    @api_view(["POST"])
    def covers(request):
        try:
            manuf_name = request.data.get('manuf_name')
            model_name = request.data.get('model_name')
            Rto = request.data.get('Rto')
            Age = int(request.data.get('Age'))
            PRODUCT = request.data.get('PRODUCT')

            recommended_covers, telematics_covers = recommendation.func_recom(manuf_name, model_name, Rto, Age, PRODUCT)
            #dt={"fir":1,"sec":2}
            dt={"Recommended_Plan":recommended_covers, "Telematics_plan":telematics_covers}

            return JsonResponse(dt, safe = False)

        except ValueError as e:
            return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
    
