from django.db import models

# Create your models here.
class Trgovina(models.Model):
    Ime = models.CharField(max_length=200)

class Delavec(models.Model):
    Ime = models.CharField(max_length=200)
    Priimek = models.CharField(max_length=200)
    DatumRojstva = models.DateField()
    Spol = models.CharField(max_length=30)
    trgovina = models.ManyToManyField(Trgovina)
