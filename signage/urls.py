
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_user, name="login_user"),
    path("register", views.register_user, name="register_user"),
    path("logout", views.logout_user, name="logout_user"),
    path("host_inquiry", views.host_inquiry, name="host_inquiry"),
    path("advertiser_inquiry", views.ad_inquiry, name="advertiser_inquiry"),
    path("locations/<str:city_id>", views.fetch_locations, name="fetch_locations"),
    path("business_details/<str:business_id>", views.business_details, name="business_details"),
    path("plans/<str:advertiser_id>", views.plans, name="plans" ),
    path("success", views.success, name="success_view")

]
