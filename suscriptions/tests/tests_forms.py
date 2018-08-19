from django.test import TestCase
from django.contrib.auth.models import User

from ..forms import SuscriptionForm
from ..models import Customer, Subscription


class SubscriptionTest(TestCase):

    def test_valid_form(self):
        self.user = User.objects.create_user(username='fuzatano', password='fulanitosuperpoderoso')
        customer = Customer.objects.create(user=self.user, stripe_customer_id='cus_xxxxxxxxxxxxxx')

        full_name = 'Fulanito Zutano'
        email = 'f@zutano.com'
        obj = Subscription.objects.create(
            stripe_subscription_id='plan_xxxxxxxxxxxxxx',
            stripe_customer_id=customer,
            plan_type='MONTHLY_PLAN',
            full_name=full_name,
            email=email
        )
        data = {
            'stripe_subscription_id': obj.stripe_subscription_id,
            'stripe_customer_id': obj.stripe_customer_id,
            'plan_type': obj.plan_type,
            'full_name': obj.full_name,
            'email': obj.email
        }

        form = SuscriptionForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('full_name'), full_name)
        self.assertEqual(form.cleaned_data.get('email'), email)
