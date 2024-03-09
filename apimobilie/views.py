from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from vitimas.backends import CustomAuthBackend

from .authentication import CustomTokenAuthentication
from .models import CustomToken
from .serializers import OcorrenciaSerializer


class LoginAPIView(APIView):
    def post(self, request):
        cpf = request.data.get("cpf")
        password = request.data.get("password")
        user = CustomAuthBackend().authenticate(request, cpf=cpf, password=password)
        if user:
            token, created = CustomToken.objects.get_or_create(user=user)
            return Response({"key": token.key}, status=status.HTTP_200_OK)

        else:
            # Falha na autenticação
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class OcorrenciaAPIView(CreateAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OcorrenciaSerializer
