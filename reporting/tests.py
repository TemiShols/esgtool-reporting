from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import FuelModel, ElectricityModel, WasteModel, HeatingModelEmission


class CalculateFuelEmissionsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_calculate_fuel_emissions_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('calculate_fuel_emissions'), data={})
        self.assertEqual(response.status_code, 200)  # Assuming the form is invalid, so it returns the form page

    def test_calculate_fuel_emissions_view_not_logged_in(self):
        response = self.client.post(reverse('calculate_fuel_emissions'), data={})
        self.assertEqual(response.status_code, 302)


class CalculateWasteEmissionsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_calculate_waste_emissions_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('calculate_waste_emissions'), data={})
        self.assertEqual(response.status_code, 200)

    def test_calculate_waste_emissions_view_not_logged_in(self):
        response = self.client.post(reverse('calculate_waste_emissions'), data={})
        self.assertEqual(response.status_code, 302)


class CalculateElectricityEmissionsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_calculate_electricity_emissions_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('calculate_electricity_emissions'), data={})
        self.assertEqual(response.status_code, 200)

    def test_calculate_electricity_emissions_view_not_logged_in(self):
        response = self.client.post(reverse('calculate_electricity_emissions'), data={})
        self.assertEqual(response.status_code, 302)  # should redirect to login page


class CalculateChpEmissionsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_calculate_chp_emissions_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('calculate_chp_emissions'), data={})
        self.assertEqual(response.status_code, 200)

    def test_calculate_chp_emissions_view_not_logged_in(self):
        response = self.client.post(reverse('calculate_chp_emissions'), data={})
        self.assertEqual(response.status_code, 302)


class CalculateHomeHeatEmissionsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_calculate_home_heat_emissions_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('calculate_home_heat_emissions'), data={})
        self.assertEqual(response.status_code, 200)

    def test_calculate_home_heat_emissions_view_not_logged_in(self):
        response = self.client.post(reverse('calculate_home_heat_emissions'), data={})
        self.assertEqual(response.status_code, 302)

class ViewEmissionsViewTests(TestCase):
    def test_view_emissions_view(self):
        fuel_model = FuelModel.objects.create(...)  # Create a fuel model instance
        response = self.client.get(reverse('view_emissions', args=(fuel_model.pk,)))
        self.assertEqual(response.status_code, 200)


class ViewElectricityEmissionsViewTests(TestCase):
    def test_view_electricity_emissions_view(self):
        electricity_model = ElectricityModel.objects.create(...)
        response = self.client.get(reverse('view_electricity_emissions', args=(electricity_model.pk,)))
        self.assertEqual(response.status_code, 200)


class ViewWasteEmissionsViewTests(TestCase):
    def test_view_waste_emissions_view(self):
        waste_model = WasteModel.objects.create(...)
        response = self.client.get(reverse('view_waste_emissions', args=(waste_model.pk,)))
        self.assertEqual(response.status_code, 200)


class ViewChpEmissionsViewTests(TestCase):
    def test_view_chp_emissions_view(self):
        chp_model = HeatingModelEmission.objects.create(...)
        response = self.client.get(reverse('view_chp_emissions', args=(chp_model.pk,)))
        self.assertEqual(response.status_code, 200)
