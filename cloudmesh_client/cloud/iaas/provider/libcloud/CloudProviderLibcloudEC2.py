from __future__ import print_function
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security
import os
from pprint import pprint
from uuid import UUID
import re
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.common.FlatDict import FlatDict
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase

from cloudmesh_client.cloud.iaas.provider.libcloud.CloudProviderLibcloud import CloudProviderLibcloud


class CloudProviderLibcloudEC2(CloudProviderLibcloud):
    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderLibcloudEC2, self).__init__(cloud_name, cloud_details, user=user)
        self.flat = flat
        self.cloud_type = "libcloud"
        self.kind = ["image"]
        self.cloudname = cloud_name
        self.initialize(cloud_name)

    def initialize(self, cloudname, user=None):

        pprint("Initializing libcloud-ec2 for " + cloudname)
        cls = get_driver(Provider.EC2_US_EAST)

        d = ConfigDict("cloudmesh.yaml")
        self.cloud_details = d["cloudmesh"]["clouds"][cloudname]
        credentials = self.cloud_details["credentials"]
        auth_url = credentials["EC2_URL"]
        pprint("Auth url is " + auth_url)
        searchobj = re.match(r'^http[s]?://(.+):([0-9]+)/([a-zA-Z/]*)',
                             auth_url,
                             re.M | re.I)

        path = None
        host = None
        port = None
        if searchobj:
            print ("searchObj.group() : ", searchobj.group())
            print ("host : ", searchobj.group(1))
            host = searchobj.group(1)
            print ("port : ", searchobj.group(2))
            port = searchobj.group(2)
            print ("path : ", searchobj.group(3))
            path = searchobj.group(3)
        else:
            # TODO: better error description.
            print ("Nothing found. failed.")

        # if libcloudname == "ec2" :
        # url_split=auth_url.split("/:")

        ec2_access_key = credentials['EC2_ACCESS_KEY']
        ec2_secret_key = credentials['EC2_SECRET_KEY']
        # ec2_auth_url=

        extra_args = {'path': path}

        # TODO: do something if the host is None

        # AWS needs two values for authentication
        self.provider = cls(ec2_access_key,
                            ec2_secret_key,
                            host=host,
                            port=port,
                            **extra_args)
