from wagtail.models import Page

from hexon.models import VehicleBase, VehicleStockBase


class HomePage(Page):
    subpage_types = ['home.VehicleStock']


class Vehicle(VehicleBase):
    subpage_types = []
    parent_page_types = ['home.VehicleStock']


class VehicleStock(VehicleStockBase):
    subpage_types = ['home.VehicleStock']
    parent_page_types = ['home.HomePage']