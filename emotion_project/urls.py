from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('facial/', include(('facial_emotion.urls', 'facial_emotion'), namespace='facial_emotion')),
    path('voice/', include(('voice_emotion.urls', 'voice_emotion'), namespace='voice_emotion')),
    path('recommendations/', include(('recommendations.urls', 'recommendations'), namespace='recommendations')),
    path('admin-panel/', include(('admin_panel.urls', 'admin_panel'), namespace='admin_panel')),
    path('dashboard/', include(('user_dashboard.urls', 'user_dashboard'), namespace='user_dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
