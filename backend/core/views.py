from rest_framework import viewsets

class SoftDeleteModelViewSet(viewsets.ModelViewSet):

    def perform_destroy(self, instance):
        instance.state = -1
        instance.save(update_fields=["state", "updated_at"])