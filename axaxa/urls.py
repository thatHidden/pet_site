from django.contrib import admin
from django.urls import path

from axaxa.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('profile/lots', profile_lots, name='profile_lots'),
    path('profile/bids', profile_bids, name='profile_bids'),
    path('profile/contact_info', login_required(ProfileEditInfo.as_view()), name='profile_contact'),
    path('addlot/', AddLot.as_view(), name='add_lot'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('search/<str:car>',  SearchCar.as_view(), name='search')
]