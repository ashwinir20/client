""" run with

python setup.py install; nosetests -v --nocapture  tests/test_scripts.py

nosetests -v --nocapture tests/test_scripts.py

or

nosetests -v tests/test_scripts.py

"""
from __future__ import print_function

from cloudmesh_client.util import HEADING
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import banner

def run(command):
    banner(command)
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_script():
    """tests script command"""

    data = {
        "cloud": "kilo",
        "group": "mygroup"
    }

    def setup(self):
        self.scripts = [
            #("bash.cm", "README.rst"),
            #("comment.cm", "/* test"),
            #("var.cm", "time ="),
            #("py.cm", "2"),
            #("terminal.cm", ""),
            #("hpc.cm", "bravo"),

            #("cloud.cm", ""),
            #("cluster.cm", ""),
            #("demo.cm", ""),
            #("group.cm", ""),
            ("key.cm", ""),
            #("network.cm", ""),
            #("nova.cm", ""),
            #("reservedemo.cm", ""),
            #("secgroup.cm", ""),

            # BROKEN:
            #("sync.cm", ""),

            #("vm.cm", ""),
        ]
        pass

    def test_001(self):
        """
        cm script set india
        """

        HEADING()
        cloud = "india"
        data = {}
        for data["script"], data["check"] in self.scripts:
            command = "cm scripts/{script}".format(**data)
            result = run(command)
            print (result)
            assert data["check"] in result


