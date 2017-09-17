import unittest
from mock import patch
from login import login, load_user_from_token, logout
from mock_ldap_backend import check_password

class TestLoginMethods(unittest.TestCase):

    @patch('login.ldap_backend.check_password', side_effect=check_password)
    def test_load_user_from_token(self, login_function):
        message = login('snsakala', 'Luxair123')
        user = load_user_from_token(message['token'])
        self.assertEqual(user.get_id(), 'snsakala')

    @patch('login.ldap_backend.check_password', side_effect=check_password)
    def test_bad_login(self, login_function):
        message = login('snsakala', 'badpass')
        self.assertEqual(message, ({'message': 'access denied'}, 403))
    
    @patch('login.ldap_backend.check_password', side_effect=check_password)
    def test_good_login(self, login_function):
        token = login('snsakala', 'Luxair123')
        self.assertIn('token', token)

    @patch('login.ldap_backend.check_password', side_effect=check_password)
    def test_logout(self, login_function):
        message = login('snsakala', 'Luxair123')
        message = logout(message['token'])
        self.assertEqual(message, {'message': 'logged out successfully'})
        

if __name__ == '__main__':
    unittest.main()
