from django.contrib import admin
from .models import PabblySubscription, User, Business, Location, Picture, CalculationSetting, City, Advertiser, Plan
# Register your models here.

admin.site.register(User)
admin.site.register(Business)
admin.site.register(Location)
admin.site.register(Picture)
admin.site.register(CalculationSetting)
admin.site.register(City)
admin.site.register(Advertiser)
admin.site.register(Plan)
admin.site.register(PabblySubscription)