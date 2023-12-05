from django.urls import path

from . import views

app_name='encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    #path("update/", views.update, name="update"),
    path("open/", views.open, name="open"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path('click_entry/',views.click_entry,name='click_entry'),
    path("new_entry/",views.new_entry,name="new_entry"),
    path('random_page/',views.random_page,name='random_page')
]
