from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Customer(models.Model):
    """ Customer model """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    stripe_customer_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.stripe_customer_id


class Subscription(models.Model):
    """ Suscription model """

    plans = (
        ('FREE', 'Basic Plan'),
        ('MONTHLY_PLAN', 'Monthly Plan ($29/Mo)'),
        ('ANNUAL_PLAN', 'Annual Plan ($299/Yr)'),
    )

    stripe_subscription_id = models.CharField(max_length=100)
    stripe_customer_id = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    plan_type = models.CharField(max_length=15, choices=plans, default='FREE')
    initiated_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.stripe_subscription_id
