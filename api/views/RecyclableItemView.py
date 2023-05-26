from api.models import RecyclableItem
from api.serializers import RecyclableItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def getAll(request):
    recyclableItemList = RecyclableItem.objects.all()
    serializedRecyclableItemList = RecyclableItemSerializer(recyclableItemList, many=True)
    return Response(serializedRecyclableItemList.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addRecyclableItem(request):
    serializedRecyclableItem = RecyclableItemSerializer(data=request.data)
    if serializedRecyclableItem.is_valid():
        serializedRecyclableItem.save()
        return Response(serializedRecyclableItem.data, status=status.HTTP_201_CREATED)
    return Response(serializedRecyclableItem.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
def getRecyclableItemById(request, id):
    try:
        recyclableItem = RecyclableItem.objects.get(pk=id)
    except RecyclableItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializedRecyclableItem = RecyclableItemSerializer(recyclableItem)
    return Response(serializedRecyclableItem.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateRecyclableItem(request, id):
    try:
        recyclableItem = RecyclableItem.objects.get(pk=id)
    except RecyclableItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializedRecyclableItem = RecyclableItemSerializer(recyclableItem, data=request.data)
    if serializedRecyclableItem.is_valid():
        serializedRecyclableItem.save()
        return Response(serializedRecyclableItem.data)
    return Response(serializedRecyclableItem.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteRecyclableItem(request, id):
    try:
        recyclableItem = RecyclableItem.objects.get(pk=id)
    except RecyclableItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    recyclableItem.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
