from rest_framework import serializers
from .models import *

class CountrySerializer(serializers.Serializer):
    name=serializers.CharField(max_length=210)

    def create(self,validated_data):
        country_obj=Country(**validated_data)
        country_obj.save()
        return country_obj
    def update(self,instance,validated_data):
        instance.name=validated_data["name"]
        instance.save()
        return instance
    def get_all(self):
        country_list=[i  for i in Country.objects.all()]
        return country_list 
    def delete(self,validated_data):
        country_obj=Country(id=validated_data)
        country_obj.delete()
        return country_obj