from django.contrib import admin
from .models import *

admin.site.register([RecyclableItem, RVM, RecyclingTransaction, RecyclingHistory])