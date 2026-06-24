from django.http.response import HttpResponse
import requests

from django.core.files.images import ImageFile
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from io import BytesIO
from wagtail.models import Collection
from wagtail.images.models import Image

from hexon.models import Vehicle, VehicleImage

from .parser import parse

def create_or_get_images(hexon_id, image_data):
    try:
        stock_collection = Collection.objects.get(depth=2, name='stock')
    except Collection.DoesNotExist:
        stock_collection = Collection.objects.get(depth=1).add_child(name='stock')

    try:
        collection = stock_collection.get_children().get(name=hexon_id)
    except Collection.DoesNotExist:
        collection = stock_collection.add_child(name=hexon_id)

    hexon_names = [i['name'] for i in image_data]
    Image.objects.filter(collection=collection).exclude(title__in=hexon_names).delete()
    already_imported_names = Image.objects.filter(collection=collection, title__in=hexon_names).values_list('title', flat=True)
    result = []

    for hexon_image in image_data:
        if hexon_image['name'] in already_imported_names:
            result.append(Image.objects.get(collection=collection, title=hexon_image['name']))
            continue

        image_data = requests.get(hexon_image['url']).content
        image_object = Image(
            title=hexon_image['name'],
            file=ImageFile(BytesIO(image_data), name=hexon_image['name']),
            collection=collection
        )
        image_object.save()
        result.append(image_object)

    return result

@transaction.atomic
def create_vehicle(parent_page, data):
    images = create_or_get_images(data['hexon_id'], data.pop('images'))

    if vehicle_qs := Vehicle.objects.child_of(parent_page).filter(hexon_id=data.get('hexon_id')):
        data.pop('hexon_id')
        vehicle_qs.update(**data)
        vehicle = vehicle_qs.get()
    else:
        vehicle = parent_page.add_child(instance=Vehicle(**data))
    vehicle.images.all().delete()
    for image in images:
        VehicleImage.objects.create(
            page=vehicle,
            image=image
        )
    return vehicle


class HexonMutateView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = parse(request.body)
        create_vehicle(self.parent_page, data)
        return HttpResponse(b"1")