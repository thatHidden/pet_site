from django.contrib import admin
from django.urls import path

from axaxa.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('addlot/', AddLot.as_view(), name='add_lot'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('search/<str:car>',  SearchCar.as_view(), name='search')
]