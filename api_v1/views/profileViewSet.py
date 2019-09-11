from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from api_v1.serializers import AdminSerializer
from api_v1.serializers import AuthorSerializer
from api_v1.serializers import SubscriberSerializer
from api_v1.serializers import SubscriptionSerializer
from home.models import AppUser


class ProfileViewSet(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users view and edit their profile data.
    """
    #: extra context passed for the view
    extra_context = None
    #: permissions for the view
    permission_classes = [
        IsAuthenticated,
    ]
    
    def get_context_data(self, filter=None):
        """
        Function to return context data for the view.
        """
        data = self.extra_context

        if filter:
            try:
                data = self.extra_context[filter]
            except Exception as e:
                data = None

        return data
    
    def get_object(self):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        page = self.get_context_data('page')
        obj = None
        
        group_data = {
            'groups': [],
        }

        if page == 'profile_author' or page == None:
            try:
                obj = self.request.user.author
                group_data['groups'].append(AppUser.AUTHOR)
            except ObjectDoesNotExist:
                pass

        if page == 'profile_admin' or page == None:
            try:
                obj = self.request.user.admin
                group_data['groups'].append(AppUser.ADMIN)
            except ObjectDoesNotExist:
                pass

        if page == 'profile_subscriber' or page == None:
            try:
                obj = self.request.user.subscriber
                group_data['groups'].append(AppUser.SUBSCRIBER)
            except ObjectDoesNotExist:
                pass

        # return group_data for SubscriptionSerializer
        if page == None:
            obj = group_data
            
        # throw NotFound if obj is None
        if obj is None:
            raise NotFound('Profile data does not exist')

        return obj
        
    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        page = self.get_context_data('page')
        serializer_class = None

        if page == 'profile_author':
            try:
                self.request.user.author
                serializer_class = AuthorSerializer
            except ObjectDoesNotExist:
                pass

        if page == 'profile_admin':
            try:
                self.request.user.admin
                serializer_class = AdminSerializer
            except ObjectDoesNotExist:
                pass

        if page == 'profile_subscriber':
            try:
                self.request.user.subscriber
                serializer_class = SubscriberSerializer
            except ObjectDoesNotExist:
                pass

        if page == None:
            serializer_class = SubscriptionSerializer

        # throw NotFound if serializer_class is None
        if serializer_class is None:
            raise NotFound('Profile data does not exist')

        return serializer_class
    
    def perform_update(self, serializer):
        """
        Update the existing AppUser instance.
        """
        response_data = None
        status_code = status.HTTP_200_OK

        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
        else:
            response_data = serializer.errors
            status_code = status.HTTP_404_NOT_FOUND

        return {
            'data': response_data,
            'status': status_code
        }

    def retrieve(self, *args, **kwargs):
        """
        Retrieve the user profile, An instance of AppUser model.
        """
        obj = self.get_object()
        serializer_class = self.get_serializer_class()        
        
        # get the AppUser instance from serializer
        instance = serializer_class(
            obj,
            context={'request': self.request}
        )

        return Response(instance.data)

    def update(self, *args, **kwargs):
        """
        Edit the user profile.
        """
        obj = self.get_object()
        serializer_class = self.get_serializer_class()
        
        # get the AppUser instance from serializer
        page = self.get_context_data('page')
        if page == None:
            instance = serializer_class(
                obj,
                data=self.request.data,
                context={'request': self.request},
            )

        else:
            instance = serializer_class(
                obj,
                exclude={'user'},
                data=self.request.data,
                context={'request': self.request},
            )
        
        # update and return
        update = self.perform_update(instance)
        return Response(update['data'], status=update['status'])
        
    def partial_update(self, *args, **kwargs):
        obj = self.get_object()
        serializer_class = self.get_serializer_class()

        # get the AppUser instance from serializer
        page = self.get_context_data('page')
        if page == None:
            instance = serializer_class(
                obj,
                partial=True,
                data=self.request.data,
                context={'request': self.request},
            )

        else:
            instance = serializer_class(
                obj,
                partial=True,
                exclude={'user'},
                data=self.request.data,
                context={'request': self.request}
            )
        
        # update and return
        update = self.perform_update(instance)
        return Response(update['data'], status=update['status'])
        
    def destroy(self, request, *args, **kwargs):
        pass

