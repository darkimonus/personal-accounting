from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from expenses.serializers import ReceiptSerializer, RetrieveReceiptSerializer
from expenses.models import Receipt
from expenses.utils.receipts import create_receipt_from_validated_data


class ReceiptViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):

    serializer_class = ReceiptSerializer
    queryset = Receipt.objects.all()

    def perform_create(self, serializer):
        receipt = create_receipt_from_validated_data(serializer.validated_data, self.request.user)
        serializer = RetrieveReceiptSerializer(receipt)
        return serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: update exception handling, to return proper error message
        try:
            response_serializer = self.perform_create(serializer)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
