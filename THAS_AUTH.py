__author__ = 'msd'
import ldap


class thas_auth_context:
    @property
    def ldap_object(self):
        return self._ldapobj

    def __init__(self,
                 ldap_uri='ldap://localhost:389',
                 trace_level=0, base_dn='cn=admin,dc=example,dc=com',
                 user_creator_bind_dn='cn=admin,dc=example,dc=com',
                 user_creator_password=None,
                 user_editor_bind_dn = 'cn=admin,dc=example,dc=com',
                 user_editor_password=None,
                 users_base_dn='ou=people,dc=example,dc=com',
                 user_search_bind_dn='cn=admin,dc=example,dc=com',
                 user_search_bind_dn_pass=None,

                 group_creator_bind_dn='cn=admin,dc=example,dc=com',
                 group_creator_password=None,
                 group_editor_bind_dn = 'cn=admin,dc=example,dc=com',
                 group_editor_password=None,
                 groups_base_dn='ou=people,dc=example,dc=com',
                 group_search_bind_dn='cn=admin,dc=example,dc=com',
                 group_search_bind_dn_pass=None,


    ):
        # initialize ldap object
        self._ldapobj = ldap.initialize(ldap_uri, trace_level)
        self._usercreator = user_creator_bind_dn
        self._usercreator_pass = user_creator_password
        self._usereditor = user_editor_bind_dn
        self._usereditor_pass = user_editor_password
        self._users_base_dn = users_base_dn
        self._user_search_bind_dn=user_search_bind_dn
        self._user_search_bind_dn_pass=user_search_bind_dn_pass


        self._groupcreator = group_creator_bind_dn
        self._groupcreator_pass = group_creator_password
        self._groupeditor = group_editor_bind_dn
        self._groupeditor_pass = group_editor_password
        self._groups_base_dn = groups_base_dn
        self._group_search_bind_dn=group_search_bind_dn
        self._group_search_bind_dn_pass=group_search_bind_dn_pass





    ########################
    ######Group Property
    ########################

    @property
    def group_editor_bind_property(self):
        return self._group_search_bind_dn,self._groupeditor_pass

    @property
    def group_search(self):
        return self._group_search_bind_dn,self._group_search_bind_dn_pass

    @property
    def groups_base_dn(self):
        return self._groups_base_dn

    @property
    def ldap_group_creator_bind_property(self):
        return self._groupcreator, self._groupcreator_pass


    ########################
    ######User Property
    ############



    @property
    def user_editor_bind_property(self):
        return self._user_search_bind_dn,self._usereditor_pass

    @property
    def user_search(self):
        return self._user_search_bind_dn,self._user_search_bind_dn_pass

    @property
    def users_base_dn(self):
        return self._users_base_dn

    @property
    def ldap_object(self):
        return self._ldapobj

    @property
    def ldap_user_creator_bind_property(self):
        return self._usercreator, self._usercreator_pass

    def group_bind_to_search(self):
        user,passw = self.group_search
        self.ldap_object.bind_s(user,passw)

    def _bind_to_search(self):
        user,passw =self.user_search
        self.ldap_object.bind_s(user,passw)

    def _bind_to_edit_group(self):
        user, passw = self.group_editor_bind_property
        self.ldap_object.bind_s(user,passw)

    def _bind_to_edit_user(self):
        user, passw = self.user_editor_bind_property
        self.ldap_object.bind_s(user, passw)

    def _bind_to_add_group(self):
        user,passw = self.ldap_group_creator_bind_property
        self.ldap_object.bind_s(user,passw)

    def _bind_to_add_user(self):
        user, passw = self.ldap_user_creator_bind_property
        self.ldap_object.bind_s(user, passw)

    def add_user(self, dn_prop_name, dn_prop_value, ldif):
        self._bind_to_add_user()
        dn = '{prop}={value},{basedn}'.format(prop=dn_prop_name, value=dn_prop_value, basedn=self.users_base_dn)
        rtn = self.ldap_object.add_s(dn, ldif)
        self.ldap_object.unbind_s()

    def edit_user(self,dn_prop_name,dn_prop_value,ldif):
        self._bind_to_edit_user()
        dn = '{prop}={value},{basedn}'.format(prop=dn_prop_name, value=dn_prop_value, basedn=self.users_base_dn)
        rtn = self.ldap_object.modify_s(dn, ldif)
        self.ldap_object.unbind_s()

    def add_group(self, dn_prop_name, dn_prop_value, ldif, parent_group_dn=None):
        self._bind_to_add_group()
        dn = '{prop}={value},{basedn}'.format(prop=dn_prop_name, value=dn_prop_value, basedn=parent_group_dn or self.groups_base_dn)
        rtn = self.ldap_object.add_s(dn, ldif)
        self.ldap_object.unbind_s()




    def get_user_by_user_id(self,dn_prop_name,user_id):
        self._bind_to_search()
        dn = '{prop}={value},{basedn}'.format(prop=dn_prop_name, value=user_id, basedn=self.users_base_dn)
        return self.ldap_object.search_s(dn,ldap.SCOPE_BASE)

    def get_group_by_group_id(self,dn_prop_name,group_name):
        pass










