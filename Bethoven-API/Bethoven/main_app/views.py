from rest_framework import generics
from rest_framework.response import Response

class ServerState(generics.GenericAPIView):
    def get(self, request, *args,  **kwargs):
        return Response({
            "message": "Server is running...",
        })