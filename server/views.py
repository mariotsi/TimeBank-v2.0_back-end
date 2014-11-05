from datetime import datetime

from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions

from server.serializers import UserSerializer, ListingSerializer
from server.models import *



# Create your views here.
class UserViewSet(viewsets.ViewSet):
    """
    Basic viewset for User model
    """

    model = get_user_model()
    # serializer_class = UserSerializer
    # permission_classes = (permissions.IsAdminUser,)

    @permission_classes((IsAuthenticated), )
    def list(self, request):
        queryset = get_user_model().objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @permission_classes((IsAuthenticated), )
    def update(self, request, *args, **kwargs):
        # one = get_user_model().objects.all().filter(username__exact=kwargs['pk'])
        if request.user.username != get_user_model().objects.all().filter(username__exact=kwargs['pk']):
            raise PermissionError
        else:
            data = UserSerializer(JSONParser().parse(request.DATA))
            if data.is_valid():
                data.save()
            else:
                raise Http404


class ListingViewSet(viewsets.ViewSet):
    """
    Basic viewset for Listing model
    """
    # queryset = Listing.objects.all()
    model = Listing
    serializer_class = ListingSerializer

    def list(self, request, *args):
        queryset = Listing.objects.all()
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Listing.objects.all().get(id=kwargs['pk'])
        if queryset is None:
            raise Http404
        return Response(ListingSerializer(queryset).data)

    @permission_classes((IsAuthenticated), )
    def create(self, request, *args):
        listing_data = request.DATA
        new_listing = Listing(category=Category.objects.get(category_id=listing_data['category']),
                              description=listing_data['description'],
                              creation_date=datetime.now())
        new_listing.owner = request.user
        new_listing.save()
        return HttpResponse(status=201)

    @permission_classes((IsAuthenticated), )
    def update(self, request, *args, **kwargs):

        listing = Listing.objects.all().get(id=kwargs['pk'])
        if listing.owner != request.user:  # if the current user is not the owner abort and send 403 Forbidden
            return HttpResponse(status=403)  # Http404
        if len(request.DATA) < 1:  # if there is no data within the request and send 204 "No content"
            return HttpResponse(status=204)
        else:
            for key in ['category', 'description']:
                if key in request.DATA.keys():
                    if key == 'category':
                        listing.category = Category.objects.get(category_id=request.DATA['category'])
                    if key == 'description':
                        listing.description = request.DATA['description']
            listing.save()
            return HttpResponse(status=200)


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