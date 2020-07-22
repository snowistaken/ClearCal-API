from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Event, Shift, UserSubClass
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

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
        print(request.data)
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
