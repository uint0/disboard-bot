import azure.mgmt.compute.aio

import config
import util.azure


class ServerManager:
    def __init__(self, vm_name, group_name):
        self._group_name = group_name
        self._vm_name    = vm_name

        creds, subscription_id = util.azure.get_aio_credentials()
        self._creds_provider = creds
        self._client = azure.mgmt.compute.aio.ComputeManagementClient(creds, subscription_id)

    async def start(self):
        return await self._client.virtual_machines.begin_start(
            self._group_name,
            self._vm_name
        )

    async def stop(self):
        return await self._client.virtual_machines.begin_deallocate(
            self._group_name,
            self._vm_name
        )

    async def get_vm_instance_view(self):
        return await self._client.virtual_machines.instance_view(
            self._group_name,
            self._vm_name
        )

    async def close(self):
        await self._creds_provider.close()
        await self._client.close()
