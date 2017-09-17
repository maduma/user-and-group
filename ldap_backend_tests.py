import unittest
import ldap
import ldap_backend

from mockldap import MockLdap


class LdapBackendTest(unittest.TestCase):
    top = ('o=test', {'o': ['test']})
    example = ('ou=example,o=test', {'ou': ['example']})
    people = ('ou=people,ou=example,o=test', {'ou': ['other']})
    group = ('ou=group,ou=example,o=test', {'ou': ['other']})
    admin = ('cn=admin,ou=group,ou=example,o=test', {'cn': ['admin'], 'uniqueMember': [
        'uid=alice,ou=people,ou=example,o=test',
        'uid=bob,ou=people,ou=example,o=test',
        ]})
    paylink = ('cn=paylink,ou=group,ou=example,o=test', {'cn': ['paylink']})
    manager = ('cn=manager,ou=example,o=test', {'cn': ['manager'], 'userPassword': ['ldaptest']})
    alice = ('uid=alice,ou=people,ou=example,o=test', {'uid': ['alice'], 'userPassword': ['alicepw']})
    bob = ('uid=bob,ou=people,ou=example,o=test', {'uid': ['bob'], 'userPassword': ['bobpw']})

    directory = dict([top, example, people, group, admin, paylink, manager, alice, bob])

    @classmethod
    def setUpClass(cls):
        cls.mockldap = MockLdap(cls.directory)

    @classmethod
    def tearDownClass(cls):
        del cls.mockldap

    def setUp(self):
        self.mockldap.start()
        self.ldapobj = self.mockldap['ldap://localhost/']

    def tearDown(self):
        self.mockldap.stop()
        del self.ldapobj

    def test_sucessfull_search_and_bind(self):
        results = ldap_backend.check_password('alice', 'alicepw')
        self.assertEquals(results, True)
        
    def test_cannot_find_user(self):
        results = ldap_backend.check_password('noone', 'alicepw')
        self.assertEquals(results, False)
        
    def test_bad_password(self):
        results = ldap_backend.check_password('alice', 'badpassword')
        self.assertEquals(results, False)
        
    def test_get_groups(self):
        results = ldap_backend.get_groups()
        self.assertEquals(sorted(results), ['admin', 'paylink'])
        
    def test_get_group(self):
        results = ldap_backend.get_group('admin')
        self.assertEquals(results, {'admin': ['alice', 'bob']})
        
    def test_get_group_not_found(self):
        results = ldap_backend.get_group('nogroup')
        self.assertEquals(results, ({'message': 'cannot find group nogroup'}, 404))

if __name__ == '__main__':
    unittest.main()