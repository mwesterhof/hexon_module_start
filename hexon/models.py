from django.db import models

from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail_app_pages.models import AppPageMixin
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageBlock
from wagtail.models import Page


class Vehicle(Page):
    hexon_id = models.CharField(max_length=200, unique=True)
    price = models.CharField(max_length=20)
    brand = models.CharField(max_length=200)

    images = StreamField([
            ('image', ImageBlock()),
        ], use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('images')
    ]

    hexon_panels = Page.settings_panels + [
        FieldPanel('hexon_id'),
        FieldPanel('price'),
        FieldPanel('brand'),
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


class VehicleStock(AppPageMixin, Page):
    url_config = 'hexon.urls'