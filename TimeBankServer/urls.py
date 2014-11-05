from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from server import views


admin.autodiscover()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
router.register(r'listings', views.ListingViewSet)

router.register(r'categories', views.CategoryViewSet)
router.register(r'cities', views.CityViewSet)

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^listings/user/(?P<username>.+)/$', views.UserListingsList.as_view()),
                       url(r'^', include(router.urls)),

                       )
urlpatterns += patterns('',
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                        )
