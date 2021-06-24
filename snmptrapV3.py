from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')



@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:1000')
# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('127.0.0.1', 162))
)

# SNMPv3/USM setup

# user: marioPriv, auth: MD5, priv DES
config.addV3User(
    snmpEngine,
    userName='marioPriv',
    authProtocol=config.usmHMACMD5AuthProtocol,
    authKey='0123456789',
    privProtocol=config.usmDESPrivProtocol,
    privKey='0123456789'
)

# user: user: marioPriv, auth: MD5, priv DES, securityEngineId: 8000000001020304
# this USM entry is used for TRAP receiving purposes
#config.addV3User(
#    snmpEngine, 
#    userName='marioPriv',
#    config.usmHMACMD5AuthProtocol, '0123456789',
#    config.usmDESPrivProtocol, '0123456789',
#    securityEngineId=v2c.OctetString(hexValue='8000000001020304')
#)

# user: marioAuth, auth: MD5, priv NONE
config.addV3User(
    snmpEngine, 
    userName='marioAuth',
    authProtocol=config.usmHMACMD5AuthProtocol,
    authKey='0123456789'
)

# user: marioAuth, auth: MD5, priv NONE, securityEngineId: 8000000001020304
# this USM entry is used for TRAP receiving purposes
#config.addV3User(
#    snmpEngine, 
#    userName='marioAuth',
#    config.usmHMACMD5AuthProtocol, '0123456789',
#    securityEngineId=v2c.OctetString(hexValue='8000000001020304')
#)

# user: marioNoAuth
config.addV3User(
    snmpEngine,
    userName='marioNoAuth'
)

# user: usr-sha-aes128, auth: SHA, priv AES
#config.addV3User(
#    snmpEngine, 'usr-sha-aes128',
#    config.usmHMACSHAAuthProtocol, 'authkey1',
#    config.usmAesCfb128Protocol, 'privkey1'
#)
# user: usr-sha-aes128, auth: SHA, priv AES, securityEngineId: 8000000001020304
# this USM entry is used for TRAP receiving purposes
#config.addV3User(
#    snmpEngine, 'usr-sha-aes128',
#    config.usmHMACSHAAuthProtocol, 'authkey1',
#    config.usmAesCfb128Protocol, 'privkey1',
#    securityEngineId=v2c.OctetString(hexValue='8000000001020304')
#)   

# Callback function for receiving notifications
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
    archivo = open('trap3','a+')
    archivo.write("Notification from ContextEngineId " + contextEngineId.prettyPrint() + ", ContextName " + contextName.prettyPrint()+"\n")
    print('Notification from ContextEngineId "%s", ContextName "%s"' % (contextEngineId.prettyPrint(),
                                                                        contextName.prettyPrint()))
    lista = []
    for name, val in varBinds:
        archivo.write(name.prettyPrint()+" = "+val.prettyPrint()+"\n")
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
    sio.emit('trap3', {'cabecera':'Trap Versión 3', 'notificacion': "Notification from ContextEngineId " + contextEngineId.prettyPrint() + ", ContextName " + contextName.prettyPrint(), 'datos': lista})
    archivo.close()


# Register SNMP Application at the SNMP engine
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
