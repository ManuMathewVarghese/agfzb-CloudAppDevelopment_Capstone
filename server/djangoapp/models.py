from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    def __str__(self):
        return f"Car make {self.name}"
        


class CarModel(models.Model):
    TYPE_CHOICES = [
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "WAGON")
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()
    def __str__(self):
        return f"Car Model {self.name}-{self.year} is a {self.type} sold by {self.dealer_id}"



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
