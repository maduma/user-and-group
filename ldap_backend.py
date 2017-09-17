import ldap


LDAP_URL = 'ldap://ldapp.svr.luxair:389/'
BASE_DN = 'o=test'
GROUP_DN = 'ou=group,ou=example,o=test'

def check_password(username, password):
    conn = ldap.initialize(LDAP_URL)
    # find the user dn
    filter = '(uid=' + username + ')'
    results = conn.search_s(BASE_DN, ldap.SCOPE_SUBTREE, filter)
    if len(results) == 1:
        dn = results[0][0]
        # Try a bind
        try:
            results = conn.simple_bind_s(dn, password)
            return True
        except ldap.INVALID_CREDENTIALS:
            return False
    return False

def get_groups():
    conn = ldap.initialize(LDAP_URL)
    results = conn.search_s(GROUP_DN, ldap.SCOPE_ONELEVEL, '(cn=*)')
    return [x[1]['cn'][0] for x in results]
    

def get_group(group_id):
    conn = ldap.initialize(LDAP_URL)
    filter = '(cn=' + group_id + ')'
    results = conn.search_s(GROUP_DN, ldap.SCOPE_ONELEVEL, filter)
    if len(results) == 1:
        attrs = results[0][1]
        member = [x.split(',')[0].split('=')[1] for x in attrs['uniqueMember']]
        return {attrs['cn'][0]: member}
    return {'message': 'cannot find group ' + group_id}, 404


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
