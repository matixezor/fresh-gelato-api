from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from django.http import Http404
from django.core.mail import send_mail

from .serializers import RecipeSerializer, RecipeListSerializer, EmailSerializer, UserSerializer
from .models import Recipe


@api_view(['GET'])
def get_recipes_list(request):
    recipes = Recipe.objects.all()

    serializer = RecipeListSerializer(recipes, context={'request': request}, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_recipe_info(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)

        serializer = RecipeSerializer(instance=recipe, context={'request': request})
        return Response(serializer.data)

    except:
        raise Http404


@api_view(['GET'])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def post_email(request):
    serializer = EmailSerializer(data=request.data)

    if serializer.is_valid():
        send_mail(
            serializer.validated_data['sender_name'] + ' ' + serializer.validated_data['sender_mail'],
            serializer.validated_data['content'],
            serializer.validated_data['sender_mail'],
            ['matixezor1998@interia.pl'],
            fail_silently=False,
        )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

