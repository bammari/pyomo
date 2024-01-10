#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2022
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import pyomo.common.unittest as unittest
import glob
import os
from pyomo.common.dependencies import attempt_import
from pyomo.common.fileutils import this_file_dir
import pyomo.environ as pyo


parameterized, param_available = attempt_import('parameterized')
if not param_available:
    raise unittest.SkipTest('Parameterized is not available.')

# Needed for testing (switches the matplotlib backend):
from pyomo.common.dependencies import matplotlib_available

bool(matplotlib_available)

currdir = this_file_dir()


class TestOnlineDocExamples(unittest.BaseLineTestDriver, unittest.TestCase):
    # Only test files in directories ending in -ch. These directories
    # contain the updated python and scripting files corresponding to
    # each chapter in the book.
    py_tests, sh_tests = unittest.BaseLineTestDriver.gather_tests(
        list(filter(os.path.isdir, glob.glob(os.path.join(currdir, '*'))))
    )

    solver_dependencies = {}
    package_dependencies = {
        # data
        'test_data_ABCD9': ['pyodbc'],
        'test_data_ABCD8': ['pyodbc'],
        'test_data_ABCD7': ['win32com', 'pyutilib.excel.spreadsheet'],
        # dataportal
        'test_dataportal_dataportal_tab': ['xlrd', 'pyutilib.excel.spreadsheet'],
        'test_dataportal_set_initialization': ['numpy'],
        'test_dataportal_param_initialization': ['numpy'],
        # kernel
        'test_kernel_examples': ['pympler'],
    }

    @parameterized.parameterized.expand(
        sh_tests, name_func=unittest.BaseLineTestDriver.custom_name_func
    )
    def test_sh(self, tname, test_file, base_file):
        self.shell_test_driver(tname, test_file, base_file)

    @parameterized.parameterized.expand(
        py_tests, name_func=unittest.BaseLineTestDriver.custom_name_func
    )
    def test_py(self, tname, test_file, base_file):
        self.python_test_driver(tname, test_file, base_file)


# Execute the tests
if __name__ == '__main__':
    unittest.main()
