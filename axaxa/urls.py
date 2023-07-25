from django.contrib import admin
from django.urls import path, re_path

from axaxa.views import *

from allauth.account.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('addlot/', AddLot.as_view(), name='add_lot'),
    path('out/', logout_user, name='logout'),
    path('lot/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('lot/<slug:post_slug>/bid/', MakeBid.as_view(), name='makebid'),
    path('search/<str:car>', SearchCar.as_view(), name='search'),

    path('register/', SignupView.as_view(), name='account_signup'),
    path('login/', LoginView.as_view(), name='account_login'),
    path("password/reset/", PasswordResetView.as_view(), name="account_reset_password"),
    path("password/reset/done/", PasswordResetDoneView.as_view(), name="account_reset_password_done", ),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            PasswordResetFromKeyView.as_view(),
            name="account_reset_password_from_key", ),
    path("password/reset/key/done/",
         PasswordResetFromKeyDoneView.as_view(),
         name="account_reset_password_from_key_done"),
    path("password/set/", PasswordSetView.as_view(), name="account_set_password"),
    path("password/change/", PasswordChangeView.as_view(), name="account_change_password"),

    path('profile/', profile, name='profile'),
    path('profile/new_picture', login_required(ProfileEditPicture.as_view()), name="profile_pic_upd"),
    path('profile/lots', profile_lots, name='profile_lots'),
    path('profile/bids', profile_bids, name='profile_bids'),
    path('profile/contact_info', login_required(ProfileEditInfo.as_view()), name='profile_contact'),
]
