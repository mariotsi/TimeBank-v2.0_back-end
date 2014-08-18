from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework import routers
from server import views


admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'listings', views.ListingViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'cites', views.CategoryViewSet)

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include(router.urls))
)