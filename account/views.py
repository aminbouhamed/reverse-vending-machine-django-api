from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from account.backends import TokenAuthenticationBackend
from rest_framework.authtoken.views import ObtainAuthToken
import qrcode
import io
from django.http import HttpResponse
from account.models import Account
import os
from api.models import RecyclingTransaction
from api.serializers import RecyclingTransactionSerializer
from django.db.models import Sum

@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


@api_view(['POST', ])
def qrcode_authentication_view(request):
    id = request.data.get("id")
    token = request.data.get("token")

    token_authentication_backend = TokenAuthenticationBackend()
    user = token_authentication_backend.authenticate(request=request, id=id, auth_token=token)
    if user is not None:
        user.backend = 'account.backends.TokenAuthenticationBackend'
        login(request, user)
        return Response({'response': 'Authentication successful'}, status=status.HTTP_200_OK)
        
    else:
        return Response({'response': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST', ])
def generate_qrcode_view(request):
    username = request.data.get("username")
    user = Account.objects.get(username=username)
    id = user.id
    token =  Token.objects.get(user=user)
    data = f"{id}:{token}"
    qrCode = qrcode.make(data)
    buffer = io.BytesIO()
    qrCode.save(buffer, format='PNG')
    qr_png = buffer.getvalue()
    response = HttpResponse(qr_png, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="qr_code.png"'
    return response

@api_view(['POST'])
def getRecyclingTransactions(request):
    username = request.data.get("username")
    user = Account.objects.get(username=username)
    transactions = RecyclingTransaction.objects.filter(client=user)
    
    # You can serialize the transactions or return them as-is, based on your needs
    #serialize transactions if you have a serializer defined
    serializedTransactions = RecyclingTransactionSerializer(transactions, many=True)
    return Response(serializedTransactions.data)
    
    # Or return transactions directly
    #return Response(transactions.values())

@api_view(['POST'])
def getTotalRecompense(request):
    username = request.data.get("username")
    user = Account.objects.get(username=username)
    transactions = RecyclingTransaction.objects.filter(client=user)
    total_recompense = transactions.aggregate(total_recompense_sum=Sum('totalRecompense'))['total_recompense_sum']
    # You can serialize the transactions or return them as-is, based on your needs
    #serialize transactions if you have a serializer defined
    response_data = {
        'total_recompense': total_recompense
    }
    
    return Response(response_data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def test_permission_view(request):
    return Response(status=status.HTTP_200_OK)