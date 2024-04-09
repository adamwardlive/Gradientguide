from django.urls import include, path
from . import views

urlpatterns = [
    path('new/', views.session_input, name='session_input'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('show-map/', views.show_map, name='show-map'),
]
