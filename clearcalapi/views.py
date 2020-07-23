from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Event, Shift, UserSubClass
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import *


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        response = {'message': 'This request is not permitted'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['GET'])
    def get_events(self, request, pk=None):
        user = request.user
        events = Event.objects.filter(organizer=user.id)

        if len(events) > 0:
            serializer = EventSerializer(events, many=True)
            response = {'message': 'Events acquired successfully', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'There are no events for this user', 'result': []}
            return Response(response, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['POST'])
    # def create_event(self, request, pk=None):
    #     if 'title' in request.data:
    #         user = request.user
    #         title = request.data['title']
    #         event = Event.objects.get(id=request.data['id'])
    #
    #         try:
    #             event.title = title
    #             event.description = request.data.description
    #             event.all_day = request.data['all_day']
    #             event.start = request.data['start']
    #             event.end = request.data['end']
    #             event.save()
    #             print(event)
    #
    #             serializer = EventSerializer(event, many=False)
    #             response = {'message': 'Event updated successfully', 'result': serializer.data}
    #             return Response(response, status=status.HTTP_200_OK)
    #         except:
    #             event = Event.objects.create(
    #                 title=title,
    #                 description=request.data.description,
    #                 all_day=request.data['all_day'],
    #                 start=request.data['start'],
    #                 end=request.data['end'],
    #                 organizer=user
    #             )
    #
    #             serializer = EventSerializer(event, many=False)
    #             response = {'message': 'Event created successfully', 'result': serializer.data}
    #             return Response(response, status=status.HTTP_200_OK)
    #
    #     else:
    #         response = {'message': 'Event must be provided'}
    #         return Response(response, status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):

        try:
            last_char = len(request.headers['Authorization'])
            user = Token.objects.get(key=request.headers['Authorization'][6:last_char]).user
            if not request.headers['Authorization']:
                response = {'message': 'You must be logged in to perform this action'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            elif str(user.id) != request.data['organizer']:
                response = {'message': 'Event does not belong to user'}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            response = {'message': 'Authorization must be provided for this request'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        try:
            user = Token.objects.get(key=request.headers['Authorization']).user
            if not request.headers['Authorization']:
                response = {'message': 'You must be logged in to perform this action'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            elif user.id != request.data['organizer']:
                response = {'message': 'Event does not belong to this user'}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            response = {'message': 'Authorization must be provided for this request'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def create(self, request, *args, **kwargs):
        if not request.headers['Authorization']:
            response = {'message': 'You must be logged in to perform this action'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}






    # def update(self, request, *args, **kwargs):
    #     response = {'message': 'You cant update an event with this route'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
    #
    # def create(self, request, *args, **kwargs):
    #     response = {'message': 'You cant create an event with this route'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


# class UserSubClassViewSet(viewsets.ModelViewSet):
#     queryset = UserSubClass.objects.all()
#     serializer_class = UserSubClassSerializer
#     permission_classes = (AllowAny, )


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = (AllowAny, )
