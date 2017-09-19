import unittest
from login_tests import TestLoginMethods
from ldap_backend_tests import LdapBackendTest
import sys


tests = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestLoginMethods),
    unittest.TestLoader().loadTestsFromTestCase(LdapBackendTest),
])

result = unittest.TextTestRunner(verbosity=2).run(tests)
if len(result.failures) != 0:
    sys.exit(1)
