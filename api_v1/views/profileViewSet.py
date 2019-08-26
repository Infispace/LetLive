from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from api_v1.serializers import AdminSerializer
from api_v1.serializers import AuthorSerializer
from api_v1.serializers import PublisherSerializer
from api_v1.serializers import SubscriberSerializer


class ProfileViewSet(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users view and edit their profile data.
    """
    permission_classes = [
        IsAuthenticated,
    ]
    
    def get_object(self):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        obj = None
        try:
            obj = self.request.user.author
        except ObjectDoesNotExist:
            pass

        try:
            obj = self.request.user.admin
        except ObjectDoesNotExist:
            pass

        try:
            obj = self.request.user.publisher
        except ObjectDoesNotExist:
            pass

        try:
            obj = self.request.user.subscriber
        except ObjectDoesNotExist:
            pass

        # throw ObjectDoesNotExist if no obj
        if obj == None:
            raise ObjectDoesNotExist('Profile data does not exist')

        return obj
        
    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        serializer_class = None
        try:
            self.request.user.author
            serializer_class = AuthorSerializer
        except ObjectDoesNotExist:
            pass

        try:
            self.request.user.admin
            serializer_class = AdminSerializer
        except ObjectDoesNotExist:
            pass

        try:
            self.request.user.subscriber
            serializer_class = SubscriberSerializer
        except ObjectDoesNotExist:
            pass

        try:
            self.request.user.publisher
            serializer_class = PublisherSerializer
        except ObjectDoesNotExist:
            pass

        return serializer_class
    
    def perform_update(self, serializer):
        """
        Update the existing AppUser instance.
        """
        response_data = None
        status_code = 200
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
        else:
            response_data = serializer.errors
            status_code = 400

        return {
            'data': response_data,
            'status': status_code
        }

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a the user profile, An instance of AppUser model.
        """
        obj = self.get_object()
        serializer_class = self.get_serializer_class()
        
        # get the AppUser instance from serializer
        instance = serializer_class(
            obj,
            context={'request': self.request}
        )

        return Response(instance.data)

    def update(self, request, *args, **kwargs):
        """
        Edit the user profile.
        """
        obj = self.get_object()
        serializer_class = self.get_serializer_class()
        
        # get the AppUser instance from serializer
        instance = serializer_class(
            obj,
            exclude={'user'},
            data=request.data,
            context={'request': self.request},
        )
        
        # update and return
        update = self.perform_update(instance)
        return Response(update['data'], update['status'])
        
    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer_class = self.get_serializer_class()

        # get the AppUser instance from serializer
        instance = serializer_class(
            obj,
            exclude={'user'},
            data=request.data,
            partial=True,
            context={'request': self.request}
        )
        
        # update and return
        update = self.perform_update(instance)
        return Response(update['data'], update['status'])
        
    def destroy(self, request, *args, **kwargs):
        pass

