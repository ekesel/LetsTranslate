from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import *
from django.core import serializers
from validate_email import validate_email


def emailcheck(email):
    is_valid = validate_email(
    email_address=email,
    check_format=True,
    check_blacklist=True,
    check_dns=True,
    dns_timeout=10,
    check_smtp=True,
    smtp_timeout=10,
    smtp_skip_tls=False,
    smtp_tls_context=None,
    smtp_debug=False)

    return is_valid

@api_view(['POST','GET'])
@permission_classes((IsAuthenticated, ))
def index(request):
    if request.method == 'POST':
        serializer = inputSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.username == 'user1':
                check = emailcheck(serializer.validated_data['email'])
                data = {
                    "email": serializer.validated_data['email'],
                    "email_is_valid": check,
                    "text_translated": "null"
                }
                return Response(data,status=200)
            elif user.username == 'user2':
                text = translate()
                data = {}
                # add code
                return Response(data,status=200)
            elif user.username == 'user3':
                check = emailcheck()
                text = translate()
                data = {}
                # add code
                return Response(data,status=200)
            else:
                data = {}
                data['response'] = "Sorry! This api can only be used by user1, user2 and user3"
                return Response(data,status=400)
        else:
            dat = serializer.errors
            data = {}
            data['error'] = {}
            if "email" in dat:
                if dat['email'][0].code == "invalid":
                    data['error']['message'] = "Email is invalid"
                    data['error']['description'] = "Email key should be a string"
                else:
                    data['error']['message'] = "Email is required"
                    data['error']['description'] = "Please enter email with appropriate value"
            if "text" in dat:
                if dat['text'][0].code == "invalid":
                    data['error']['message'] = "text is invalid"
                    data['error']['description'] = "text key should be a string"
                else:
                    data['error']['message'] = "text is required"
                    data['error']['description'] = "Please enter text with appropriate value"
            return Response(data,status=406)
    else:
        data = {}
        data['response'] = "Please hit the endpoint with POST method only and use appropriate user Token in Headers, Thanks!"
        return Response(data,status=400)