from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from incomes.serializers import IncomeTaxSerializer


class IncomeTaxesView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = IncomeTaxSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
