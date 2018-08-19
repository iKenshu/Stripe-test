from django.contrib import admin

from .models import Subscription, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """ Customer register on admin """

    list_display = ('user', 'stripe_customer_id')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """ Subscription register on admin """

    list_display = ('stripe_customer_id', 'plan_type', 'full_name', 'email', 'initiated_on')
