from django.utils.translation import gettext as _
from django.templatetags.static import static


def point_features_from_sampling_event(sampling_event, **kwargs):
    collection_site = sampling_event.collection_site
    site = collection_site.site
    sampling_event_type = sampling_event.sampling_event_type

    features = {
        "coordinates": [
            site.longitude,
            site.latitude
        ],
        "icon_url": sampling_event_type.icon.url,
        "name": _("Sampling event {}").format(sampling_event.pk)
    }

    features.update(kwargs)
    return features


def point_features_from_sampling_event_device(sampling_event_device, **kwargs):
    collection_device = sampling_event_device.collection_device
    physical_device = collection_device.physical_device
    device = physical_device.device
    device_type = device.device_type

    features = {
        "coordinates": [
            sampling_event_device.longitude,
            sampling_event_device.latitude
        ],
        "icon_url": device_type.icon.url,
        "name": _('Deployed device {}').format(sampling_event_device.pk)
    }

    features.update(kwargs)
    return features


def point_features_from_site(site, **kwargs):
    features = {
        "coordinates": [
            site.longitude,
            site.latitude
        ],
        "icon_url": static('selia_maps/site.png'),
        "name": _('Site {}').format(site.pk)
    }

    features.update(kwargs)
    return features
