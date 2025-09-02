# Write your Python code here
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MenuItem
from .serializers import MenuItemSerializer

# CREATE A NEW MENU ITEM
@api_view(['POST'])
def create_menu_item(request):
    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# LIST ALL MENU ITEMS (OPTIONALY FILTER BY restaurant_id)
@api_view(['GET'])
def list_menu_items(request):
    restaurant_id = request.query_params.get('restaurant_id', None)
    if restaurant_id:
        menu_item = MenuItem.objects.filter(restaurant_id=restaurant_id)
    else:
        menu_item = MenuItem.objects.all()
    
    serializer = MenuItemSerializer(menu_item, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# GET A SPECIFIC MENU ITEM BY ID
@api_view(['GET'])
def get_menu_item(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(
            {"error": "menu item not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = MenuItemSerializer(menu_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


# UPDATE A MENU ITEM
@api_view(['PUT'])
def update_menu_item(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(
            {"error": "Menu item not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = MenuItemSerializer(menu_item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE A MENU ITEM
@api_view(['DELETE'])
def delete_menu_item(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(
            {"error": "Menu item does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    menu_item.delete()
    return Response(
        {"message": "Menu item deleted successfully."},
        status=status.HTTP_204_NO_CONTENT
    )