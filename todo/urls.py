from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='homedef'),
    path('<int:view_mode>/', views.home, name='home'),
    path('signup/', views.signupuser, name='signupuser'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('create/', views.create_todo, name='createtodo'),
    path('show/<int:todo_pk>', views.showtodo, name='showtodo'),
    path('setcomplete/<int:todo_pk>', views.setcomplete, name='set_as_complete'),
    path('deleterecord/<int:todo_pk>', views.delete_record, name='deleterecord'),
]

