from rest_framework import serializers
from api.models import Game
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'score')

class GameSerializer(serializers.ModelSerializer):
    player1 = serializers.SlugRelatedField(slug_field='username', allow_null=True, queryset=User.objects.all())
    player2 = serializers.SlugRelatedField(slug_field='username', allow_null=True, queryset=User.objects.all())
    winner = serializers.SlugRelatedField(slug_field='username', allow_null=True, queryset=User.objects.all())
    turn = serializers.BooleanField()
    mineFieldSetup = serializers.JSONField(required=False)

    class Meta:
        model = Game
        fields = ('id', 'name', 'date', 'player1', 'player2', 'turn', 'player1score', 'player2score', 'winner', 'mineFieldSetup')
