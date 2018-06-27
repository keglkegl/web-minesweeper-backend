from api.models import Game
from api.serializers import GameSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from rest_framework import permissions
from api.permissions import IsOwnerEmptyOrReadOnly, IsOwner, ReadOnly
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import pusher
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.settings import api_settings

pusher_client = pusher.Pusher(
  app_id='510769',
  key='eff33873fa92681cdb5e',
  secret='2fb1bd87d2a97943e04b',
  cluster='eu',
  ssl=True
)


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user, format=None):
        user = self.get_object(user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GameList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_fields = ('username',)


class GameDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerEmptyOrReadOnly,)
    """
    Retrieve, update or delete a Game instance.
    """
    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            newGame = self.get_object(pk)
            content = { 'mineFieldSetup': newGame.mineFieldSetup, 'turn' : newGame.turn, 'player1score' : newGame.player1score, 'player2score' : newGame.player2score}
            pusher_client.trigger((str(pk) + '_game'), 'event', content)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        game = self.get_object(pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CheckAuthorization(APIView):
    def get(self, request, format=None):
        if 'logged' in request.session:
            user = User.objects.get(username=request.session['username'])
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            content = {'token' : token, 'username' : request.session['username']}
            return Response(content)
        else:
            return HttpResponse('Please login!')

class LoginAndObtainToken(APIView):

    def post(self, request, format=None):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['logged'] = True
            request.session['username'] = username
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            content = {'token' : token, 'username' : user.username}
            return JsonResponse(content)
        else:
            return HttpResponse("Login Failed!")

class LogoutUser(APIView):

    def get(self, request, format=None):
        try:
            del request.session['logged']
            del request.session['username']
        except KeyError:
            pass
        content = {'logout' : True }
        return HttpResponse("You're logged out!")

class RegistrationAndObtainToken(APIView):

    def post(self, request, format=None):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['logged'] = True
                request.session['username'] = username
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                content = {'token' : token, 'username' : user.username}
                return JsonResponse(content)
            else:
                return HttpResponse("Registration successful but login failed!")
        else:
            return JsonResponse(form.errors)