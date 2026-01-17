from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static

def home_redirect(request):
    return redirect('users:login')



urlpatterns = [
    path('', home_redirect),   # ✅ ROOT URL FIX
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('ambulance/', include('ambulance.urls')),
     # ✅ ADD THIS LINE
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0]
    )
