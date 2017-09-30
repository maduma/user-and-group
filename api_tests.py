import unittest
import json
import api
from mock import patch
from mock_ldap_backend import get_groups, get_group, get_group_users
from mock_ldap_backend import get_users, get_user, get_user_groups

class TestApiNoLogin(unittest.TestCase):

    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()


    def test_root(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 404)
    
    @patch('api.ldap_backend.get_groups', side_effect=get_groups)
    def test_groups(self, mock_function):
        resp = self.app.get('/groups')
        data = json.loads(resp.data)
        self.assertEqual(sorted(data), ['admin', 'dxretail'])
        
    @patch('api.ldap_backend.get_group', side_effect=get_group)
    def test_group(self, mock_function):
        resp = self.app.get('/groups/admin')
        data = json.loads(resp.data)
        self.assertEqual(sorted(data), ['admin'])
    
    @patch('ldap_backend.get_group_users', side_effect=get_group_users)
    def test_get_user_group(self, mock_function):
        resp = self.app.get('/groups/admin/users')
        data = json.loads(resp.data)
        self.assertEqual(sorted(data), ['ckoenig', 'snsakala'])
    
    def test_create_group(self):
        resp = self.app.put('/groups/newgroup')
        self.assertEqual(resp.status_code, 401)
    
    
    def test_delete_group(self):
        resp = self.app.delete('/groups/admin')
        self.assertEqual(resp.status_code, 401)
        
    def test_add_user_to_group(self):
        resp = self.app.put('/groups/admin/users/newuser')
        self.assertEqual(resp.status_code, 401)
        
    def test_delete_user_from_group(self):
        resp = self.app.delete('/groups/admin/users/snsakala')
        self.assertEqual(resp.status_code, 401)
        
    @patch('ldap_backend.get_users', side_effect=get_users)
    def test_get_all_users(self, mock_function):
        resp = self.app.get('/users')
        data = json.loads(resp.data)
        self.assertEqual(sorted(data), ['ckoenig', 'mgrof', 'snsakala'])
        
    
    @patch('ldap_backend.get_user', side_effect=get_user)
    def test_get_all_users(self, mock_function):
        resp = self.app.get('/users/snsakala')
        data = json.loads(resp.data)
        self.assertEqual(data, 'snsakala')
        
    @patch('ldap_backend.get_user_groups', side_effect=get_user_groups)
    def test_group_users(self, mock_function):
        resp = self.app.get('/users/ckoenig/groups')
        data = json.loads(resp.data)
        self.assertEqual(sorted(data), ['admin', 'dxretail'])

        


if __name__ == '__main__':
    unittest.main()