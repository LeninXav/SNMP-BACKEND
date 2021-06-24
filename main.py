from snmpget import *
from snmpset import *
from snmptrapV3 import *

print ("\nMensaje get-request v2:")
errorIndication, errorStatus, errorIndex, varBinds = snmpget_v1 ('public', '127.0.0.1', '.1.3.6.1.2.1.1.5.0')
print_response (errorIndication, errorStatus, errorIndex, varBinds)
print ()

print ("\nMensaje set-request v2:")
errorIndication, errorStatus, errorIndex, varBinds = snmpset_v2 ('private', '127.0.0.1', '.1.3.6.1.2.1.1.6.0', 'Quito')
print_response (errorIndication, errorStatus, errorIndex, varBinds)
print ()
