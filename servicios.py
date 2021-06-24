from flask import Flask, jsonify, request
from flask_cors import CORS
from snmpget import *
from snmpset import *
from pysnmp.hlapi import *

AUTH_PROTOCOLS = { 'md5': 'config.usmHMACMD5AuthProtocol', 'sha': 'config.usmHMACSHAAuthProtocol', 'sha128': 'config.usmHMAC128SHA224AuthProtocol',
'sha256' : 'config.usmHMAC192SHA256AuthProtocol', 'sha384' : 'config.usmHMAC256SHA384AuthProtocol', 'sha512' : 'config.usmHMAC384SHA512AuthProtocol'}

PRIV_PROTOCOLS = { 'des': 'config.usmDESPrivProtocol', '3des': 'config.usm3DESEDEPrivProtocol', 'aes128': 'config.usmAesCfb128Protocol',
'aes192' : 'config.usmAesCfb192Protocol', 'aes256' : 'config.usmAesCfb256Protocol', 'aesb192' : 'config.usmAesBlumenthalCfb192Protocol', 'aesb256' : 'config.usmAesBlumenthalCfb256Protocol'}

app = Flask(__name__)
CORS(app, resources=r'/api/*')

@app.route('/api/snmpGET', methods=['POST'])
def get_snmp():
    community = request.json.get('community', "")
    user_name = request.json.get('user_name', "")
    ip_addr = request.json.get('ip_addr', "")
    mib_oid = request.json.get('mib_oid', "")
    version = request.json.get('version', "")
    tipo = request.json.get('type', "")
    authkey = request.json.get('authkey', "")
    auth_prot = request.json.get('auth_prot', "")
    privkey = request.json.get('privkey', "")
    priv_proto = request.json.get('priv_proto', "") 
    errorIndication = ""
    errorStatus = ""
    errorIndex = 0
    varBinds = ""
    
    if version == 1:
        errorIndication, errorStatus, errorIndex, varBinds = snmpget_v1(community, ip_addr, mib_oid)
    elif version == 2:
        errorIndication, errorStatus, errorIndex, varBinds = snmpget_v2(community, ip_addr, mib_oid)
    elif version == 3:
        if tipo == 1:
            errorIndication, errorStatus, errorIndex, varBinds = snmpget_v3_1(user_name, ip_addr, mib_oid)
        elif tipo == 2:
            errorIndication, errorStatus, errorIndex, varBinds = snmpget_v3_2(user_name, authkey, AUTH_PROTOCOLS[auth_prot], ip_addr, mib_oid)
        elif tipo == 3:
            errorIndication, errorStatus, errorIndex, varBinds = snmpget_v3_3(user_name, authkey, privkey, ip_addr, mib_oid, AUTH_PROTOCOLS[auth_prot], PRIV_PROTOCOLS[priv_proto])
    value = response(errorIndication, errorStatus, errorIndex, varBinds)
    #modelRes = {
    #    'message': value
    #}
    #return jsonify(modelRes)
    return jsonify(mensaje=value)

@app.route('/api/snmpGETNext', methods=['POST'])
def get_snmpNext():
    community = request.json.get('community', "")
    user_name = request.json.get('user_name', "")
    ip_addr = request.json.get('ip_addr', "")
    mib_oid = request.json.get('mib_oid', "")
    version = request.json.get('version', "")
    tipo = request.json.get('type', "")
    authkey = request.json.get('authkey', "")
    auth_prot = request.json.get('auth_prot', "")
    privkey = request.json.get('privkey', "")
    priv_proto = request.json.get('priv_proto', "") 
    errorIndication = ""
    errorStatus = ""
    errorIndex = 0
    varBinds = ""
    if version == 1:
        errorIndication, errorStatus, errorIndex, varBinds = snmpgetnext_v1(community, ip_addr, mib_oid)
    elif version == 2:
        errorIndication, errorStatus, errorIndex, varBinds = snmpgetnext_v2(community, ip_addr, mib_oid)
    elif version == 3:
        if tipo == 1:
            errorIndication, errorStatus, errorIndex, varBinds = snmpgetnext_v3_1(user_name, ip_addr, mib_oid)
        elif tipo == 2:
            errorIndication, errorStatus, errorIndex, varBinds = snmpgetnext_v3_2(user_name, authkey, AUTH_PROTOCOLS[auth_prot], ip_addr, mib_oid)
        elif tipo == 3:
            errorIndication, errorStatus, errorIndex, varBinds = snmpgetnext_v3_3(user_name, authkey, privkey, ip_addr, mib_oid, AUTH_PROTOCOLS[auth_prot], PRIV_PROTOCOLS[priv_proto])
    value = response(errorIndication, errorStatus, errorIndex, varBinds)
    return jsonify(mensaje=value)

@app.route('/api/snmpSET', methods=['POST'])
def get_snmpSet():
    community = request.json.get('community', "")
    user_name = request.json.get('user_name', "")
    ip_addr = request.json.get('ip_addr', "")
    mib_oid = request.json.get('mib_oid', "")
    version = request.json.get('version', "")
    tipo = request.json.get('type', "")
    authkey = request.json.get('authkey', "")
    auth_prot = request.json.get('auth_prot', "")
    privkey = request.json.get('privkey', "")
    priv_proto = request.json.get('priv_proto', "")
    new_value = request.json.get('new_value', "") 
    errorIndication = ""
    errorStatus = ""
    errorIndex = 0
    varBinds = ""
    if version == 1:
        errorIndication, errorStatus, errorIndex, varBinds = snmpset_v1(community, ip_addr, mib_oid, new_value)
    elif version == 2:
        errorIndication, errorStatus, errorIndex, varBinds = snmpset_v2(community, ip_addr, mib_oid, new_value)
    elif version == 3:
        if tipo == 1:
            errorIndication, errorStatus, errorIndex, varBinds = snmpset_v3_1(user_name, ip_addr, mib_oid, new_value)
        elif tipo == 2:
            errorIndication, errorStatus, errorIndex, varBinds = snmpset_v3_2(user_name, authkey, AUTH_PROTOCOLS[auth_prot], ip_addr, mib_oid, new_value)
        elif tipo == 3:
            errorIndication, errorStatus, errorIndex, varBinds = snmpset_v3_3(user_name, authkey, privkey, ip_addr, mib_oid, AUTH_PROTOCOLS[auth_prot], PRIV_PROTOCOLS[priv_proto], new_value)
    value = response(errorIndication, errorStatus, errorIndex, varBinds)
    return jsonify(mensaje=value)



if __name__ == '__main__':
    app.run(debug=True)