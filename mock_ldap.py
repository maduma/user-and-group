passwords = {'snsakala': 'Luxair123', 'ckoenig': 'Luxair2987'}
groups = {'admin': ['snsakala', 'ckoenig'], 'dxretail': ['ckoenig']}

def check_password(username, password):
    return passwords[username] == password

def get_groups():
    return list(groups.keys())


def get_group(group_id):
    if group_id in groups:
        return {group_id: groups[group_id]}
    return {'message': 'cannot find group ' + group_id}, 404


def create_group(group_id):
    if group_id in groups:
        return {'message': group_id + ' already exists'}, 500
    groups[group_id] = []
    return {'message': group_id + ' created'}


def delete_group(group_id):
    if group_id in groups:
        if len(groups[group_id]) == 0:
            groups.pop(group_id)
            return {'message': 'group deleted'}
        return {'message': 'group not empty'}, 403
    return {'message': 'group not existing'}, 404


def get_group_users(group_id):
    if group_id in groups:
        return groups[group_id]
    return {'message': 'cannot find group ' + group_id}, 404


def add_user_in_group(user_id, group_id):
    if group_id in groups:
        if user_id not in groups[group_id]:
            groups[group_id].append(user_id)
            return groups[group_id]
        return {'message': 'user already in group'}, 403
    return {'message': 'cannot find group ' + group_id}, 404


def delete_user_from_group(user_id, group_id):
    if group_id in groups:
        if user_id in groups[group_id]:
            groups[group_id].remove(user_id)
            return {'message': 'user removed from group'}
        return {'message': 'cannot find user' + user_id}, 404
    return {'message': 'cannot find group' + group_id}, 404


def find_ldap_users(filter):
    pass


def get_users():
    users = []
    for group_id in groups:
        for user_id in groups[group_id]:
            if user_id not in users:
                users.append(user_id)
    return users


def get_user(user_id):
    users = []
    for group_id in groups:
        for user in groups[group_id]:
            if user not in users:
                users.append(user)
    if user_id in users:
        return user_id
    return {'message': 'cannot find user'}, 404


def get_user_groups(user_id):
    user_groups = []
    for group_id in groups:
        if user_id in groups[group_id]:
            user_groups.append(group_id)
    return user_groups
