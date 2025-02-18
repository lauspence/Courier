"""
URL configuration for CourierMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

  
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('customer/', views.customer_registration, name='customer_registration'),
    path('register/', views.customer_registration, name='customer_registration'),
    # path('courier/', views.courier_page),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('create-job/', views.create_job, name='create_job'),
    path('job-list/', views.job_list, name='job-list'),
    path('customer/job/<int:job_id>/', views.job_details, name='job_detail'),
    path('create-customer-profile/', views.create_customer_profile, name='create-customer-profile'),
    path('courier/dashboard/', views.courier_dashboard, name='courier_dashboard'),  # Uncomment this
    path('accept-job/<int:job_id>/', views.accept_job, name='accept_job'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path("courier/login/", views.courier_login, name="courier_login"),
    path('courier/register/', views.courier_registration, name='courier_registration'),
    path('profile-creation/', views.profile_creation, name='profile_creation'),
    path('update-job-status/<int:job_id>/<str:new_status>/', views.update_job_status, name='update_job_status'),
    path('get-job-status/<int:job_id>/', views.get_job_status, name='get_job_status'),
    path('accept-job/<int:job_id>/', views.customer_accept_job, name='customer_accept_job'),
    path('start-delivery/<int:job_id>/', views.start_delivery, name='start_delivery'),
    path('courier/delivery-history/', views.courier_delivery_history, name='courier_delivery_history'),
    path('customer/jobs/', views.customer_job_list, name='customer_job_list'),
    path('courier/jobs/', views.courier_job_list, name='courier_job_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
