from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import dict_printer, attribute_printer, \
    list_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.list import List
from pprint import pprint


class Hpc(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the hpc list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        return cls.cm.refresh('hpc', cloud)

    @classmethod
    def list(cls, cloud, live=False, format="table"):
        """
        This method lists all hpcs of the cloud
        :param cloud: the cloud name
        """
        # cm = CloudmeshDatabase()
        try:

            if live:
                cls.refresh(cloud)

            elements = cls.cm.find("hpc", cloud=cloud)

            # pprint(elements)

            (order, header) = CloudProvider(cloud).get_attributes("hpc")

            return dict_printer(elements,
                                order=order,
                                header=header,
                                output=format)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):
        if live:
            cls.refresh(cloud)

        return CloudProvider(cloud).details('hpc', cloud, id, format)


if __name__ == "__main__":
    Hpc.details("juno", "58c9552c-8d93-42c0-9dea-5f48d90a3188")

