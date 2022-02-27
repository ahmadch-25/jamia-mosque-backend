from rest_framework import serializers
from .models import Duas, DuaCategory


class DuaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duas
        fields = ('zekr', 'reference')


class DuaCategorySerializer(serializers.ModelSerializer):
    duas = DuaSerializer(many=True)

    class Meta:
        model = DuaCategory
        fields = ['id', 'category', 'duas', ]
