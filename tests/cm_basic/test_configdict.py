""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_configdict.py:Test_configdict.test_001

nosetests -v --nocapture tests/cm_basic/test_configdict.py

or

nosetests -v tests/cm_basic/test_configdict.py

"""
from __future__ import print_function
from cloudmesh_client.util import HEADING
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell
import shutil
import os

class Test_configdict:

    root_path = os.path.abspath(os.sep)
    cwd_path = os.getcwd()

    def setup(self):
        os.system("cm help")
        self.etc_yaml = os.path.join(self.cwd_path, "cloudmesh_client", "etc", "cloudmesh.yaml")
        self.tmp_yaml = os.path.join(self.root_path, "tmp", "cloudmesh.yaml")
        self.tmp_dir = os.path.join(self.root_path, "tmp")
        pass

    def tearDown(self):
        pass

    def test_001_read(self):
        """test if cloudmesh.yaml is loaded"""
        HEADING()
        d = ConfigDict("cloudmesh.yaml",
                       verbose=True)

        assert d["cloudmesh"]["profile"]["firstname"] == "TBD"

        try:
            d = ConfigDict("cloudmesh.yam",
                           verbose=True)
            print("the file cloudmesh.yam should not exists")
            assert False
        except Exception as e:
            assert str(e).startswith("could not find")

    def test_002_set(self):
        """testing to set a value in the dict"""
        HEADING()
        shutil.copy(self.etc_yaml,self.tmp_yaml)
        d = ConfigDict("cloudmesh.yaml",
                       load_order=[self.tmp_dir],
                       verbose=True)
        d["cloudmesh"]["profile"]["firstname"] = "Gregor"
        d.save()

        d = ConfigDict("cloudmesh.yaml",
                       load_order=[self.tmp_dir],
                       verbose=True)
        assert d["cloudmesh"]["profile"]["firstname"] == "Gregor"


    def test_003_json(self):
        """test if json is produced"""
        HEADING()
        d = ConfigDict("cloudmesh.yaml",
                       verbose=True)

        assert d.json.startswith('{')

        try:
            assert  not isinstance(d.json, str)
            print ("json should be string")
            assert False
        except Exception as e:
            assert isinstance(d.json, str)

    def test_004_yaml(self):
        """test if yaml is produced"""
        HEADING()
        d = ConfigDict("cloudmesh.yaml",
                       verbose=True)
        result = d.yaml

        try:
            assert result.startswith("meta")
        except Exception as e:
            print ("not valid yaml file.")
            assert False




"""	def main():
    d = ConfigDict("cmd3.yaml")
    print (d, end='')
    d.info()

    print (d["meta"])
    print (d["meta.kind"])
    print (d["meta"]["kind"])

    # this does not yet work
    print (d)
    d.save()

    import os
    os.system("cat cmd3.yaml")

    print(d.json)
    print(d.filename)

if __name__ == "__main__":
    main()
"""
