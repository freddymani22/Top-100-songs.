from django.db import models


# Create your models here.
class BillBoard(models.Model):
    id = models.IntegerField(primary_key=True)
    date= models.DateField()
    rank=models.IntegerField()
    song =models.CharField(max_length=50)
    artist =models.CharField(max_length=50)
    last_week=models.IntegerField()
    peak_rank=models.IntegerField()
    weeks_on_board=models.IntegerField()




