from django.db import models

from wagtail.models import Page

from hexon.models import Vehicle as BaseVehicle, VehicleStock as BaseVehicleStock


class HomePage(Page):
    subpage_types = ['home.VehicleStock']


class Vehicle(BaseVehicle):
    subpage_types = []
    parent_page_types = ['home.VehicleStock']


class VehicleStock(BaseVehicleStock):
    subpage_types = ['home.VehicleStock']
    parent_page_types = ['home.HomePage']