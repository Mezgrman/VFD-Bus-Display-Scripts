import time

from pyfis.ibis import SerialIBISMaster, TCPIBISMaster
from easysnmp import Session

from config_ibis import *
from config_snmp_stats import *


def main():
    if IBIS_MODE == "TCP":
        ibis = TCPIBISMaster(IBIS_TCP_HOST, IBIS_TCP_PORT)
    elif IBIS_MODE == "SERIAL":
        ibis = SerialIBISMaster(IBIS_SERIAL_PORT)
    snmp = Session(hostname=SNMP_HOST, community='public', version=2)

    prev_time = 0
    prev_in_bytes = 0
    prev_out_bytes = 0
    while True:
        in_bytes = int(snmp.get(IF_HC_IN_OCTETS).value)
        out_bytes = int(snmp.get(IF_HC_OUT_OCTETS).value)

        now = time.time()

        in_rate = (in_bytes-prev_in_bytes) / (now - prev_time)
        out_rate = (out_bytes-prev_out_bytes) / (now - prev_time)

        prev_time = now
        prev_in_bytes = in_bytes
        prev_out_bytes = out_bytes

        ibis.DS009("Down: {:.1f} MB\n{:.2f} MB/s\nUp: {:.1f} MB\n{:.2f} MB/s".format(in_bytes/1048576, in_rate/1048576, out_bytes/1048576, out_rate/1048576))

        time.sleep(5)



if __name__ == "__main__":
    main()
