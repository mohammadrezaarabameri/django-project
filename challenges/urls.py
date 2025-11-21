from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='users'),
    path('edit-profile', views.profile),
    path('edit-user', views.edit),
    path('<int:user>', views.dynamic_users, name='list_users'),
]