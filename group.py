__author__ = 'msd'
import ldap.modlist as modlist


class group(object):

    ldap_mapping = {
        'group_name': 'cn',
        'members': 'member',
    }

    ldap_object_classes = ['top', 'groupOfNames']
    ldap_rdn_property = 'group_name'

    def __init__(self,
                 ldap_context=None,
                 ldap_mapping=None,
                 ldap_object_classes=None,
                 ldap_rdn_property=None,

    ):
        '''

        :param ldap_context: is an instance of thas_auth_contenxt
        :param ldap_mapping: is dictionary which maps this object properties to ldap one
        :param ldap_object_classes: is array of strings which define object class of this entry in ldap
        :param ldap_rdn_property: specifies which property of this object should use in ldap dn
        :return:
        '''
        self._ldap_rdn = ldap_rdn_property or group.ldap_rdn_property
        self._ldap_context = ldap_context
        self._ldap_mapping = ldap_mapping or group.ldap_mapping
        self._ldap_object_classes = ldap_object_classes or group.ldap_object_classes
        self._properties_changed = []
        self._old_properties_values = []
        self._state = 'NEW'
        self._group_name = None
        self._members= []


    def _clear_changes(self):
        self._old_properties_values =[]
        self._properties_changed=[]

    @property
    def rdn_property(self):
        return self._ldap_rdn

    def to_ldif(self):
        if self.state == 'NEW':
            attrs = dict()
            for i in self._properties_changed:
                attrs[self.ldap_mapping[i]] = getattr(self, i)
                attrs['objectclass'] = self._ldap_object_classes
            return modlist.addModlist(attrs)
        elif self.state=='EDIT':
            old_attrs=dict()
            attrs = dict()
            for i in range(len(self._properties_changed)):
                prop_name = self._properties_changed[i]
                ldap_name = self.ldap_mapping[prop_name]
                old_value = self._old_properties_values[i]
                new_value = getattr(self,prop_name)
                old_attrs[ldap_name]=old_value
                attrs[ldap_name]=new_value
            return modlist.modifyModlist(old_attrs,attrs)

        return None

    def from_ldif(self, ldif):
        user_dict = ldif
        inv_ldap_mapping = {v: k for k, v in self._ldap_mapping.items()}
        for i in user_dict:
            if i in inv_ldap_mapping:
                setattr(self, inv_ldap_mapping[i], user_dict[i][0])
        self._clear_changes()
        self._state = 'EDIT'
        return self

    @property
    def ldap_context(self):
        return self._ldap_context

    @property
    def state(self):
        return self._state

    def pc(self, name, value):
        '''
        pc is 'property change' abstract, wv

        :param name: property name which its value is changed
        :param value: old property value
        :return: nothing
        '''

        self._properties_changed.append(name)
        self._old_properties_values.append(value)


    def save(self):
        if self.ldap_context is None:
            raise Exception('No ldap context exists')

        if self.state == 'NEW':
            if len(self._properties_changed) == 0:
                return
            self.ldap_context.add_group(self.ldap_mapping[self.rdn_property], getattr(self, self.rdn_property),
                                       self.to_ldif())
        elif self.state == 'EDIT':
            if len(self._properties_changed) == 0:
                return
            self.ldap_context.edit_user(self.ldap_mapping[self.rdn_property], getattr(self, self.rdn_property),
                                       self.to_ldif())


    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        self.pc('group_name', self._group_name)
        self._group_name= value


    @property
    def members(self):
        return self._members or []

    @members.setter
    def members(self, value):
        self.pc('members', self._members)
        self._members= value
