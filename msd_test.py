__author__ = 'msd'
import config
from THAS_AUTH import thas_auth_context
from user import  user

ldap_uri='ldap://{basedn}:{port}'.format(basedn=config.ldap_server_host,port=config.ldap_server_port)
context = thas_auth_context(ldap_uri,
                            base_dn=config.ldap_base_dn,
                            users_base_dn=config.ldap_base_dn,
                            user_creator_bind_dn='cn=admin,{basedn}'.format(basedn=config.ldap_base_dn),
                            user_creator_password=config.ldap_bind_user_creator_pass,
                            user_editor_bind_dn='cn=admin,{basedn}'.format(basedn=config.ldap_base_dn),
                            user_editor_password=config.ldap_bind_user_creator_pass,
                            user_search_bind_dn='cn=admin,{basedn}'.format(basedn=config.ldap_base_dn),
                            user_search_bind_dn_pass=config.ldap_bind_user_creator_pass)

def test1():
    auth_context = thas_auth_context(ldap_uri,0,config.ldap_base_dn)

def adduser():
    u= user(context)
    u.surname='Mazarei'
    u.common_name='Masoud'
    u.password='1234'
    u.user_id='m.mazarei'
    u.save()

def getuser():
    u=user(context)
    m=u.get_user('m.mazarei')

def edit_user():
    u=user(context)
    m=u.get_user('m.mazarei')
    m.surname='JAFAR GHOLI'
    m.save()


if __name__=='__main__':
    edit_user()
