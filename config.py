__author__ = 'msd'
#######################
##### LDAP CONFIGs ####
#######################
ldap_server_host='ldap.lxc.msd.local'
ldap_server_port=389
ldap_base_dn='dc=ldap,dc=lxc,dc=msd,dc=local'
ldap_bind_user_creator='cn=admin,{basedn}'.format(basedn=ldap_base_dn)
ldap_bind_user_creator_pass='123456'
ldap_trace_level=0 #out put ldap commands
########################
### LOGGING SECTION  ###
########################
