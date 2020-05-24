from django.utils.translation import gettext as _
from django.templatetags.static import static


def point_features_from_sampling_event(sampling_event, **kwargs):
    collection_site = sampling_event.collection_site
    site = collection_site.site
    sampling_event_type = sampling_event.sampling_event_type

    if sampling_event_type.icon:
        icon = sampling_event_type.icon.url
    else:
        icon = static('selia_maps/site.png')

    features = {
        "type": "point",
        "coordinates": [
            site.longitude,
            site.latitude
        ],
        "style": {
            "image": {
                "url": icon,
                "scale": "0.06"
            }
        },
        "name": _("Sampling event {}").format(sampling_event.pk)
    }

    for key, value in kwargs.items():
        features["style"]["image"][key] = value

    return features


def point_features_from_sampling_event_device(sampling_event_device, **kwargs):
    collection_device = sampling_event_device.collection_device
    physical_device = collection_device.physical_device
    device = physical_device.device
    device_type = device.device_type

    if device_type.icon:
        icon = device_type.icon.url
    else:
        icon = static('selia_maps/site.png')

    features = {
        "type": "point",
        "coordinates": [
            sampling_event_device.longitude,
            sampling_event_device.latitude
        ],
        "style": {
            "image": {
                "url": icon,
                "scale": "0.06"
            }
        },
        "name": _('Deployed device {}').format(sampling_event_device.pk)
    }

    for key, value in kwargs.items():
        features["style"]["image"][key] = value

    return features


def point_features_from_site(site, **kwargs):
    features = {
        "type": "point",
        "coordinates": [
            site.longitude,
            site.latitude
        ],
        "style": {
            "image": {
                "url": static('selia_maps/site.png'),
                "scale": "0.06"
            }
        },
        "name": _('Site {}').format(site.pk)
    }

    for key, value in kwargs.items():
        features["style"]["image"][key] = value

    return features
