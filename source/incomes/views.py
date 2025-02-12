from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin

from incomes.serializers import IncomeSourceSerializer


class IncomeSourcesView(generics.GenericAPIView, CreateModelMixin):
    serializer_class = IncomeSourceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

