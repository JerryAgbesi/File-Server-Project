from django.urls import path

from . import views

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path('download/<int:file_id>/',views.file_download,name='download'),
    path('search/',views.file_search,name='file_search'),
]