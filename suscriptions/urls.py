from django.urls import path
from .views import (
    SubscriptionView,
    SubscriptionMONView,
    SubscriptionYEARView,
    SubscriptionCancelView,
    CustomerCreateView,
    CustomerLoginView,
    CustomerLogoutView
)

urlpatterns = [
    # {{ url 'home' }}
    path(
        route='',
        view=SubscriptionView.as_view(),
        name='home',
    ),
    # {{ url 'subscription-mon' }}
    path(
        route='monthly/',
        view=SubscriptionMONView.as_view(),
        name='subscription-mon',
    ),
    # {{ url 'subscription-year' }}
    path(
        route='annual/',
        view=SubscriptionYEARView.as_view(),
        name='subscription-year',
    ),
    # {{ url 'cancel' }}
    path(
        route='cancel/<stripe_id>',
        view=SubscriptionCancelView.as_view(),
        name='cancel',
    ),
    # {{ url 'signup' }}
    path(
        route='signup/',
        view=CustomerCreateView.as_view(),
        name='signup',
    ),
    # {{ url 'login' }}
    path(
        route='login/',
        view=CustomerLoginView.as_view(),
        name='login',
    ),
    # {{ url 'logout' }}
    path(
        route='logout/',
        view=CustomerLogoutView.as_view(),
        name='logout',
    ),
]
