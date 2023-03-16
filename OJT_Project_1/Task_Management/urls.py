from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client_home', views.client_home, name='client_home'),
    path('client_pending', views.client_pending, name='client_pending'),
    path('accept-task/<int:task_id>/', views.accept_task, name='accept_task'),
    path('client_complete', views.client_complete, name='client_complete'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_pending', views.admin_pending, name='admin_pending'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('admin_complete', views.admin_complete, name='admin_complete'),
    path('admin_users', views.admin_users, name='admin_users'),
    path('add_user', views.add_user, name='add_user'),
    path('admin_add_task', views.admin_add_task, name='admin_add_task'),
    path('admin_edit', views.admin_edit, name='admin_edit'),
    path('category', views.category, name='category'),
    path('subcategory', views.subcategory, name='subcategory'),
    path('steps', views.steps, name='steps'),
    path('logout', views.logoutuser, name='logout'),

]
