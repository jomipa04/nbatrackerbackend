from rest_framework import serializers
from .models import  Games, Details



class DetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Details
    fields = ['id','michaelScore','michaelTeam','geoScore','geoTeam']
  
class GamesSerializer(serializers.ModelSerializer):
  details = DetailsSerializer()
  class Meta:
    model = Games
    fields=['id','date','quit','winner','details']

  def create(self, validated_data):
    details_data = validated_data.pop('details')
    details = Details.objects.create(**details_data)
    game= Games.objects.create(details=details, **validated_data)
    # print(game)
    return game
  