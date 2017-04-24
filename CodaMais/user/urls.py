# Django.
from django.conf.urls import url

# Local Django.
from .views import (
    register_view,
    register_confirm,
    login_view,
    logout_view,
    edit_profile_view,
    profile_view,
    recover_password,
    recover_password_confirm,
)

urlpatterns = (
    # TODO(João) Change this url to landpage, and delete this url
    url(r'^register/', register_view, name='register_view'),

    url(r'^confirm/(?P<activation_key>\w+)/', register_confirm,
        name='confirm_account'),

    # TODO(João) Change this url to landpage, and delete this url
    url(r'^login/', login_view, name='login_view'),
    url(r'^logout/', logout_view, name='logout_view'),
    url(r'^edit/(?P<username>[\w|\W]+)/', edit_profile_view, name='edit'),
    url(r'^profile/(?P<username>[\w|\W]+)/', profile_view, name='profile_view'),

    # Recover password.
    url(r'^recoverpassword/', recover_password, name='recover_password'),
    url(r'^recover/(?P<activation_key>\w+)/', recover_password_confirm,
        name='recover_password_confirm'),
)
