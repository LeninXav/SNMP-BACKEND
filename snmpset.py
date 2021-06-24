from pysnmp.hlapi import *

# SNMPv1 SET-REQUEST
# Parámetros de entrada del tipo string
def snmpset_v1 (community, ip_addr, mib_oid, new_value):
    errorIndication, errorStatus, errorIndex, varBinds = next(setCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0), 
        UdpTransportTarget((ip_addr, 161)),
        ContextData(), 
        ObjectType(ObjectIdentity(mib_oid), new_value)))
    return errorIndication, errorStatus, errorIndex, varBinds

# SNMPv2c SET-REQUEST
# Parámetros de entrada del tipo string
def snmpset_v2 (community, ip_addr, mib_oid, new_value):
    errorIndication, errorStatus, errorIndex, varBinds = next(setCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1),
        UdpTransportTarget((ip_addr, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(mib_oid), new_value)))
    return errorIndication, errorStatus, errorIndex, varBinds

# SNMPv3 SET-REQUEST noAuth noPriv
# # Parámetros de entrada del tipo string 
def snmpset_v3_1 (user_name, ip_addr, mib_oid, new_value):
    errorIndication, errorStatus, errorIndex, varBinds = next(setCmd(
        SnmpEngine(),
        UsmUserData(user_name),
        UdpTransportTarget((ip_addr, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(mib_oid), new_value)))
    return errorIndication, errorStatus, errorIndex, varBinds


# SNMPv3 SET-REQUEST Auth noPriv
# # Parámetros de entrada del tipo string 
def snmpset_v3_2 (user_name, authkey, auth_prot,ip_addr, mib_oid, new_value):
    errorIndication, errorStatus, errorIndex, varBinds = next(setCmd(
        SnmpEngine(),
        UsmUserData(user_name, authKey=authkey, authProtocol=auth_prot),
        UdpTransportTarget((ip_addr, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(mib_oid), new_value)))
    return errorIndication, errorStatus, errorIndex, varBinds


# SNMPv3 SET-REQUEST Auth Priv
# # Parámetros de entrada del tipo string 
def snmpset_v3_3 (user_name, authkey, privkey, ip_addr, mib_oid, auth_prot, priv_proto, new_value):
    errorIndication, errorStatus, errorIndex, varBinds = next(setCmd(
        SnmpEngine(),
        UsmUserData(user_name, privKey=privkey, privProtocol=priv_proto, authKey=authkey, authProtocol=auth_prot),
        UdpTransportTarget((ip_addr, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(mib_oid), new_value)))
    return errorIndication, errorStatus, errorIndex, varBinds



