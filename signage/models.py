from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField






class User(AbstractUser):
    pass



class Business(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField()
    contact_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=False)
    loop_length = models.IntegerField(default=0)
    number_of_screens = models.IntegerField(default=0)
    notes = models.TextField()
    salesman = models.ForeignKey(User, on_delete=models.CASCADE, related_name="businesses")
    logo = models.ImageField(upload_to = "logos", blank=True, default="logos/business_default_logo.png")

    class Meta:
        verbose_name_plural = "businesses"
    def __str__(self):
        return f"{self.name}"

class City(models.Model):
    name = models.CharField(max_length=20)
    population = models.BigIntegerField()

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return f"{self.name}  | {self.population}"
        
class Location(models.Model):
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="locations")
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="locations")


    def __str__(self):
        return f"{self.business.name}, {self.address}"

class Picture(models.Model):
    name = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to = "BusinessPictures", blank=False, default="BusinessPictures/business_default.png")
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="pictures")


    def __str__(self):
        return f"{self.name},  {self.business}"



class CalculationSetting(models.Model):
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_increase = models.IntegerField()

    def __str__(self):
        return f"{self.base_cost},  {self.percentage_increase}"


class Advertiser(models.Model):
    business_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField()
    contact_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=False)
    salesman = models.ForeignKey(User, on_delete=models.CASCADE, related_name="advertisers")
    address = address = models.TextField()

    businesses = models.ManyToManyField(Business) 
    length_of_ad = models.IntegerField(default=0)
   

    def __str__(self):
        return f"{self.business_name}"

class Plan(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="plans")
    plan_id = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business}"

class PabblySubscription(models.Model):
    subscription_id = models.CharField(max_length=150)
    customer_id = models.CharField(max_length=150)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="subscriptions")
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name="subscriptions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.advertiser.business_name} | {self.plan.business.name}"

