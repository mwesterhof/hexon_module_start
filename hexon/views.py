from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from hexon.models import Vehicle

from .parser import parse


class HexonMutateView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = parse(request.body)

        if vehicle_qs := Vehicle.objects.child_of(self.parent_page).filter(hexon_id=data.get('hexon_id')):
            data.pop('hexon_id')
            vehicle_qs.update(**data)
            vehicle = vehicle_qs.get()
        else:
            vehicle = self.parent_page.add_child(instance=Vehicle(**data))
        import ipdb; ipdb.set_trace()