__author__ = 'msd'
import ldap.modlist as modlist
from THAS_AUTH import thas_auth_context #no real usage only in asserts

class user(object):
    ldap_mapping = {
        'user_id': 'uid',
        'password': 'userPassword',
        'common_name': 'cn',
        'surname': 'sn'
    }

    ldap_object_classes = ['top', 'inetOrgPerson']
    ldap_rdn_property='user_id'

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
        self._ldap_rdn = ldap_rdn_property or user.ldap_rdn_property
        self._ldap_context = ldap_context
        self._ldap_mapping = ldap_mapping or user.ldap_mapping
        self._ldap_object_classes = ldap_object_classes or user.ldap_object_classes
        self._properties_changed = []
        self._old_properties_values = []
        self._state = 'NEW'
        self._user_id=None
        self._surname=None
        self._common_name=None
        self._password=None


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
        return None

    @classmethod
    def from_ldif(self,ldif):
        pass

    def get_user_by_user_id(self,user_id):
        k=self.ldap_context.get_user_by_user_id(self.ldap_mapping[self.rdn_property],user_id)
        print k
        return  k




    def save(self):
        if self.ldap_context is None:
            raise Exception('No ldap context exists')

        if self.state=='NEW':
            self.ldap_context.add_user(self.ldap_mapping[self.rdn_property], getattr(self,self.rdn_property),
                                       self.to_ldif())
        elif self.state=='EDIT':
            pass





    @property
    def ldap_context(self):
        return self._ldap_context

    @property
    def state(self):
        return self._state

    def pc(self, name, value):
        '''
        pc is 'property change' abstract

        :param name: property name which its value is changed
        :param value: old property value
        :return: nothing
        '''

        self._properties_changed.append(name)
        self._old_properties_values.append(value)


    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        print 'user id setted to ',value
        self.pc('user_id', self._user_id)
        self._user_id = value


    @property
    def common_name(self):
        return self._common_name

    @common_name.setter
    def common_name(self, value):
        self.pc('common_name', self._common_name)
        self._common_name = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self.pc('surname', self._surname)
        self._surname = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self.pc('password', self._password)
        self._password = value
