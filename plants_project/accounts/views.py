from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import RegisterSerializer
import logging
from rest_framework.permissions import IsAdminUser

logger = logging.getLogger(__name__)

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"User registered: {user.username}")

class PrivateInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"User accessed private info: {request.user.username}")
        return Response({"msg": f"Hello, {request.user.username}! Only authorized users see this."})

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info(f"Admin accessed admin page: {request.user.username}")
        return Response({"msg": "Hello, Admin! This page is for admin users only."})