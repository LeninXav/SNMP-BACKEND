from pysnmp.hlapi import *

# SNMPv1 GETREQUEST
# Parámetros de entrada del tipo string
def snmpget_v1 (community, ip_addr, mib_oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0), 
        UdpTransportTarget((ip_addr, 161)),
        ContextData(), 
        ObjectType(ObjectIdentity(mib_oid))))
    return errorIndication, errorStatus, errorIndex, varBinds


# SNMPv2c GETREQUEST
# Parámetros de entrada del tipo string
def snmpget_v2 (community, ip_addr, mib_oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1), 
        UdpTransportTarget((ip_addr, 161)), ContextData(),
        ObjectType(ObjectIdentity(mib_oid))))
    return errorIndication, errorStatus, errorIndex, varBinds


# SNMPv3 GETREQUEST noAuth noPriv
# # Parámetros de entrada del tipo string 
def snmpget_v3_1 (user_name, ip_addr, mib_oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
        SnmpEngine(),
        UsmUserData(user_name),
        UdpTransportTarget((ip_addr, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(mib_oid))))
    return errorIndication, errorStatus, errorIndex, varBinds


# SNMPv3 GETREQUEST Auth noPriv
# # Parámetros de entrada del tipo string 
def snmpget_v3_2 (user_name, authkey, auth_prot,ip_addr, mib_oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
        SnmpEngine(),
        UsmUserData(user_name, authKey=authkey, authProtocol=auth_prot),
        UdpTransportTarget((ip_addr, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(mib_oid))))
    return errorIndication, errorStatus, errorIndex, varBinds


# SNMPv3 GETREQUEST Auth Priv
# # Parámetros de entrada del tipo string 
def snmpget_v3_3 (user_name, authkey, privkey, ip_addr, mib_oid, auth_prot, priv_proto):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
        SnmpEngine(),
        UsmUserData(user_name, privKey=privkey, privProtocol=priv_proto, authKey=authkey, authProtocol=auth_prot),
        UdpTransportTarget((ip_addr, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(mib_oid))))
    return errorIndication, errorStatus, errorIndex, varBinds


# Imprime los posibles errores generados en los mensajes SNMP
def print_response (errorIndication, errorStatus, errorIndex, varBinds):
    if errorIndication:
            print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


def response (errorIndication, errorStatus, errorIndex, varBinds):
    if errorIndication:
            return errorIndication
    elif errorStatus:
        return str(errorStatus.prettyPrint()) + " at " + str(errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
    else:
        var = ''
        for varBind in varBinds:
            var = var + ' = '.join([x.prettyPrint() for x in varBind]) + "\n"
        return var


