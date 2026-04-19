from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('update-duration/<int:task_id>/', views.update_duration, name='update_duration'),
]