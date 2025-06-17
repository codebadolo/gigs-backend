# users/views.py
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import User
# users/views.py
from rest_framework import generics, permissions
from users.serializers import RegisterSerializer , AdminRegisterSerializer
from rest_framework.response import Response
from rest_framework import status

class AdminRegisterView(generics.CreateAPIView):
    serializer_class = AdminRegisterSerializer
    permission_classes = [permissions.IsAdminUser]  # Seuls les admins existants peuvent créer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Administrateur créé avec succès"}, status=status.HTTP_201_CREATED)
class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email et mot de passe requis.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_obj = User.objects.get(email=email)
            # Authentification avec username (email ou username selon votre USERNAME_FIELD)
            user = authenticate(request, username=user_obj.username or user_obj.email, password=password)
        except User.DoesNotExist:
            user = None

        # Vérifier que l'utilisateur est actif ET admin (ou staff)
        if user is not None and user.is_active and (user.role == 'admin' or user.is_staff):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Identifiants invalides ou accès non autorisé'}, status=status.HTTP_401_UNAUTHORIZED)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email et mot de passe sont requis.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username or user_obj.email, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)