import ldap


LDAP_URL = 'ldap://localhost:389'


def check_password(username, password):
    ldap_conn = ldap.initialize(LDAP_URL)
    # find the user dn
    dn = ''
    # try to bind
    ldap_conn.simple_bind(dn, password)


def get_groups():
    pass


def get_group(group_id):
    pass


def create_group(group_id):
    pass


def delete_group(group_id):
    pass


def get_group_users(group_id):
    pass


def add_user_in_group(user_id, group_id):
    pass


def delete_user_from_group(user_id, group_id):
    pass


def find_ldap_users(filter):
    pass


def get_users():
    pass


def get_user(user_id):
    pass


def get_user_groups(user_id):
    pass
