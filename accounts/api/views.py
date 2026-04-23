from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializers
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "user_id": user.id,
                "email": user.email
            },
            status=status.HTTP_201_CREATED
        )
    

class LogoutApi(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error" : "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )
