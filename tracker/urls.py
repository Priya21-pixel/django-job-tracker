

from django.urls import path
from . import views
from . import views as tracker_views

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('', views.job_list, name='job_list'),
    path('', tracker_views.dashboard, name='dashboard'), 
    path('register/', tracker_views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', tracker_views.dashboard, name='dashboard'),
    path('add/', views.add_job, name='add_job'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('export/', views.export_csv, name='export_csv'),


]

