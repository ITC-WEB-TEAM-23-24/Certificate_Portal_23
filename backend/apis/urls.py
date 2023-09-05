from django.urls import path
from . import views 

urlpatterns = [
    path('userdata',views.posts),
    path('kritika/<str:rollno>',views.kritika_check),
    path('kritika/download/<str:rollno>',views.download_certificate),
]