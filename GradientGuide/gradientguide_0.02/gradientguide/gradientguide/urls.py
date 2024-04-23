"""gradientguide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from routeplanner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('routeplanner/', include('routeplanner.urls')),
    path('', views.home, name='home'),
    path('new/', views.session_input, name='session_input'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('show-map/', views.show_map, name='show-map'),
    path('past/', views.past_routes, name='past_routes'),
    path('profile/', views.user_profile, name='user_profile'),
    path('session/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    path('session/<int:session_id>/update/', views.edit_session, name='edit_session'),
    path('edit_session/<int:session_id>/', views.edit_session, name='edit_session'),

]
