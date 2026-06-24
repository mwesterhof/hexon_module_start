from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel, HelpPanel, InlinePanel, ObjectList, TabbedInterface
from wagtail_app_pages.models import AppPageMixin
from wagtail.images.models import Image
from wagtail.models import Orderable, Page
from wagtail.search import index


class Vehicle(Page):
    hexon_id = models.CharField(max_length=200, unique=True)
    price = models.CharField(max_length=20)
    brand = models.CharField(max_length=200)
    accessories = models.JSONField()
    axleconfig_svg = models.CharField(max_length=2048, null=True)

    content_panels = Page.content_panels + [
        InlinePanel('images')
    ]

    hexon_panels = Page.settings_panels + [
        FieldPanel('hexon_id'),
        FieldPanel('price'),
        FieldPanel('brand'),
        HelpPanel(template='hexon/admin/accessories.html'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('hexon_id'),
        index.SearchField('brand'),
        index.SearchField('accessories'),
        index.FilterField('price'),
    ]

Vehicle.edit_handler = TabbedInterface(
    [
        ObjectList(Vehicle.content_panels, heading="Content"),
        ObjectList(Vehicle.promote_panels, heading="Promote"),
        ObjectList(Vehicle.settings_panels, heading="Settings"),
        ObjectList(Vehicle.hexon_panels,  heading="Hexon data"),
    ],
    base_form_class=WagtailAdminPageForm,
)


class VehicleImage(Orderable):
    page = ParentalKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='+')

    panels = [
        FieldPanel('image')
    ]


class VehicleStock(AppPageMixin, Page):
    url_config = 'hexon.urls'