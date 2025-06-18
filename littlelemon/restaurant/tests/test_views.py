from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from restaurant.models import Menu
from restaurant.serializers import MenuSerializer

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Create a token for that user
        self.token = Token.objects.create(user=self.user)
        # Authenticate client with token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create menu items
        self.item1 = Menu.objects.create(title="Burger", price=50, inventory=20)
        self.item2 = Menu.objects.create(title="Pizza", price=100, inventory=15)

    def test_getall(self):
        url = reverse('menu-items')
        response = self.client.get(url)
        items = Menu.objects.all()
        serializer = MenuSerializer(items, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)