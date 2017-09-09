Group
- create : POST /groups
- delete (must be empty) : DELETE /groups/<groupdId>
- list groups : GET /groups
- group info : GET /groups/<groupId>
- add user to a group : POST /groups/<groupId>/users/<userId>
- remove user from a group : DELETE /groups/<groupId>/users/<userId>
- list user from a group : GET /groups/<groupId>/users


User
- search all users (ldap filter): Get /users?filter=(uid=snsak*)
- get all users that belong to a least one group: GET /users
- get user information (key: uid) : GET /users/<userId>
- list group that the user belong to : GET /users/<userId>/groups


Auth:
- /login (return a session token)
- /logout
