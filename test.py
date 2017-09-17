import unittest
from login_tests import TestLoginMethods
from ldap_backend_tests import LdapBackendTest


tests = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestLoginMethods),
    unittest.TestLoader().loadTestsFromTestCase(LdapBackendTest),
])

unittest.TextTestRunner(verbosity=2).run(tests)
