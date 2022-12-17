
import json
from venv import create
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Advertiser, Business, CalculationSetting, Location, PabblySubscription, Picture, Plan, User, City
from django.db import IntegrityError
from django.http import JsonResponse

from django.contrib import messages
from .serializers import BusinessSerializer, LocationSerializer
from django.core.paginator import Paginator
from phonenumber_field.phonenumber import PhoneNumber
from .api import create_host_plan, fetch_plans_list, verify_hosted_page, fetch_all_subscriptions, revenue_report


# Create your views here.



def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_user'))
    return render(request, "signage/index.html")

def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Logged in!')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.add_message(request, messages.ERROR, 'User not found')
            return HttpResponseRedirect(reverse('login_user'))
    return render(request, "signage/login.html")


def register_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        if password != cpassword:
            return HttpResponseRedirect(reverse("register_user"))
        
        try:
            new_user = User.objects.create_user(email=email, username=email, password=password)
            new_user.save()
            messages.add_message(request, messages.SUCCESS, 'Signed up successfully!')
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError as e:
            messages.add_message(request, messages.ERROR, 'User with this email already exists')
            return HttpResponseRedirect(reverse("register_user"))

    return render(request, "signage/register.html")

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        
    return HttpResponseRedirect(reverse("login_user"))
 


def host_inquiry(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_user'))
    
    if request.method == "POST":

        business_name = request.POST.get("business_name")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email_address = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        notes = request.POST.get("notes")
        

        loop_length = request.POST.get("loop_length")
        city_id = request.POST.get("city_location")
        no_of_screens = request.POST.get("no_of_screens")
        min_avg_revenue = request.POST.get("min_avg_revenue")
        print(f"min_avg_revenue: {min_avg_revenue}")

        if no_of_screens  == "":
            no_of_screens = 0

        validated_phone_number = PhoneNumber.from_string(phone_number, region="US")

        try:

            new_business = Business(name=business_name, contact_name=f"{fname} {lname}", email=email_address, phone_number=validated_phone_number.as_e164, notes = notes, loop_length = loop_length, number_of_screens = no_of_screens, salesman=request.user)
            new_business.save()

            print(city_id)
            city = City.objects.all().first()
            print(city)
            location = Location(city=city, business=new_business)
            location.save()

            plan_name = f"{business_name} {city.name}"
            response = create_host_plan(plan_name, int(min_avg_revenue))

            if response["status"] == "success":
                new_plan = Plan(business=new_business, plan_id=response["data"]["id"])
                new_plan.save()
            else:
                messages.add_message(request, messages.ERROR, "Could not signup for an account on pabbly")
                return HttpResponseRedirect(reverse('host_inquiry'))
        except Exception as e:
            print(str(e))
            messages.add_message(request, messages.ERROR, str(e))
        messages.add_message(request, messages.SUCCESS, "Signed up successfully!")
        return HttpResponseRedirect(reverse('host_inquiry'))
    
    cities = City.objects.all()
    settings = CalculationSetting.objects.all().first()
    print(settings.base_cost)
    settings_json = {
        "base_cost": str(settings.base_cost),
        "percentage_increase": str(settings.percentage_increase)
    }
    return render(request, "signage/host_inquiry.html", {"cities": cities, "settings": json.dumps(settings_json)})

def ad_inquiry(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_user'))


    if request.method == "POST":
        business_name = request.POST.get("business_name")
        fname = request.POST.get("first_name")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("business_name")
        ad_length = request.POST.get("ad_length")
        

        selected_businesses = request.POST.get("selected_businesses")
        print(f"Selected businesses: {selected_businesses}")
        
        validated_phone_number = PhoneNumber.from_string(phone_number, region="US")
        try:
            new_ad = Advertiser(business_name=business_name, email=email, contact_name=f"{fname} {lname}", phone_number=validated_phone_number.as_e164, salesman=request.user, address=address, length_of_ad=int(ad_length))
            new_ad.save()

            business_ids = [int(i) for i in selected_businesses.split(',')]
            businesses = Business.objects.filter(id__in=business_ids)
            
            for b in businesses:
                new_ad.businesses.add(b)

            
            messages.add_message(request, messages.SUCCESS, "Advertiser signed up. Please sign up for a plan")
            return HttpResponseRedirect(reverse('plans', kwargs={"advertiser_id": new_ad.id}))


        except Exception as e:
            print(str(e))
            messages.add_message(request, messages.ERROR, "There was a problem signing up")
            return HttpResponseRedirect(reverse('advertiser_inquiry'))
        
    
    
    
    
    cities = City.objects.all()
    print(request.GET.get('city'))
    selected_city = request.GET.get('city')
    businesses = None
    if not selected_city:
        businesses = Business.objects.all()
    else:
        locations = Location.objects.filter(city__id=selected_city)
        print(locations)
    
        business_ids = []
        for loc in locations:
            business_ids.append(loc.business.id)

        businesses = Business.objects.filter(id__in=business_ids)
        print(businesses)

    paginator = Paginator(businesses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "signage/advertiser_inquiry.html", {"cities": cities, "page_obj": page_obj, "selected_city": selected_city})






def fetch_locations(request, city_id):
    print(city_id)
    locations = Location.objects.filter(city__id=city_id)
    print(locations)
    
    business_ids = []
    for loc in locations:
        business_ids.append(loc.business.id)

    businesses = Business.objects.filter(id__in=business_ids)
    print(businesses)

    business_serializer = BusinessSerializer(businesses, many=True)
    return JsonResponse({"businesses": business_serializer.data})


def business_details(request, business_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_user'))
    business = Business.objects.filter(id=business_id).first()
    images = Picture.objects.filter(business__id=business_id)
    locations = Location.objects.filter(business__id=business_id)
    
    return render(request, "signage/business_details.html", {"business": business, "images": images, "locations": locations})

def plans(request, advertiser_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_user'))
    advertiser = Advertiser.objects.filter(id=advertiser_id).first()
    business_ids = [ b.id for b in advertiser.businesses.all()]
    print(business_ids)
    plan_records = Plan.objects.filter(business__id__in=business_ids)
    print(plan_records)
    plan_ids = [ plan.plan_id for plan in plan_records  ]
    print(plan_ids)
    result = fetch_plans_list()
    relevant_plans = []
    for r in result["data"]:
        if r["id"] in plan_ids:
            relevant_plans.append(r)

    print(relevant_plans)
    request.session["advertiser_id"] = advertiser_id
    print(f"session set: ")
    return render(request, "signage/plans.html", {"plans":relevant_plans})

def success(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_user'))
    hostedpage = request.GET.get('hostedpage')

    if hostedpage:
        result = verify_hosted_page(hostedpage)


        subscription_id = result["data"]["id"]
        plan_id = result["data"]["plan_id"]
        customer_id = result["data"]["customer_id"]

        plan = Plan.objects.filter(plan_id=plan_id).first()

        advertiser_id = request.session.get('advertiser_id')

        print(f"Session: {advertiser_id}")

        
        if advertiser_id:
            del request.session["advertiser_id"]
            advertiser = Advertiser.objects.filter(id=advertiser_id).first()
            ps = PabblySubscription(subscription_id=subscription_id, customer_id=customer_id, plan=plan, advertiser=advertiser)
            ps.save()

        return render(request, 'signage/success.html', {"plan": {"name": result["data"]["plan"]["plan_name"]}})
    return render(request, 'signage/success.html')


def display_report(request):
    plans = fetch_all_subscriptions()
    revenue_report()

    # print(plans)
    # for plan in plans:
    #     print(plan)
    return render(request, "signage/report.html", {"data": plans})
    

