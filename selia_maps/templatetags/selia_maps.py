from uuid import uuid4
import json

from django import template
from django.conf import settings
from irekua_database.models import SamplingEvent
from irekua_database.models import SamplingEventDevice

from selia_maps.utils import point_features_from_sampling_event_device
from selia_maps.utils import point_features_from_sampling_event
from selia_maps.utils import point_features_from_site


register = template.Library()


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


@register.inclusion_tag('selia_maps/map_with_point_list.html')
def collection_site_map(collection_site):
    point_list = [
        point_features_from_sampling_event_device(device, opacity=0.4)
        for device in collection_site.deployments.all()
    ] + [
        point_features_from_site(collection_site.site, color='#900C3F')
    ]

    return {
        'latitude': collection_site.site.latitude,
        'longitude': collection_site.site.longitude,
        'zoom': 14,
        'map_id': 'map_{}_{}'.format(collection_site.pk, str(uuid4())[:5]),
        'point_list': json.dumps(point_list)
    }


@register.inclusion_tag('selia_maps/map_with_point_list.html')
def sampling_event_map(sampling_event):
    point_list = [
        point_features_from_sampling_event_device(device, opacity=0.8)
        for device in sampling_event.samplingeventdevice_set.all()
    ] + [
        point_features_from_sampling_event(event, opacity=0.5)
        for event in (
            SamplingEvent.objects
            .filter(collection=sampling_event.collection)
            .exclude(pk=sampling_event.pk))
    ] + [
        point_features_from_sampling_event(sampling_event)
    ]

    return {
        'latitude': sampling_event.collection_site.site.latitude,
        'longitude': sampling_event.collection_site.site.longitude,
        'zoom': 14,
        'map_id': 'map_{}_{}'.format(sampling_event.pk, str(uuid4())[:5]),
        'point_list': json.dumps(point_list)
    }


@register.inclusion_tag('selia_maps/map_with_point_list.html')
def sampling_event_device_map(sampling_event_device):
    point_list = [
        point_features_from_sampling_event_device(device, opacity=0.5)
        for device in (
            SamplingEventDevice.objects
            .filter(sampling_event=sampling_event_device.sampling_event)
            .exclude(pk=sampling_event_device.pk))
    ] + [
        point_features_from_sampling_event(sampling_event_device.sampling_event, opacity=0.5)
    ] + [
        point_features_from_sampling_event_device(sampling_event_device)
    ]

    return {
        'latitude': sampling_event_device.latitude,
        'longitude': sampling_event_device.longitude,
        'zoom': 14,
        'point_list': json.dumps(point_list),
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

    point_list = [
        point_features_from_sampling_event_device(device, opacity=0.4)
        for device in sampling_event.samplingeventdevice_set.all()
    ] + [
        point_features_from_sampling_event(sampling_event, opacity=0.6)
    ]

    return {
        'latitude': float(latitude),
        'longitude': float(longitude),
        'zoom': 13,
        'map_id': 'form_map',
        'latitude_form_id': str(latitude_form.auto_id),
        'longitude_form_id': str(longitude_form.auto_id),
        'icon_url': device_type.icon.url,
        'point_list': json.dumps(point_list),
    }
