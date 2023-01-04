from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path("", views.index, name='index'),
    path('get', views.get_api),
    path('post', views.search),
    path('update', views.update_db)
]
