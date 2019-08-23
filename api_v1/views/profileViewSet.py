from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from api_v1.serializers import AdminSerializer
from api_v1.serializers import AuthorSerializer
from api_v1.serializers import PublisherSerializer
from api_v1.serializers import SubscriberSerializer
from home.models import Admin
from home.models import Author
from home.models import Publisher
from home.models import Subscriber


class ProfileViewSet(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [
        IsAuthenticated,
    ]
    
    def get_queryset(self):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        queryset = None
        try:
            self.request.user.author
            queryset = Author.objects.get(
                user=self.request.user
            )
        except ObjectDoesNotExist:
            pass

        try:
            self.request.user.admin
            queryset = Admin.objects.get(
                user=self.request.user
            )
        except ObjectDoesNotExist:
            pass

        try:
            self.request.user.publisher
            queryset = Publisher.objects.get(
                user=self.request.user
            )
        except ObjectDoesNotExist:
            pass

        try:
            self.request.user.subscriber
            queryset = Subscriber.objects.get(
                user=self.request.user
            )
        except ObjectDoesNotExist:
            pass

        
        if queryset == None:
            raise ObjectDoesNotExist

        return queryset
        
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class
    
    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        serializer_class = None
        try:
            serializer_class = AuthorSerializer(
                self.request.user.author,
                context={'request': self.request}
            )
        except ObjectDoesNotExist:
            pass

        try:
            serializer_class = AdminSerializer(
                self.request.user.admin,
                context={'request': self.request}
            )
        except ObjectDoesNotExist:
            pass

        try:
            serializer_class = SubscriberSerializer(
                self.request.user.subscriber,
                context={'request': self.request}
            )
        except ObjectDoesNotExist:
            pass

        try:
            serializer_class = PublisherSerializer(
                self.request.user.publisher,
                context={'request': self.request}
            )
        except ObjectDoesNotExist:
            pass

        # make user readonly
        serializer_class.fields['user'].read_only = True
        return serializer_class
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a the user profile, An instance of AppUser model.
        """
        serializer_class = self.get_serializer_class()
        return Response(serializer_class.data)

    def update(self, request, *args, **kwargs):
        self.get_queryset()
        self.get_serializer_class()
        
    def destroy(self, request, *args, **kwargs):
        pass

