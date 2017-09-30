import unittest
from login_tests import TestLoginMethods
from ldap_backend_tests import LdapBackendTest
from api_tests import TestApiNoLogin
import sys


tests = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestLoginMethods),
    unittest.TestLoader().loadTestsFromTestCase(LdapBackendTest),
    unittest.TestLoader().loadTestsFromTestCase(TestApiNoLogin),
])

result = unittest.TextTestRunner(verbosity=2).run(tests)
if len(result.failures) != 0:
    sys.exit(1)
