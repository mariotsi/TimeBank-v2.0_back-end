from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from server.models import *


class UserViewSet(viewsets.ModelViewSet):
    """
    Basic viewset for User model
    """
    queryset = User.objects.all()
    model = User


class ListingViewSet(viewsets.ModelViewSet):
    """
    Basic viewset for Listing model
    """
    queryset = Listing.objects.all()
    model = Listing


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Basic viewset for Category model
    """
    queryset = Category.objects.all()
    model = Category


class CityViewSet(viewsets.ModelViewSet):
    """
    Basic viewset for City model
    """
    queryset = City.objects.all()
    model = City