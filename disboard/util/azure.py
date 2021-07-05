import collections

import azure.identity

import config

ResourceDescriptor = collections.namedtuple('ResoucDescriptor', [
    'subscription',
    'group',
    'provider',
    'type',
    'name'
])

def get_credentials():
    subscription_id = config.azure.AZURE_SUBSCRIPTION_ID
    credentials = azure.identity.DefaultAzureCredential()
    return credentials, subscription_id


def derive_resource_descriptor(resource_full_id):
    resource_parts = resource_full_id.split('/', 8)[1:]
    subscription_id = None
    group = None
    provider = None
    rsrc_type = None
    name = None

    try:
        if resource_parts.pop(0) != 'subscriptions':
            raise ValueError("Resource id is missing subsciption")
        else:
            subscription_id = resource_parts.pop(0)
        
        if resource_parts.pop(0) != 'resourcegroups':
            raise ValueError("Resource id is missing resourcegroups")
        else:
            group = resource_parts.pop(0)
        
        if resource_parts.pop(0) != 'providers':
            raise ValueError("Resource id is missing providers")
        else:
            provider = resource_parts.pop(0)
        
        rsrc_type = resource_parts.pop(0)
        name = resource_parts.pop(0)
    except IndexError:
        pass

    return ResourceDescriptor(
        subscription=subscription_id,
        group=group,
        provider=provider,
        type=rsrc_type,
        name=name
    )


def resource_short_name(resource_full_id):
    descriptor = derive_resource_descriptor(resource_full_id)
    return f"{descriptor.type}/{descriptor.name}"
