from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from rest_framework import viewsets
from rest_framework import routers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Tier, Contact, Role, CallLog, NewUser, Position
from core.serializers import TierSerializer, ContactSerializer, RoleSerializer, CallLogSerializer, UserSerializer, \
    PositionSerializer


class TierViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Tier.objects.all()
    serializer_class = TierSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class CallLogViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer
    # permission_classes = [IsAuthenticated]
    # permission_classes = (TokenAuthentication,)


class PositionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class LoginViewSet(viewsets.ModelViewSet):
    """
    Check email and password and return an auth token.
    """
    queryset = NewUser.objects.all()
    serializer_class = AuthTokenSerializer

    def create(self, request, *args, **kwargs):
        """
        Use obtainAuthToken APIView to validate and create a token
        """
        return CustomObtainAuthToken().as_view()(request=request._request)


# Register views sets
router = routers.DefaultRouter()
router.register(r'tiers', TierViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'call_log', CallLogViewSet)
router.register(r'users', UserViewSet)
router.register(r'positions', PositionViewSet)
router.register('login', LoginViewSet, basename='login')
