# from rest_framework import status, generics
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import UserSerializer, CustomTokenObtainPairSerializer
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from rest_framework.decorators import api_view, permission_classes
# import logging

# logger = logging.getLogger(__name__)

# class RegisterView(generics.CreateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         try:
#             logger.info(f"Registration attempt with data: {request.data}")
#             serializer = self.get_serializer(data=request.data)
#             if serializer.is_valid():
#                 user = serializer.save()
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'user': UserSerializer(user).data,
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }, status=status.HTTP_201_CREATED)
#             logger.error(f"Registration validation failed: {serializer.errors}")
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             logger.error(f"Registration error: {str(e)}")
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     # def options(self, request, *args, **kwargs):
#     #     response = Response()
#     #     response["Access-Control-Allow-Origin"] = "http://localhost:5173"
#     #     response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
#     #     response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     #     return response
#     CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS"]
# CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def health_check(request):
#     return Response({"status": "healthy"}, status=status.HTTP_200_OK)





from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'user': UserSerializer(user).data,
                    'message': 'User registered successfully'
                }, status=status.HTTP_201_CREATED)

            return Response({
                'detail': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "healthy"}, status=status.HTTP_200_OK)
