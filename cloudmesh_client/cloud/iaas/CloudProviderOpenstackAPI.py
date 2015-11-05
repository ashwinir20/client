from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict

from keystoneclient.auth.identity import v3
from keystoneclient import session
from novaclient import client
import requests

from cloudmesh_client.common.Printer import attribute_printer
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.cloud.nova import Nova
from pprint import pprint

requests.packages.urllib3.disable_warnings()


# TODO: unset as not allowing to smoothly switch
def set_os_environ(cloudname):
    """Set os environment variables on a given cloudname"""
    # TODO: this has a severe bug as it is not unsetting variabes
    # Also this coded duplicates in part from register
    try:
        d = ConfigDict("cloudmesh.yaml")
        credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
        for key, value in credentials.iteritems():
            if key == "OS_CACERT":
                os.environ[key] = Config.path_expand(value)
            else:
                os.environ[key] = value
    except Exception, e:
        print(e)


#
# we already have a much better convert to dict function
#


class CloudProviderOpenstackAPI(CloudProviderBase):
    def __init__(self, cloud_name, cloud_details, user=None):
        super( CloudProviderOpenstackAPI, self ).__init__(cloud_name, user=user)
        self.initialize(cloud_name, cloud_details)

    def _to_dict(self, openstack_result):
        d = {}

        for i in enumerate(openstack_result):
            print i

        for index, value in enumerate(openstack_result):
            print index, value
            d[index] = value.__dict__["_info"]
            del d[index]['links']

        return d

    def _ksv3_auth(self, credentials):
        # auth to identity v3
        ksauth = v3.Password(
            auth_url=credentials["OS_AUTH_URL"],
            username=credentials["OS_USERNAME"],
            password=credentials["OS_PASSWORD"],
            project_name=credentials["OS_PROJECT_NAME"],
            user_domain_name=credentials["OS_USER_DOMAIN_ID"],
            project_domain_name=credentials["OS_PROJECT_DOMAIN_ID"])

        return ksauth

    def initialize(self, cloud_name, user=None):

        d = ConfigDict("cloudmesh.yaml")
        cloud_details = d["cloudmesh"]["clouds"][cloud_name]

        pprint (cloud_details)

        self.cloud = cloud_name
        self.default_flavor = cloud_details["default"]["flavor"]
        self.default_image = cloud_details["default"]["image"]
        version = 2
        credentials = cloud_details["credentials"]
        cert = False
        if "OS_CACERT" in credentials:
            if credentials["OS_CACERT"] is not False:
                cert = Config.path_expand(credentials["OS_CACERT"])
        auth_url = credentials["OS_AUTH_URL"]
        ksversion = auth_url.split("/")[-1]

        if "v2.0" == ksversion:
            self.provider = client.Client(
                version,
                credentials["OS_USERNAME"],
                credentials["OS_PASSWORD"],
                credentials["OS_TENANT_NAME"],
                credentials["OS_AUTH_URL"],
                cert)
        elif "v3" == ksversion:
            sess = session.Session(auth=self._ksv3_auth(credentials),
                                   verify=cert)
            self.provider = client.Client(2, session=sess)

    def mode(self, source):
        """
        Sets the source for the information to be returned. "db" and "cloud"
        :param source: the database can be queried in mode "db",
        the database can be bypassed in mode "cloud"
        """
        TODO.implement()


    def list_flavor(self, cloudname, **kwargs):
        return self._to_dict(self.provider.flavors.list())

    def list_image(self, cloudname, **kwargs):
         return self._to_dict(self.provider.images.list())

    def list_vm(self, cloudname, **kwargs):
        return self._to_dict(self.provider.servers.list())

    def list_limits(self, cloudname, **kwargs):
        raise ValueError ("list limits is not supported")

    def list_quota(self, cloudname, **kwargs):
        raise ValueError ("list quota is not supported")

    def list_usage(self, cloudname, **kwargs):
        raise ValueError ("list usage is not supported")


    def boot(self, name, image=None, flavor=None, cloud="India", key=None,
             secgroup=None, meta=None):
        """
        Spawns a VM instance on the cloud.
        If image and flavor passed as none, it would consider the defaults specified in cloudmesh.yaml.

        :param name: Name of the instance to be started
        :param image: Image id to be used for the instance
        :param flavor: Flavor to be used for the instance
        :param cloud: Cloud on which to spawn the machine. Defaults to 'India'.
        :param key: Key to be used for the instance
        :param secgroup: Security group for the instance
        :param meta: A dict of arbitrary key/value metadata to store for this server
        """
        if image is None:
            image = self.default_image
        if flavor is None:
            flavor = self.default_flavor

        server = self.provider.servers.create(name, image, flavor, meta=meta,
                                          key_name=key,
                                          security_groups=secgroup)
        # return the server id
        return server.__dict__["id"]

    def delete(self, name, group=None, force=None):
        """
        Deletes a machine on the target cloud indicated by the id
        :param id: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """
        server = self.provider.servers.find(name=name)
        server.delete()

    def get_ips(self, name, group=None, force=None):
        """
        Returns the ip of the instance indicated by name_or_id
        :param name_or_id:
        :param group:
        :param force:
        :return: IP address of the instance
        """
        server = self.provider.servers.find(name=name)
        return self.provider.servers.ips(server)

    def create_assign_floating_ip(self, server_name):
        """
        Function creates a new floating ip and associates it with the machine specified.
        :param server_name: Name of the machine to which the floating ip needs to be assigned.
        :return: Floating IP | None if floating ip already assigned.
        """

        float_pool = self.provider.floating_ip_pools.list()[0].name

        floating_ip = self.provider.floating_ips.create(pool=float_pool)
        server = self.provider.servers.find(name=server_name)
        try:
            server.add_floating_ip(floating_ip)
        except Exception, e:
            print (e)
            self.provider.floating_ips.delete(floating_ip)
            return None

        return floating_ip.ip

    # TODO: define this
    def get_image(self, **kwargs):
        """
        finds the image based on a query
        TODO: details TBD
        """
        TODO.implement()

    # TODO: define this
    def get_flavor(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        TODO.implement()

    # TODO: define this
    def get_vm(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        TODO.implement()

    @classmethod
    def list_limits(self, cloud, output="table", tenant=None):
        try:
            # nova = CloudProvider.setet((cloud)
            result = self.provider.limits.get(tenant_id=tenant)._info[
                "absolute"]
            return attribute_printer(result, output=output)
        except Exception, e:
            return e


    def attributes(self, kind):
        header = None
        order = None
        if kind == 'flavor':
            order = [
                'id',
                'name',
                'cm_cloud',
                'disk',
                'ephemeral_disk',
                'ram',
                'vcpus'
            ]
        elif kind == 'default':
            order = ['user',
                     'cloud',
                     'name',
                     'value',
                     'created_at',
                     'updated_at'
                     ]
        elif kind == 'image':
            order = [
                'cm_cloud',
                'cm_user',
                'instance_type_ephemeral_gb',
                'instance_type_flavorid',
                'instance_type_id',
                'instance_type_memory_mb',
                'instance_type_name',
                'instance_type_root_gb',
                'instance_type_rxtx_factor',
                'instance_type_swap',
                'instance_type_vcpus',
                'minDisk',
                'minRam',
                'name',
            ]
            header = [
                'cloud',
                'user',
                'ephemeral_gb',
                'flavorid',
                'id',
                'memory_mb',
                'flavor',
                'root_gb',
                'rxtx_factor',
                'swap',
                'vcpus',
                'minDisk',
                'minRam',
                'name',
            ]
        return (order, header)
