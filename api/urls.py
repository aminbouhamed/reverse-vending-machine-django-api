"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import RecyclableItemView, RecyclingHistoryView, RecyclingTransactionView, RVMView
from account.views import registration_view, qrcode_authentication_view, test_permission_view, generate_qrcode_view
from rest_framework.authtoken.views import obtain_auth_token
from account.views import CustomObtainAuthToken, getRecyclingTransactions, getTotalRecompense

urlpatterns = [
    path('rvm/api/register', registration_view),
    path('rvm/api/login', CustomObtainAuthToken.as_view()),
    path('rvm/api/qrcode-auth', qrcode_authentication_view),
    path('rvm/api/qrcode-generate', generate_qrcode_view),
    path('rvm/api/get-recycling-transactions', getRecyclingTransactions),
    path('rvm/api/get-recycling-history', RecyclingTransactionView.getRecyclingHistory),
    path('rvm/api/get-total-recompense', getTotalRecompense),

    path('admin', admin.site.urls),
    path('rvm/api/recyclableItem', RecyclableItemView.getAll),
    path('rvm/api/recyclableItem/add', RecyclableItemView.addRecyclableItem),
    path('rvm/api/recyclableItem/<int:id>', RecyclableItemView.getRecyclableItemById),
    path('rvm/api/recyclableItem/update/<int:id>', RecyclableItemView.updateRecyclableItem),
    path('rvm/api/recyclableItem/delete/<int:id>', RecyclableItemView.deleteRecyclableItem),

    path('rvm/api/recyclingHistory', RecyclingHistoryView.getAll),
    path('rvm/api/recyclingHistory/add', RecyclingHistoryView.addRecyclingHistory),
    path('rvm/api/recyclingHistory/<int:id>', RecyclingHistoryView.getRecyclingHistoryById),
    path('rvm/api/recyclingHistory/update/<int:id>', RecyclingHistoryView.updateRecyclingHistory),
    path('rvm/api/recyclingHistory/delete/<int:id>', RecyclingHistoryView.deleteRecyclingHistory),

    path('rvm/api/recyclingTransaction', RecyclingTransactionView.getAll),
    path('rvm/api/recyclingTransaction/add', RecyclingTransactionView.addRecyclingTransaction),
    path('rvm/api/recyclingTransaction/<int:id>', RecyclingTransactionView.getRecyclingTransactionById),
    path('rvm/api/recyclingTransaction/update/<int:id>', RecyclingTransactionView.updateRecyclingTransaction),
    path('rvm/api/recyclingTransaction/delete/<int:id>', RecyclingTransactionView.deleteRecyclingTransaction),

    path('rvm/api/rvm', RVMView.getAll),
    path('rvm/api/rvm/add', RVMView.addRVM),
    path('rvm/api/rvm/<int:id>', RVMView.getRVMById),
    path('rvm/api/rvm/update/<int:id>', RVMView.updateRVM),
    path('rvm/api/rvm/delete/<int:id>', RVMView.deleteRVM),
]
