from django.urls import path
from . import views 

urlpatterns = [
    path('userdata',views.posts),
    
    path('ksp/<str:rollno>',views.ksp_check),
    path('ksp/download/<str:rollno>',views.download_certificate),

    path('soc/<str:rollno>',views.soc_check),
    path('soc/download/<str:rollno>',views.download_certificate),

    path('sos/<str:rollno>',views.sos_check),
    path('sos/download/<str:rollno>',views.download_certificate),

    # path('itsp/<str:rollno>',views.itsp_check),
    # path('itsp/download/<str:rollno>',views.download_certificate),

    # path('tss/<str:projectname>/<str:rollno>',views.tss_check),
    # path('download/tss/<str:projectname>/<str:rollno>',views.download_certificate),

    path('ls/<str:rollno>',views.ls_check),
    path('download/ntss/<str:rollno>',views.download_certificates_ntss),

    path('ntss/<str:rollno>',views.ls_check),
    path('download/tss/<str:rollno>',views.download_certificates_tss),
]