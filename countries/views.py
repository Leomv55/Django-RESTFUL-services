from django.shortcuts import render
from django.http import HttpResponse
from countries.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from rest_framework import status

import json
# Create your views here.

@api_view(['POST'])
def add_country(request):
    country_serializer=CountrySerializer(data=request.data)
    if country_serializer.is_valid():
        country_serializer.save()
        return HttpResponse(json.dumps([{ 'data' :"Country added successfully"}]),status=status.HTTP_201_CREATED,content_type='application/json')
    else:
        error_details=[]
        for k in country_serializer.errors.keys():
            error_details.append({"field":k,"message":country_serializer.errors[k][0]})
            data={
                "Error":{
                    "status":400,
                    "message":"You submitted data not vaild-check the stacktrace",
                    "error_details":error_details
                }
            }
        return Response(data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
def update_country(request,id):
    if request.method == 'GET':
        try:
            country_obj=Country.objects.get(id=id)
            country_data=CountrySerializer(country_obj).data
            return HttpResponse(json.dumps(
            [{
                "data":country_data
            }]
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
            )
        except:
            country_data=""
            return HttpResponse(json.dumps([
            {
                "data":{
                    'name':"Country not found"
                }
            }]
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
            )
    elif request.method == 'DELETE':
        try:
            # country_obj=Country.objects.get(id=id)
            # country_obj.delete()
            country_obj=CountrySerializer().delete(validated_data=id)
            country_obj.delete()
            return HttpResponse(json.dumps([{
                "data":"Country deleted succesfully"
            }
            ]),content_type="application/json")
        except:
            return HttpResponse(
                json.dumps(
                    [{
                        "data":"Country not found"
                    }]
                ),
                content_type="application/json"
            )
@api_view(['GET'])
def all_countries(request):
    country_list=CountrySerializer().get_all()
    cl=[]
    for i in range(0,len(country_list)):
        c_dict={}
        c_dict["name"]=country_list[i].name
        cl.append(c_dict)
    return HttpResponse(json.dumps(cl),content_type="application/json")
