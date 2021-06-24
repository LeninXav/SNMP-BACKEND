from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import socketio

sio = socketio.Client()

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

@sio.event
def connect():
    print('connection established')



@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:1000')
# Transport setup

# UDP over IPv4, first listening interface/port
config.addTransport(
    snmpEngine,
    udp.domainName + (1,),
    udp.UdpTransport().openServerMode(('127.0.0.1', 162))
)

# UDP over IPv4, second listening interface/port
config.addTransport(
    snmpEngine,
    udp.domainName + (2,),
    udp.UdpTransport().openServerMode(('127.0.0.1', 2162))
)

# SNMPv1/2c setup

# SecurityName <-> CommunityName mapping
# Se setea el nombre de comunidad a donde llegarán las traps
# como se muestra a continuación
config.addV1System(snmpEngine, 'private', 'private')

# Callback function for receiving notifications
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    archivo = open('trap','a+')
    archivo.write("Notification from ContextEngineId " + contextEngineId.prettyPrint() + ", ContextName " + contextName.prettyPrint()+"\n")
    #sio.emit('trap', 'Trap Versión 1,2')
    #sio.emit('trap', "Notification from ContextEngineId " + contextEngineId.prettyPrint() + ", ContextName " + contextName.prettyPrint())
    print('Notification from ContextEngineId "%s", ContextName "%s"' % (contextEngineId.prettyPrint(),
                                                                        contextName.prettyPrint()))
    lista = []
    for name, val in varBinds:
        archivo.write(name.prettyPrint()+" = "+val.prettyPrint()+"\n")
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        #sio.emit('trap', name.prettyPrint()+" = "+val.prettyPrint())
        lista.append(name.prettyPrint()+" = "+val.prettyPrint())
    sio.emit('trap', {'cabecera':'Trap Versión 1-2', 'notificacion': "Notification from ContextEngineId " + contextEngineId.prettyPrint() + ", ContextName " + contextName.prettyPrint(), 'datos': lista})
    archivo.close()


# Register SNMP Application at the SNMP engine
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    sio.disconnect()
    raise