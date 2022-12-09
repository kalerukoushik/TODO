from django.urls import path
from . import views

app_name = "todo_app"
urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.index, name="index"),
    path('mark_complete_or_incomplete/<str:pk>/', 
        views.mark_complete_or_incomplete, name='mark_complete_or_incomplete'),
    path('add_task/', views.add_task, name='add_task'),
    path('update_task/<str:pk>', views.update_task, name='update_task'),
    path('delete_task/<str:pk>', views.delete_task, name='delete_task'),
]