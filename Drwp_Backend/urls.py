from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
admin.site.site_header = "Drwp"
admin.site.site_title = "Drwp"
admin.site.index_title = "Drwp-Admin"


schema_view = get_schema_view(
   openapi.Info(
      title="Drwp API",
      default_version='v1',
      description="Api documentation for Drwp",
      terms_of_service="https://www.drwp.com/policies/terms/",
      contact=openapi.Contact(email="isaack.bsmith@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls',)),
    path('api/drwp/', include('drwp.api.urls',)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



