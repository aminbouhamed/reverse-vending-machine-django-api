from api.models import RecyclingTransaction
from api.serializers import RecyclingTransactionSerializer, RecyclingHistorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.models import Account, RVM
from api.models import RecyclingHistory


@api_view(['GET'])
def getAll(request):
    recyclingTransactionList = RecyclingTransaction.objects.all()
    serializedRecyclingTransactionList = RecyclingTransactionSerializer(recyclingTransactionList, many=True)
    return Response(serializedRecyclingTransactionList.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addRecyclingTransaction(request):
    serializedRecyclingTransaction = RecyclingTransactionSerializer(data=request.data)
    if serializedRecyclingTransaction.is_valid():
        try:
            client_id = request.data["client"]
        except:
            client_id = None

        rvm_id = request.data["rvm"]
        transactionDate = request.data["transactionDate"]
        totalRecompense = request.data["totalRecompense"]

        if client_id != None:
            client = get_object_or_404(Account, pk=client_id)
        else:
            client = None
        rvm = get_object_or_404(RVM, pk=rvm_id)
        
        recycling_transaction = RecyclingTransaction(client=client, transactionDate=transactionDate, totalRecompense=totalRecompense, rvm=rvm)
        recycling_transaction.save()
        serializedRecyclingTransaction = RecyclingTransactionSerializer(recycling_transaction)
        return Response(serializedRecyclingTransaction.data, status=status.HTTP_201_CREATED)
    return Response(serializedRecyclingTransaction.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
def getRecyclingTransactionById(request, id):
    try:
        recyclingTransaction = RecyclingTransaction.objects.get(pk=id)
    except RecyclingTransaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializedRecyclingTransaction = RecyclingTransactionSerializer(recyclingTransaction)
    return Response(serializedRecyclingTransaction.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateRecyclingTransaction(request, id):
    try:
        recyclingTransaction = RecyclingTransaction.objects.get(pk=id)
    except RecyclingTransaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializedRecyclingTransaction = RecyclingTransactionSerializer(recyclingTransaction, data=request.data)
    if serializedRecyclingTransaction.is_valid():
        serializedRecyclingTransaction.save()
        return Response(serializedRecyclingTransaction.data)
    return Response(serializedRecyclingTransaction.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteRecyclingTransaction(request, id):
    try:
        recyclingTransaction = RecyclingTransaction.objects.get(pk=id)
    except RecyclingTransaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    recyclingTransaction.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def getRecyclingHistory(request):
    recyclingTransactionId = request.data.get("id")
    recyclingTransaction = get_object_or_404(RecyclingTransaction, id=recyclingTransactionId)
    recyclingHistory = RecyclingHistory.objects.filter(recyclingTransaction=recyclingTransaction)
    
    # You can serialize the transactions or return them as-is, based on your needs
    #serialize transactions if you have a serializer defined
    serializedHistory = RecyclingHistorySerializer(recyclingHistory, many=True)
    return Response(serializedHistory.data)
    
    # Or return transactions directly
    #return Response(transactions.values())
