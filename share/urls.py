# Module 0
from django.urls import path, include
from . import views  #import everything from views module
app_name = 'share'
urlpatterns = [
    path('',views.index, name='index'), #Module 0
    # path('first_script', views.get_first_script, name='first_script'), # Module 1

    path('signup',views.signup, name='signup'),
    path('create',views.create, name='create'),

    path('login',views.login_view, name='login'),
    path('loguser',views.login_user,name='loguser'),

    path('logout',views.logout_view, name='logout'),

    path('dashboard', views.dashboard, name='dashboard'),

    # Problems
    path('publish_problem', views.publish_problem, name='publish_problem'),
    path('problem/<int:problem_id>/show', views.show_problem, name='show_problem'),
    path('problem/<int:problem_id>/show_my_problem', views.show_my_problem, name='show_my_problem'),



    # scripts
    path('script/<int:script_id>/show_my_script', views.show_my_script, name='show_my_script'),
    path('script/<int:script_id>/show', views.show_script, name='show_script'),

    # edit
    path('problem/<int:problem_id>/edit', views.edit_problem,  name='edit_problem'),
    path('script/<int:script_id>/edit', views.edit_script, name='edit_script'),

]
