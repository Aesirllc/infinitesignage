
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



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
    path("success", views.success, name="success_view"),
    


    # Auth views
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='signage/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='signage/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='signage/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='signage/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='signage/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='signage/password_reset_complete.html'),
     name='password_reset_complete'),

]
