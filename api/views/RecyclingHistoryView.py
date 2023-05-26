from api.models import RecyclingHistory
from api.serializers import RecyclingHistorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.models import RecyclingTransaction, RecyclableItem

@api_view(['GET'])
def getAll(request):
    recyclingHistoryList = RecyclingHistory.objects.all()
    serializedRecyclingHistoryList = RecyclingHistorySerializer(recyclingHistoryList, many=True)
    return Response(serializedRecyclingHistoryList.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addRecyclingHistory(request):
    recyclingHistroyList = []
    for object in request.data:
        serializedRecyclingHistory = RecyclingHistorySerializer(data=object)
        if serializedRecyclingHistory.is_valid():
            recyclingTransaction_id = object["recyclingTransaction"]
            recyclableItem_id = object["recyclableItem"]
            quantity = object["quantity"]
            recyclingTransaction = get_object_or_404(RecyclingTransaction, pk=recyclingTransaction_id)
            recyclableItem = get_object_or_404(RecyclableItem, pk=recyclableItem_id)
            recyclingHistory = RecyclingHistory(recyclingTransaction = recyclingTransaction, recyclableItem = recyclableItem, quantity = quantity)
            recyclingHistroyList.append(recyclingHistory)
            print("okk")
            print(recyclingHistroyList)
            #recyclingHistory.save()
            #serializedRecyclingHistory = RecyclingHistorySerializer(recyclingHistory)
            #return Response(serializedRecyclingHistory.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializedRecyclingHistory.errors, status=status.HTTP_400_BAD_REQUEST)
    RecyclingHistory.objects.bulk_create(recyclingHistroyList)
    return Response(status=status.HTTP_200_OK) 

@api_view(['GET'])
def getRecyclingHistoryById(request, id):
    try:
        recyclingHistory = RecyclingHistory.objects.get(pk=id)
    except RecyclingHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializedRecyclingHistory = RecyclingHistorySerializer(recyclingHistory)
    return Response(serializedRecyclingHistory.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateRecyclingHistory(request, id):
    try:
        recyclingHistory = RecyclingHistory.objects.get(pk=id)
    except RecyclingHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializedRecyclingHistory = RecyclingHistorySerializer(recyclingHistory, data=request.data)
    if serializedRecyclingHistory.is_valid():
        serializedRecyclingHistory.save()
        return Response(serializedRecyclingHistory.data)
    return Response(serializedRecyclingHistory.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteRecyclingHistory(request, id):
    try:
        recyclingHistory = RecyclingHistory.objects.get(pk=id)
    except RecyclingHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    recyclingHistory.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
