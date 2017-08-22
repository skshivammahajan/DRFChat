from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.serializers import SuperUserSerializer
from experchat.authentication import SuperAdminAuthentication, TokenAuthentication

UserBase = get_user_model()


class SuperUserView(generics.ListCreateAPIView):
    queryset = UserBase.objects.filter(is_superuser=True)
    serializer_class = SuperUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SuperAdminAuthentication,)
    parser_classes = (JSONParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        userbase = UserBase.objects.filter(email=email, is_superuser=True).first()
        if userbase is not None:
            userbase.name = serializer.validated_data['name']
            userbase.is_active = True
            userbase.save()
            serializer = self.serializer_class(instance=userbase)
        else:
            userbase = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        token = TokenAuthentication.generate_credentials(request, userbase.id)

        response = {'token': token}
        response.update(serializer.data)

        return Response(response, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class SuperUserEnableView(APIView):
    queryset = UserBase.objects.filter(is_superuser=True)
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SuperAdminAuthentication,)

    def put(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(self.queryset, pk=pk)
        obj.is_active = True
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SuperUserDisableView(APIView):
    queryset = UserBase.objects.filter(is_superuser=True)
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SuperAdminAuthentication,)

    def put(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(self.queryset, pk=pk)
        obj.is_active = False
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
