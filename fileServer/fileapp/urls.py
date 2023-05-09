from django.urls import path

from . import views

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path('download/<int:file_id>/',views.file_download,name='download'),
    # path('download/increment/<int:file_id>/',views.increment_downloads,name='increment_download'),
]