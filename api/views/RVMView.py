from api.models import RVM
from api.serializers import RVMSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def getAll(request):
    RVMList = RVM.objects.all()
    serializedRVMList = RVMSerializer(RVMList, many=True)
    return Response(serializedRVMList.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addRVM(request):
    serializedRVM = RVMSerializer(data=request.data)
    if serializedRVM.is_valid():
        serializedRVM.save()
        return Response(serializedRVM.data, status=status.HTTP_201_CREATED)
    return Response(serializedRVM.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
def getRVMById(request, id):
    try:
        rvm = RVM.objects.get(pk=id)
    except RVM.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializedRVM = RVMSerializer(rvm)
    return Response(serializedRVM.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateRVM(request, id):
    try:
        rvm = RVM.objects.get(pk=id)
    except RVM.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializedRVM = RVMSerializer(rvm, data=request.data)
    if serializedRVM.is_valid():
        serializedRVM.save()
        return Response(serializedRVM.data)
    return Response(serializedRVM.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteRVM(request, id):
    try:
        rvm = RVM.objects.get(pk=id)
    except RVM.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    rvm.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
