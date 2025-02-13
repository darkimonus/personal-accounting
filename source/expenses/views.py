from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from expenses.serializers import ReceiptSerializer
from expenses.models import Receipt


class ReceiptViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):

    serializer_class = ReceiptSerializer
    queryset = Receipt.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



