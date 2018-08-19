import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (
    TemplateView,
    FormView,
    CreateView,
    DetailView,
)

from .forms import SuscriptionForm, CustomerCreationForm

from .models import Subscription, Customer


class StripeMixin(object):
    """
    Mixing to add Public Key to the context_data on views
    """

    def get_context_data(self):
        context = super(StripeMixin, self).get_context_data()
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class CustomerCreateView(CreateView):
    """ Create Customer View or Registration Users"""

    model = Customer
    template_name = 'suscriptions/customer_create.html'
    form_class = CustomerCreationForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        customer = Customer.objects.create(user=user)
        login(self.request, user)
        return redirect('/')


class CustomerLoginView(LoginView):
    """ Login Customers or Users """
    success_url = '/'
    template_name = 'suscriptions/customer_login.html'


class CustomerLogoutView(LogoutView):
    """ Logout Customers or Users """
    pass


class SubscriptionView(TemplateView):
    """ Index view with subscriptions plans """
    template_name = 'suscriptions/suscriptions.html'


class SubscriptionCancelView(LoginRequiredMixin, DetailView):
    """
    Form for cancel subscription.
    It will remove the subcription plan from the database,
    the stripe_customer_id and the customer user from the Dashboard
    on stripe
    """

    model = Customer
    slug_field = 'stripe_customer_id'
    slug_url_kwarg = 'stripe_id'

    template_name = 'suscriptions/my-subscription.html'

    def get_context_data(self, **kwargs):
        context = super(SubscriptionCancelView, self).get_context_data(**kwargs)
        obj = (
            Subscription.objects.select_related('stripe_customer_id')
            .get(stripe_customer_id=kwargs['object'])
        )

        context['subscription'] = obj.get_plan_type_display()
        return context

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        customer = stripe.Customer.retrieve(str(self.request.user.customer))
        customer.delete()

        user = Customer.objects.get(user__username=self.request.user)
        user.stripe_customer_id = ''
        user.save()

        subscription = (
            Subscription.objects.select_related('stripe_customer_id')
            .get(stripe_customer_id=user)
        )
        subscription.delete()

        return redirect('/')


class SubscriptionMONView(LoginRequiredMixin, StripeMixin, FormView):
    """ Form with the subscription monthly plan """

    template_name = 'suscriptions/subscription_mon.html'
    form_class = SuscriptionForm

    def form_valid(self, form):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = self.request.POST['stripeToken']

        customer_data = {
            'description': 'Monthly Subscription customer',
            'card': token,
            'email': form.cleaned_data['email']

        }

        customer = stripe.Customer.create(**customer_data)
        user = Customer.objects.get(user__username=self.request.user)
        user.stripe_customer_id = customer.id
        user.save()

        suscription = Subscription.objects.get_or_create(
            plan_type='MONTHLY_PLAN',
            stripe_subscription_id='plan_DQaiAiiHgNxbId',
            stripe_customer_id=user,
            email=form.cleaned_data['email'],
            full_name=form.cleaned_data['full_name']
        )

        stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": suscription[0]
                }
            ]
        )
        return redirect('/')


class SubscriptionYEARView(LoginRequiredMixin, StripeMixin, FormView):
    """ Form with the subscription monthly plan """

    template_name = 'suscriptions/subscription_year.html'
    form_class = SuscriptionForm

    def form_valid(self, form):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = self.request.POST['stripeToken']

        customer_data = {
            'description': 'Annual Subscription customer',
            'card': token,
            'email': form.cleaned_data['email']

        }

        customer = stripe.Customer.create(**customer_data)
        user = Customer.objects.get(user__username=self.request.user)
        user.stripe_customer_id = customer.id
        user.save()

        suscription = Subscription.objects.get_or_create(
            plan_type='ANNUAL_PLAN',
            stripe_subscription_id='plan_DQbSOESCbSnlVG',
            stripe_customer_id=user,
            email=form.cleaned_data['email'],
            full_name=form.cleaned_data['full_name']
        )

        stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": suscription[0]
                }
            ]
        )
        return redirect('/')
