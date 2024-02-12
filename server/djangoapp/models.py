from django.db import models
from django.utils.timezone import now


# Create your models here.



# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
# - Any other fields you would like to include in car make model
    founders = models.CharField(max_length=200)
    country_of_origin = models.CharField(max_length=100)
# - __str__ method to print a car make object
    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()  # Refers to a dealer created in Cloudant database
    name = models.CharField(max_length=100)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    car_type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES, default=SEDAN)
    year = models.DateField()
# - __str__ method to print a car make object
    def __str__(self):
        return f"{self.name} ({self.car_make.name})"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
