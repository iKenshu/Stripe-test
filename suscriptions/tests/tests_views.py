from django.contrib.auth.models import User

from django.urls import reverse

from django.test import TestCase

from ..models import Subscription, Customer


class HomeTest(TestCase):

    def test_home_view_with_name_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_home_view_with_url_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suscriptions/suscriptions.html')


class SubscriptionTest(TestCase):

    def setUp(self):
        self.user_test = User.objects.create_user(
            username='Fulanito',
            password='fulanitosuperpoderoso'
        )
        self.customer = Customer.objects.create(
            user=self.user_test,
            stripe_customer_id='cus_xxxxxxxxxxxxxx'
        )

    def test_subscription_monthly_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('subscription-mon'))
        self.assertRedirects(response, '/login/?next=/monthly/')

    def test_subscription_monthly_logged_in_uses_correct_template(self):
        self.client.login(username='Fulanito', password='fulanitosuperpoderoso')

        response = self.client.get(reverse('subscription-mon'))

        self.assertEqual(str(response.context['user']), 'Fulanito')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suscriptions/subscription_mon.html')

    def test_subscription_monthly_view_csrf(self):
        self.client.login(username='Fulanito', password='fulanitosuperpoderoso')

        response = self.client.get(reverse('subscription-mon'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_subscription_year_redirect_if_not_logged_in(self):

        response = self.client.get(reverse('subscription-year'))
        self.assertRedirects(response, '/login/?next=/annual/')

    def test_subscription_year_logged_in_uses_correct_template(self):
        self.client.login(username='Fulanito', password='fulanitosuperpoderoso')

        response = self.client.get(reverse('subscription-year'))

        self.assertEqual(str(response.context['user']), 'Fulanito')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suscriptions/subscription_year.html')


class CustomerTest(TestCase):

    def test_customer_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_customer_signup_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'suscriptions/customer_create.html')

    def test_customer_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_customer_login_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'suscriptions/customer_login.html')
