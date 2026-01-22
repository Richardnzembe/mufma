from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from farms import views as farm_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # include accounts URLs with a namespace so templates can reverse
    # namespaced URLs like 'accounts:register'
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('', farm_views.home, name='home'),  # homepage
    path('farms/', include('farms.urls', namespace='farms')),
    # PWA service worker and offline fallback
    path('service-worker.js', TemplateView.as_view(template_name='service-worker.js', content_type='application/javascript'), name='service-worker.js'),
    path('offline/', farm_views.offline, name='offline'),
]

# Serve static files during development or when DEBUG=False for testing
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
