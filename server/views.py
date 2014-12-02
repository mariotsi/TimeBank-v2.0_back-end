from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.template.defaultfilters import upper
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, list_route, detail_route
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
    permission_classes = (permissions.IsAdminUser,)

    # TODO change to IsAdmin in production
    def list(self, request):
        queryset = get_user_model().objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


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

    @list_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def login(self, request, *args):
        """
        Login endpoint
        ---
        # YAML (must be separated by `---`)

        omit_serializer: false
        serializer: server.serializers.UserSerializer

        parameters:
           - name: Authorization
             description: Basic HTTP authentication
             required: true
             type: string
             paramType: header

        responseMessages:
            - code: 200
              message: Correctly logged in
            - code: 401
              message: Invalid Authtentication
        """
        return Response(UserSerializer(request.user).data)

    @list_route(methods=['DELETE'], permission_classes=[IsAuthenticated])
    def logout(self, request, *args):
        """
        Logout endpoint
        ---
        # YAML (must be separated by `---`)

        omit_serializer: false
        serializer: server.serializers.ListingSerializer

        parameters:
           - name: Authorization
             description: Basic HTTP authentication
             required: true
             type: string
             paramType: header

        responseMessages:
            - code: 410
              message: Correctly logged out
            - code: 401
              message: Invalid Authtentication
        """
        return HttpResponse(status=410)

    @list_route(methods=['GET'], permission_classes=[IsAuthenticated])
    def my_profile(self, request, *args):
        """
        Return all mine listings plus ones that the user requested
        ---
        # YAML (must be separated by `---`)

        omit_serializer: false
        serializer: server.serializers.ListingSerializer

        parameters:
           - name: Authorization
             description: Basic HTTP authentication
             required: true
             type: string
             paramType: header

        responseMessages:
            - code: 200
              message: OK
            - code: 401
              message: Invalid Authtentication
        """
        return Response(ListingSerializer(Listing.objects.filter(Q(owner=request.user) | Q(applicant=request.user)),
                                          many=True).data)


