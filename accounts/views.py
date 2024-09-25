from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .validators import validator_signup
from .serializers import UserSerializer


class AccountView(APIView):
    def post(self, request):
        is_valid, error_message = validator_signup(request.data)
        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=request.data.get("username"),
            password=request.data.get("password"),
            name=request.data.get("name"),
            email=request.data.get("email"),
            address=request.data.get("address"),
        )
        serializer = UserSerializer(user)
        res_data = serializer.data
        refresh = RefreshToken.for_user(user)
        res_data['refresh_token'] = str(refresh)
        res_data['access_token'] = str(refresh.access_token)
        return Response(res_data, status=status.HTTP_201_CREATED)
