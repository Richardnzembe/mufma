from django.urls import path
from . import views

# register the application namespace so templates can use the
# namespaced URL form: {% url 'accounts:register' %}
app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
