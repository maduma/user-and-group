import unittest
import ldap
import ldap_backend

from mockldap import MockLdap


class LdapBackendTest(unittest.TestCase):
    top = ('o=test', {'o': ['test']})
    example = ('ou=example,o=test', {'ou': ['example']})
    people = ('ou=people,ou=example,o=test', {'ou': ['people']})
    group = ('ou=group,ou=example,o=test', {'ou': ['group']})
    admin = ('cn=admin,ou=group,ou=example,o=test', {'cn': ['admin'], 'uniqueMember': [
        'uid=alice,ou=people,ou=example,o=test',
        'uid=bob,ou=people,ou=example,o=test',
        ]})
    paylink = ('cn=paylink,ou=group,ou=example,o=test', {'cn': ['paylink'], 'uniqueMember': [
        'uid=bob,ou=people,ou=example,o=test',
        'uid=jeff,ou=people,ou=example,o=test',
        ]})
    dev = ('cn=dev,ou=group,ou=example,o=test', {'cn': ['dev']})
    manager = ('cn=manager,ou=example,o=test', {'cn': ['manager'], 'userPassword': ['ldaptest']})
    alice = ('uid=alice,ou=people,ou=example,o=test', {'uid': ['alice'], 'userPassword': ['alicepw']})
    bob = ('uid=bob,ou=people,ou=example,o=test', {'uid': ['bob'], 'userPassword': ['bobpw']})
    jeff = ('uid=jeff,ou=people,ou=example,o=test', {'uid': ['jeff'], 'userPassword': ['jeffpw']})

    directory = dict([top, example, people, group, admin, paylink, dev, manager, alice, bob, jeff])

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
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s', 'simple_bind_s'])
        
    def test_cannot_find_user(self):
        results = ldap_backend.check_password('noone', 'alicepw')
        self.assertEquals(results, False)
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
        
    def test_bad_password(self):
        results = ldap_backend.check_password('alice', 'badpassword')
        self.assertEquals(results, False)
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s', 'simple_bind_s'])
        
    def test_get_groups(self):
        results = ldap_backend.get_groups()
        self.assertEquals(sorted(results), ['admin', 'dev', 'paylink'])
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
        
    def test_get_group(self):
        results = ldap_backend.get_group('admin')
        self.assertEquals(results, {'admin': ['alice', 'bob']})
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
        
    def test_get_group_not_found(self):
        results = ldap_backend.get_group('nogroup')
        self.assertEquals(results, ({'message': 'cannot find group nogroup'}, 404))
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
    
    def test_create_group_already_exists(self):
        results = ldap_backend.create_group('admin')
        self.assertEquals(results, ({'message': 'group admin already exists'}, 403))
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
        
    def test_create_group(self):
        results = ldap_backend.create_group('newgroup')
        self.assertEquals(results, {'message': 'group newgroup created'})
        self.assertEquals(self.ldapobj.bound_as, 'cn=manager,ou=example,o=test')
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s', 'simple_bind_s', 'add_s'])
        self.assertIn('cn=newgroup,ou=group,ou=example,o=test', self.ldapobj.directory)
    
    def test_delete_group_not_exists(self):
        results = ldap_backend.delete_group('nogroup')
        self.assertEquals(results, ({'message': 'cannot find group nogroup'}, 403))
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
    
    def test_delete_group_not_empty(self):
        results = ldap_backend.delete_group('admin')
        self.assertEquals(results, ({'message': 'group admin not empty'}, 403))
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
        
    def test_delete_group(self):
        results = ldap_backend.delete_group('dev')
        self.assertEquals(results, {'message': 'group dev deleted'})
        self.assertEquals(self.ldapobj.bound_as, 'cn=manager,ou=example,o=test')
        self.assertEquals(self.ldapobj.methods_called(), [
            'initialize', 'search_s', 'simple_bind_s', 'delete_s'])
        self.assertNotIn('cn=dev,ou=group,ou=example,o=test', self.ldapobj.directory)

    def test_get_group_users_group_not_found(self):
        results = ldap_backend.get_group_users('notthere')
        self.assertEquals(results, ({'message': 'cannot find group notthere'}, 403))
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
        
    def test_get_group_users_group_empty(self):
        results = ldap_backend.get_group_users('dev')
        self.assertEquals(results, [])
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])

    def test_get_group_users(self):
        results = ldap_backend.get_group_users('paylink')
        self.assertEquals(sorted(results), ['bob', 'jeff'])
        self.assertEquals(self.ldapobj.methods_called(), ['initialize', 'search_s'])
        
    def test_add_user_in_group(self):
        results = ldap_backend.add_user_in_group('alice', 'paylink')
        
if __name__ == '__main__':
    unittest.main()