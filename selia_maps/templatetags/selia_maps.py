from uuid import uuid4
import json

from django import template
from django.conf import settings
from django.utils.translation import gettext as _
from django.templatetags.static import static

from irekua_database.models import SamplingEvent
from irekua_database.models import SamplingEventDevice

from selia_maps.utils import point_features_from_sampling_event_device
from selia_maps.utils import point_features_from_sampling_event
from selia_maps.utils import point_features_from_site


register = template.Library()


VECTOR_LAYER = 'vector'
TILE_LAYER = 'tile'
IMAGE_LAYER = 'image'


@register.inclusion_tag('selia_maps/site.html')
def site_map(site):
    return {
        'latitude': site.latitude,
        'longitude': site.longitude,
        'zoom': 14,
        'map_id': 'map_{}_{}'.format(site.pk, str(uuid4())[:5])
    }


@register.inclusion_tag('selia_maps/site_no_controls.html')
def site_map_list(site):
    return {
        'latitude': site.latitude,
        'longitude': site.longitude,
        'zoom': 14,
        'width': '100%',
        'height': '100%',
        'map_id': 'map_{}_{}'.format(site.pk, str(uuid4())[:5])
    }


@register.inclusion_tag('selia_maps/map_with_layer_list.html')
def collection_site_map(collection_site):
    devices = [
        point_features_from_sampling_event_device(device, opacity=0.4)
        for device in collection_site.deployments.all()
    ]

    site = [
        point_features_from_site(collection_site.site, color='#900C3F')
    ]

    layer_list = [
        {
            'title': _('Deployed devices'),
            'type': VECTOR_LAYER,
            'features': devices
        },
        {
            'title': _('Collection Site'),
            'type': VECTOR_LAYER,
            'features': site
        }
    ]

    return {
        'latitude': collection_site.site.latitude,
        'longitude': collection_site.site.longitude,
        'zoom': 14,
        'map_id': 'map_{}_{}'.format(collection_site.pk, str(uuid4())[:5]),
        'layer_list': json.dumps(layer_list)
    }


@register.inclusion_tag('selia_maps/map_with_layer_list.html')
def sampling_event_map(sampling_event):
    devices = [
        point_features_from_sampling_event_device(device, opacity=0.8)
        for device in sampling_event.samplingeventdevice_set.all()
    ]

    near_sampling_event = [
        point_features_from_sampling_event(event, opacity=0.5)
        for event in (
            SamplingEvent.objects
            .filter(collection=sampling_event.collection)
            .exclude(pk=sampling_event.pk))
    ]

    sampling_event_point = [
        point_features_from_sampling_event(sampling_event, scale=0.08)
    ]

    layer_list = [
        {
            'title': _('Deployed devices'),
            'type': VECTOR_LAYER,
            'features': devices
        },
        {
            'title': _('Other sampling events'),
            'type': VECTOR_LAYER,
            'features': near_sampling_event
        },
        {
            'title': _('Sampling event'),
            'type': VECTOR_LAYER,
            'features': sampling_event_point
        }
    ]

    return {
        'latitude': sampling_event.collection_site.site.latitude,
        'longitude': sampling_event.collection_site.site.longitude,
        'zoom': 14,
        'map_id': 'map_{}_{}'.format(sampling_event.pk, str(uuid4())[:5]),
        'layer_list': json.dumps(layer_list)
    }


@register.inclusion_tag('selia_maps/map_with_layer_list.html')
def sampling_event_device_map(sampling_event_device):
    devices_points = [
        point_features_from_sampling_event_device(device, opacity=0.5)
        for device in (
            SamplingEventDevice.objects
            .filter(sampling_event=sampling_event_device.sampling_event)
            .exclude(pk=sampling_event_device.pk))
    ]

    sampling_event_point = [
        point_features_from_sampling_event(sampling_event_device.sampling_event, opacity=0.5)
    ]

    sampling_event_device_point = [
        point_features_from_sampling_event_device(sampling_event_device)
    ]

    layer_list = [
        {
            'title': _('Other deployed devices'),
            'type': VECTOR_LAYER,
            'features': devices_points
        },
        {
            'title': _('Sampling event site'),
            'type': VECTOR_LAYER,
            'features': sampling_event_point
        },
        {
            'title': _('Deployed device'),
            'type': VECTOR_LAYER,
            'features': sampling_event_device_point
        }
    ]

    return {
        'latitude': sampling_event_device.latitude,
        'longitude': sampling_event_device.longitude,
        'zoom': 14,
        'layer_list': json.dumps(layer_list),
        'map_id': 'map_{}_{}'.format(sampling_event_device.pk, str(uuid4())[:5]),
    }


@register.inclusion_tag('selia_maps/media.html')
def selia_map_media():
    return {}


@register.inclusion_tag('selia_maps/form_map.html')
def form_map(latitude_form, longitude_form, locality):
    longitude, latitude = settings.SELIA_MAPS_INITIAL_COORDINATES

    longitude_form_value = longitude_form.value()
    if longitude_form_value:
        longitude = longitude_form_value

    latitude_form_value = latitude_form.value()
    if latitude_form_value:
        latitude = latitude_form_value

    if locality:
        locality = locality.geometry.wkt

    return {
        'latitude': float(latitude),
        'longitude': float(longitude),
        'zoom': settings.SELIA_MAPS_INITIAL_ZOOM,
        'map_id': 'form_map',
        'latitude_form_id': str(latitude_form.auto_id),
        'longitude_form_id': str(longitude_form.auto_id),
        'locality': locality
    }


@register.inclusion_tag('selia_maps/sampling_event_form_map.html')
def sampling_event_form_map(latitude_form, longitude_form, sampling_event, collection_device):
    longitude = sampling_event.collection_site.site.longitude
    latitude = sampling_event.collection_site.site.latitude
    device_type = collection_device.physical_device.device.device_type

    longitude_form_value = longitude_form.value()
    if longitude_form_value:
        longitude = longitude_form_value

    latitude_form_value = latitude_form.value()
    if latitude_form_value:
        latitude = latitude_form_value

    devices_points = [
        point_features_from_sampling_event_device(device, opacity=0.4)
        for device in sampling_event.samplingeventdevice_set.all()
    ]

    sampling_event_point = [
        point_features_from_sampling_event(sampling_event, opacity=0.6)
    ]

    layer_list = [
        {
            'title': _('Other deployed devices'),
            'type': VECTOR_LAYER,
            'features': devices_points
        },
        {
            'title': _('Sampling event site'),
            'type': VECTOR_LAYER,
            'features': sampling_event_point
        }
    ]

    if device_type.icon:
        icon = device_type.icon.url
    else:
        icon = static('selia_maps/site.png')

    return {
        'latitude': float(latitude),
        'longitude': float(longitude),
        'zoom': 13,
        'map_id': 'form_map',
        'latitude_form_id': str(latitude_form.auto_id),
        'longitude_form_id': str(longitude_form.auto_id),
        'icon_url': icon,
        'layer_list': json.dumps(layer_list),
    }
