from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import *
from django.core import serializers
from validate_email import validate_email
import json
import sys
from urllib import request, parse
from langdetect import detect

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

def translate(text):
    url = "http://localhost:5000/translate"
    params = {"q": text, "source": detect(text), "target": 'en'}
    params["api_key"] = 'f726f7b4-eb71-47a5-aba8-e8b4cbd94ab5'
    url_params = parse.urlencode(params)
    req = request.Request(url, data=url_params.encode())
    response = request.urlopen(req)
    response_str = response.read().decode()
    return json.loads(response_str)["translatedText"]


@api_view(['POST','GET'])
@permission_classes((IsAuthenticated, ))
def index(request):
    if request.method == 'POST':
        serializer = inputSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.has_perm('api.do_both'):
                check = emailcheck(serializer.validated_data['email'])
                text = translate(serializer.validated_data['text'])
                data = {
                    "email": serializer.validated_data['email'],
                    "email_is_valid": check,
                    "text_translated": text
                }
                return Response(data,status=200)
            else:
                if user.has_perm('api.only_email_validation'):
                    check = emailcheck(serializer.validated_data['email'])
                    data = {
                        "email": serializer.validated_data['email'],
                        "email_is_valid": check,
                        "text_translated": "null"
                    }
                    return Response(data,status=200)
                elif user.has_perm('api.only_translate_text'):
                    text = translate(serializer.validated_data['text'])
                    data = {
                        "email": serializer.validated_data['email'],
                        "email_is_valid": "false",
                        "text_translated": text
                    }
                    return Response(data,status=200)
                else:
                    data = {}
                    data['response'] = "Sorry! This api can only be used by user who have permissions"
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
        data['response'] = "Please hit the endpoint with POST method only after logging in with appropriate user, Thanks!"
        return Response(data,status=400)


# @api_view(['POST','GET'])
# def login(request):
#     if request.method == 'POST':
#         serializer = loginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     data = {}
#                     data['response'] = "Success, now use the main api to test!"
#                     return Response(data,status=200)
#                 else:
#                     data = {}
#                     data['response'] = "This account is disabled!"
#                     return Response(data,status=400)
#             else:
#                 data = {}
#                 data['response'] = "Invalid Credentials!"
#                 return Response(data,status=400)
#         else:
#             dat = serializer.errors
#             data = {}
#             data['error'] = {}
#             if "username" in dat:
#                 if dat['username'][0].code == "invalid":
#                     data['error']['message'] = "username is invalid"
#                     data['error']['description'] = "username key should be a string"
#                 else:
#                     data['error']['message'] = "username is required"
#                     data['error']['description'] = "Please enter username with appropriate value"
#             if "password" in dat:
#                 if dat['password'][0].code == "invalid":
#                     data['error']['message'] = "password is invalid"
#                     data['error']['description'] = "password key should be a string"
#                 else:
#                     data['error']['message'] = "password is required"
#                     data['error']['description'] = "Please enter password with appropriate value"
#             return Response(data,status=406)
#     else:
#         data = {}
#         data['response'] = "Please hit the endpoint with POST method only after logging in with appropriate user, Thanks!"
#         return Response(data,status=400)