# Module 0
from django.urls import path, include
from . import views  #import everything from views module
app_name = 'share'
urlpatterns = [
    path('',views.index, name='index'), #Module 0
    path('first_script', views.get_first_script, name='first_script'), # Module 1

    path('signup',views.signup, name='signup'),
    path('create',views.create, name='create'),

    path('login',views.login_view, name='login'),
    path('loguser',views.login_user,name='loguser'),

    path('logout',views.logout_view, name='logout'),

    path('dashboard', views.dashboard_view, name='dashboard'),
    path('publish_problem', views.publish_problem, name='publish_problem'),


]
