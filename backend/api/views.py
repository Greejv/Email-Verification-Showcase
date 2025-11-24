from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializers import EmailSerializer
from .EmailVerification import generate_verification, email_verifier


# api pre ulozenie emailu do databazy a callnutie funkcie pre odoslanie verifikacneho emailu
@api_view(['POST'])
def send_email(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # email bude obsahovať práve ulozene data do databazy
    email = serializer.save()

    # call funkcie pre odoslanie verifikacneho emailu s informaciami o prave ulozenom emaily
    generate_verification(email)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# api pre callnutie funkcie pre verifikaciu token s tokenom ktory prisiel s requestom
@api_view(['POST'])
def verify_token(request):
    token = request.data.get('token')

    response = email_verifier(token)

    return Response({"detail": {response.data.get('detail')}}, status=response.status_code)