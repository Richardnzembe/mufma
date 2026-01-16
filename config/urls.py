from django.contrib import admin
from django.urls import path, include
from farms import views as farm_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # include accounts URLs with a namespace so templates can reverse
    # namespaced URLs like 'accounts:register'
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('', farm_views.home, name='home'),  # homepage
    path('farms/', include('farms.urls', namespace='farms')),
]
