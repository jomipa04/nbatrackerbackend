from django.db import models

# Create your models here.
class Details(models.Model):
    michaelScore = models.IntegerField(default=0)
    michaelTeam= models.CharField(max_length=5)
    geoScore = models.IntegerField(default=0)
    geoTeam = models.CharField(max_length=5)

class Games(models.Model):
    date=models.DateField(auto_now_add=True )
    quit=models.BooleanField(default=False)
    winner=models.CharField(max_length=5)
    details = models.ForeignKey(Details, on_delete=models.CASCADE, related_name="details")


