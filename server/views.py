from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from server.serializers import UserSerializer, ListingSerializer
from server.models import *
from rest_framework import permissions
from django.contrib.auth.models import User


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    Basic viewset for User model
    """
    queryset = get_user_model().objects.all()
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class ListingViewSet(viewsets.ModelViewSet):
    """
    Basic viewset for Listing model
    """
    queryset = Listing.objects.all()
    model = Listing
    serializer_class = ListingSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user


class UserListingsList(generics.ListAPIView):
    """
    This view return a list of all listings owned by
    the in the URL user.
    """
    serializer_class = ListingSerializer

    def get_queryset(self):
        queryset = Listing.objects.filter(owner=self.kwargs['username'])
        if not queryset.exists():
            raise Http404
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Basic viewset for Category model
    """
    queryset = Category.objects.all()
    model = Category
    permission_classes = (permissions.IsAdminUser,)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Basic viewset for City model
    """
    paginate_by = 100
    queryset = City.objects.all()
    model = City
    authentication_classes = (BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)