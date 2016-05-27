from __future__ import print_function
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.limits import Limits
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.dotdict import dotdict

class LoadCommand(PluginCommand, CloudPluginCommand):
    topics = {"load": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command load")

    # noinspection PyUnusedLocal
    @command
    def do_load(self, args, arguments):
        """
        ::

            Usage:
                load MODULE


            ARGUMENTS:
               MODULE  The name of the module

            PREDEFINED MODULE NAMES:
               vbox    loads vbox command

            Examples:
                cm load cloudmesh_vagrant.cm_vbox.do_vbox
                    lists the plugins currently loaded

        """
        arg = dotdict(arguments)
        print(arg)

        if arg.MODULE == "vbox":
            arg.MODULE = "cloudmesh_vagrant.cm_vbox.do_vbox"

        try:
                print("LOADING VBOX", arg.MODULE)
                arg.MODULE = "cloudmesh_vagrant.cm_vbox.do_vbox"
                from pydoc import locate
                # f = locate(arg.MODULE)
                # print (f)
                self.load_instancemethod(arg.MODULE)

        except:
            Console.error("Problem loading module {}".format(arg.MODULE),
                          traceflag=True)
        return ""



