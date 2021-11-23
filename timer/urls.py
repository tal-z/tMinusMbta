# timer/urls.py
from . import views as timer_views
from users import views as user_views
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    path('', timer_views.index, name='timer'),
    path('CreateTimer/', timer_views.create_timer, name='create_timer'),
    path('NewTimer/', timer_views.new_timer, name='new_timer'),
    path('add_timer/', user_views.add_timer, name='add_timer'),
    #path('NewTimer/_update_timer/<str:tmr>/', views._update_timer, name='update_timer'), # DEPRECATED VIEW
]