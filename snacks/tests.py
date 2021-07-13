from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Snack

# Create your tests here.


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="suhaib", email="suhaibabdennabi33@gmail.com", password="password"
        )

        self.snack = Snack.objects.create(
            title="mansaf",
            description="meat",
            purchaser=self.user,
        )


    def test_string_representation(self):
        self.assertEqual(str(self.snack), "mansaf")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "mansaf")
        self.assertEqual(f"{self.snack.description}", "meat")
        self.assertEqual(f"{self.snack.purchaser}", "suhaib")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "mansaf")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/10/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Ordered By: suhaib")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "burger",
                "description": "meet with bread",
                "purchaser": self.user.id,
            }, follow=True
        )
        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Order: burger")
    
    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)
