from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Customer, Subscription


class CustomerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='ikenshu')
        Customer.objects.create(user=self.user, stripe_customer_id='key_from_strip_api')

    def test_stripe_customer_id_max_lenght(self):
        customer = Customer.objects.get(user__username=self.user.username)
        max_length = customer._meta.get_field('stripe_customer_id').max_length
        self.assertEquals(max_length, 100)

    def test_stripe_customer_id_label(self):
        customer = Customer.objects.get(user__username=self.user.username)
        field_label = customer._meta.get_field('stripe_customer_id').verbose_name
        self.assertEquals(field_label, 'stripe customer id')


class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='ikenshu')
        customer = Customer.objects.create(user=self.user, stripe_customer_id='key_from_strip_api')
        Subscription.objects.create(
            stripe_subscription_id='subscription_plan_from_stripe_api',
            stripe_customer_id=customer,
            plan_type='MONTHLY_PLAN',
            full_name='Fulanito Zutano',
            email='f@zutano.com'
        )

    def test_stripe_subscription_id_max_lenght(self):
        subscription = Subscription.objects.get(
            stripe_subscription_id='subscription_plan_from_stripe_api'
        )

        max_length = subscription._meta.get_field('stripe_subscription_id').max_length
        self.assertEquals(max_length, 100)

    def test_plan_type_label(self):
        subscription = Subscription.objects.get(
            stripe_subscription_id='subscription_plan_from_stripe_api'
        )
        field_label = subscription._meta.get_field('plan_type').verbose_name
        self.assertEquals(field_label, 'plan type')

    def test_plan_type_display(self):
        subscription = Subscription.objects.get(
            stripe_subscription_id='subscription_plan_from_stripe_api'
        )
        plan_type_display = subscription.get_plan_type_display()
        self.assertEquals(plan_type_display, 'Monthly Plan ($29/Mo)')

    def test_full_name_max_lenght(self):
        subscription = Subscription.objects.get(
            stripe_subscription_id='subscription_plan_from_stripe_api'
        )
        max_length = subscription._meta.get_field('full_name').max_length
        self.assertEquals(max_length, 255)

    def test_email_max_lenght(self):
        subscription = Subscription.objects.get(
            stripe_subscription_id='subscription_plan_from_stripe_api'
        )
        max_length = subscription._meta.get_field('email').max_length
        self.assertEquals(max_length, 255)
