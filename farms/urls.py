from django.urls import path
from . import views

app_name = 'farms'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_crop, name='add_crop'),
    path('<int:crop_id>/', views.crop_detail, name='crop_detail'),
    path('<int:crop_id>/add-activity/', views.add_activity, name='add_activity'),
    path('<int:crop_id>/edit/', views.edit_crop, name='edit_crop'),
    path('<int:crop_id>/delete/', views.delete_crop, name='delete_crop'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('add-animal/', views.add_animal, name='add_animal'),
    path('animal/<int:animal_id>/', views.animal_detail, name='animal_detail'),
    path('animal/<int:animal_id>/add-activity/', views.add_animal_activity, name='add_animal_activity'),
    path('animal/<int:animal_id>/edit/', views.edit_animal, name='edit_animal'),
    path('animal/<int:animal_id>/delete/', views.delete_animal, name='delete_animal'),
    path('animal-task/<int:task_id>/complete/', views.complete_animal_task, name='complete_animal_task'),
    path('animal-task/<int:task_id>/delete/', views.delete_animal_task, name='delete_animal_task'),
    path('animals/<str:animal_type>/', views.animals_by_type, name='animals_by_type'),
    path('timeline/', views.timeline, name='timeline'),
]