class ListingViewSet(viewsets.ViewSet):
    """
    Basic viewset for Listing model
    """
    # queryset = Listing.objects.all()
    model = Listing
    serializer_class = ListingSerializer

    @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    def mine(self, request, *args, **kwargs):
        """
        Return all the listings owned by the current authenticated user
        ---
        omit_serializer: false
        serializer: server.serializers.ListingSerializer

        responseMessages:
           - code: 404
             message: The user does not own any listing
        """
        queryset = Listing.objects.filter(owner=request.user)
        if not queryset.exists():
            raise Http404
        return Response(ListingSerializer(queryset, many=True).data)

    def list(self, request, *args):
        """
        Return all the listings
        """
        queryset = Listing.objects.all()
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Return the listing with id=pk
        ---
        omit_serializer: false
        serializer: server.serializers.ListingSerializer

        responseMessages:
          - code: 404
            message: There is not a listing with given id
        """
        try:
            queryset = Listing.objects.all().get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if queryset is None:
            raise Http404
        return Response(ListingSerializer(queryset).data)

    @permission_classes((IsAuthenticated), )
    def create(self, request, *args):
        """
        Create a new listing and return it
        ---
        # YAML (must be separated by `---`)

        type:
            id:
                type: integer
                required: true
            creation_date:
                type: date
                required: true
            description:
                type: string
                required: true
            category:
                type: integer
                required: true
            applicant:
                type: integer
                required: true
            requested:
                type: boolean
                required: true

        omit_serializer: true

        parameters:
           - name: description
             required: true
             type: string
             paramType: form
           - name: category
             required: true
             type: integer
             paramType: form
           - name: Authorization
             description: Basic HTTP authentication
             required: true
             type: string
             paramType: header

        responseMessages:
            - code: 204
              message: Empty body request
        """
        if len(request.DATA) < 1:  # if there is no data within the request and send 204 "No content"
            return HttpResponse(status=204)
        listing_data = request.DATA
        new_listing = Listing(category=Category.objects.get(category_id=listing_data['category']),
                              description=listing_data['description'],
                              creation_date=datetime.now())
        new_listing.owner = request.user
        new_listing.save()
        return Response(ListingSerializer(new_listing).data)


    @permission_classes((IsAuthenticated), )
    def update(self, request, *args, **kwargs):
        """
        Update an existing listing and return it
        ---
        # YAML (must be separated by `---`)

        type:
            id:
                type: integer
                required: true
            creation_date:
                type: date
                required: true
            description:
                type: string
                required: true
            category:
                type: integer
                required: true
            applicant:
                type: integer
                required: true
            requested:
                type: boolean
                required: true

        omit_serializer: true

        parameters:
           - name: description
             required: true
             type: string
             paramType: form
           - name: category
             required: true
             type: integer
             paramType: form
           - name: Authorization
             description: Basic HTTP authentication
             required: true
             type: string
             paramType: header

        responseMessages:
            - code: 204
              message: Empty body request
            - code: 404
              message: There is not a listing with given id
            - code: 403
              message: The authenticated user is not the owner of that listing
        """
        try:
            listing = Listing.objects.all().get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if listing.owner != request.user:  # if the current user is not the owner abort and send 403 Forbidden
            return HttpResponse(status=403)
        if len(request.DATA) < 1:  # if there is no data within the request and send 204 "No content"
            return HttpResponse(status=204)
        category = request.DATA.get('category', None)
        description = request.DATA.get('description', None)
        if category is not None:
            listing.category_id = category
        if description is not None:
            listing.description = description
        listing.save()
        return Response(ListingSerializer(listing).data)

    @permission_classes((IsAuthenticated), )
    def destroy(self, request, *args, **kwargs):
        """
        Delete the listing with id=pk
        ---
        omit_serializer: false


        responseMessages:
          - code: 410
            message: Listing successfully deleted
          - code: 404
            message: There is not a listing with given id
          - code: 403
            message: The authenticated user is not the owner of that listing

        """
        try:
            listing = Listing.objects.all().get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if listing.owner != request.user:  # if the current user is not the owner abort and send 403 Forbidden
            return HttpResponse(status=403)  # Forbidden
        listing.delete()
        return HttpResponse(status=410)  # Gone

    @detail_route(methods=['PUT'], permission_classes=[IsAuthenticated])
    def claim(self, request, *args, **kwargs):
        """
        Claim the listing with id=pk
        ---
        omit_serializer: true


        responseMessages:
          - code: 201
            message: Successfully claimed
          - code: 404
            message: There is not a listing with given id
          - code: 403
            message: Listing's owner cannot claim it
          - code: 406
            message: Listing already claimed
        """
        try:
            listing = Listing.objects.all().get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if listing.owner == request.user:  # if the current user IS the owner abort and send 403 Forbidden
            return HttpResponse(status=403)
        if listing.requested:
            return HttpResponse(status=406)
        listing.requested = True
        listing.applicant = request.user
        listing.save()
        return HttpResponse(status=201)

    @detail_route(methods=['DELETE'], permission_classes=[IsAuthenticated])
    def unclaim(self, request, *args, **kwargs):
        """
        Unclaim the listing with id=pk
        ---
        omit_serializer: true


        responseMessages:
          - code: 410
            message: Successfully unclaimed
          - code: 404
            message: There is not a listing with given id
          - code: 403
            message: Current user is not the applicant OR the listing is not claimed
        """
        try:
            listing = Listing.objects.all().get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        # if the current user is not the applicant or the listing is not requested
        if listing.applicant != request.user or not listing.requested:
            return HttpResponse(status=403)
        listing.requested = False
        listing.applicant = None
        listing.save()
        return HttpResponse(status=410)

    @list_route(methods=['get'])
    def search(self, request, *args, **kwargs):
        """
        Filter non requested listings based on passed arguments.
        If no argument is passed all non requested listings are returned
        ---
        # YAML (must be separated by `---`)

        serializer: server.serializers.ListingSerializer

        omit_serializer: false

        parameters:
           - name: province
             required: false
             type: string(2)
             paramType: query
           - name: city
             required: false
             type: integer
             paramType: query
           - name: description
             required: false
             description: match is case insensitive and across all listing's description field
             type: string
             paramType: query
           - name: category
             required: false
             type: integer
             paramType: query

        responseMessages:
          - code: 204
            message: No listing match the current search terms

        """
        listings = Listing.objects
        listings = listings.filter(requested=False)
        province = request.QUERY_PARAMS.get('province', None)
        city = request.QUERY_PARAMS.get('city', None)
        description = request.QUERY_PARAMS.get('description', None)
        category = request.QUERY_PARAMS.get('category', None)
        if province is not None:
            listings = listings.filter(owner__city__province=upper(province))
        if city is not None:
            listings = listings.filter(owner__city=city)
        if description is not None:
            listings = listings.filter(description__icontains=description)
        if category is not None:
            listings = listings.filter(category_id=category)
        if len(listings) < 1:
            return HttpResponse(status=204)  # No Content
        return Response(ListingSerializer(listings, many=True).data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Basic viewset for Category model
    """
    queryset = Category.objects.all()
    model = Category
    permission_classes = (permissions.IsAuthenticated,)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Basic viewset for City model
    """
    paginate_by = 100
    queryset = City.objects.all()
    model = City
    permission_classes = (permissions.AllowAny,)

    @list_route(methods=['get'])
    def provinces(self, request, *args, **kwargs):
        """
        Get an ordered array with the abbreviation of all Italian Provinces
        """
        cities = City.objects.all()
        provinces = set([city.province for city in cities])
        return Response(sorted(provinces))

    @list_route(methods=['get'])
    def get_cities_by_province(self, request, *args, **kwargs):
        """
        Get an ordered array of all cities within given province
        ---
        # YAML (must be separated by `---`)

        type:
            name:
               required: true
               type: string
            id:
               required: true
               type: integer

        omit_serializer: false

        parameters:
            - name: province
             description: Province where cities are needed. Case insensitive
             required: true
             type: string(2)
             paramType: query

        responseMessages:
           - code: 400
             message: Province nonexistent

        """
        cities = City.objects.filter(province=upper(request.QUERY_PARAMS.get('province', None)))
        cities = ([[city.name, city.id] for city in cities])
        if len(cities) < 1:
            return HttpResponse(status=400, )  # Bad Request
        return Response(cities)