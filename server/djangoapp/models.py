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
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, review, purchase, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        #self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
        

    def __str__(self):
        return f"Review of Dealership {self.dealership} by {self.name} is {self.sentiment}"