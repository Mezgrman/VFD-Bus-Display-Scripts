import time

from pyfis.ibis import TCPIBISMaster
from easysnmp import Session


IF_HC_IN_OCTETS = "1.3.6.1.2.1.31.1.1.1.6.1"
IF_HC_OUT_OCTETS = "1.3.6.1.2.1.31.1.1.1.10.1"


def main():
    ibis = TCPIBISMaster("192.168.100.45", 5001)
    snmp = Session(hostname="192.168.100.1", community='public', version=2)

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
