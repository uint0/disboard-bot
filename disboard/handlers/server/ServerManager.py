import azure.identity
import azure.mgmt.compute

import config

def get_credentials():
    subscription_id = config.azure.AZURE_SUBSCRIPTION_ID
    credentials = azure.identity.DefaultAzureCredential()
    return credentials, subscription_id


class ServerManager:
    def __init__(self, vm_name, group_name):
        self._group_name = group_name
        self._vm_name    = vm_name

        creds, subscription_id = get_credentials()
        self._client = azure.mgmt.compute.ComputeManagementClient(creds, subscription_id)

    def start(self):
        return self._client.virtual_machines.begin_start(
            self._group_name,
            self._vm_name
        )

    def stop(self):
        return self._client.virtual_machines.begin_deallocate(
            self._group_name,
            self._vm_name
        )

    def get_vm_instance_view(self):
        return self._client.virtual_machines.instance_view(
            self._group_name,
            self._vm_name
        )
    

    @staticmethod
    def wait(self, waiter):
        return waiter.wait()
