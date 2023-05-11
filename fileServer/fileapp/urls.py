from django.urls import path

from . import views

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path('download/<int:file_id>/',views.file_download,name='download'),
    path('search/',views.file_search,name='file_search'),
    path('email_form/<int:file_id>/',views.email_form,name='email_form'),
    path('send_mail/<int:file_id>',views.send_mail,name='send_mail'),
    path('files/<int:file_id>/preview/',views.preview_file,name='preview_file'),

]