from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from django.core.mail import send_mail

from .serializers import RecipeSerializer, RecipeListSerializer, EmailSerializer, UserSerializer
from .models import Recipe


@api_view(['GET', 'POST'])
def recipes_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()

        serializer = RecipeListSerializer(recipes, context={'request': request}, many=True)

        return Response(serializer.data)
    elif request.user.is_staff:
        serializer = RecipeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_recipe_info(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)

        serializer = RecipeSerializer(instance=recipe, context={'request': request})
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def user_view(request):
    if request.method == 'GET' and request.user.is_authenticated:
        serializer = UserSerializer(request.user)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_401_UNAUTHORIZED)

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

