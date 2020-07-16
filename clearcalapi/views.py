from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import *
from .serializers import *


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (AllowAny)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update an event with this route'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create an event with this route'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.obects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['POST'])
    def create_event(self, request):
        if 'event' in request.data:
            user = request.user
            title = request.data.event['title']

            try:
                event = Event.objects.get(user=user.id, title=title)

                event.title = title
                event.description = request.data.event['description']
                event.all_day = request.data.event['all_day']
                event.start = request.data.event['start']
                event.end = request.data.event['end']
                event.save()

                # check tutorial and see what is needed for the argument here
                serializer = EventSerializer( , many=False)
                response = {'message': 'Event updated successfully', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                event = Event.objects.create(
                    title = title,
                    description = request.data.event['description'],
                    all_day = request.data.event['all_day'],
                    start = request.data.event['start'],
                    end = request.data.event['end'],
                    organizer = user
                )

                serializer = EventSerializer( , many=False)
                response = {'message': 'Event created successfully', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'Event must be provided'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
