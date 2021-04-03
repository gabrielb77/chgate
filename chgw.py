#!/usr/bin/env python3

from pyroute2 import IPRoute
from pyroute2 import IPDB
from ping3 import ping
import ipaddress
from time import sleep
import ipcalc
import socket


def main():
  HostStaticConfig = {
    "eqx-vm-jmp-01":{
      "pri":{
        "ip":"10.255.15.135",
        "gw":"10.255.15.129",
        "prefix":"27",
        "dc":"eqx"
      },
      "sec":{
        "ip":"10.255.15.163",
        "gw":"10.255.15.161",
        "prefix":"27",
        "dc":"eqx"
      }
    },
    "eqx-vm-dlg-01":{
      "pri":{
        "ip":"10.255.15.136",
        "gw":"10.255.15.129",
        "prefix":"27",
        "dc":"eqx"
      },
      "sec":{
        "ip":"10.255.15.167",
        "gw":"10.255.15.161",
        "prefix":"27",
        "dc":"eqx"
      },
    },
    "eqx-vm-flw-01":{
      "pri":{
        "ip":"10.255.15.137",
        "gw":"10.255.15.129",
        "prefix":"27",
        "dc":"eqx"
      },
      "sec":{
        "ip":"10.255.15.168",
        "gw":"10.255.15.161",
        "prefix":"27",
        "dc":"eqx"
      },
    },
    "eqx-vm-jmp-02":{
      "pri":{
        "ip":"10.255.15.165",
        "gw":"10.255.15.161",
        "prefix":"27",
        "dc":"eqx"
      },
      "sec":{
        "ip":"10.255.15.138",
        "gw":"10.255.15.129",
        "prefix":"27",
        "dc":"eqx"
      },
    },
    "eqx-vm-tucu-02":{
      "pri":{
        "ip":"10.255.15.166",
        "gw":"10.255.15.161",
        "prefix":"27",
        "dc":"eqx"
      },
      "sec":{
        "ip":"10.255.15.131",
        "gw":"10.255.15.129",
        "prefix":"27",
        "dc":"eqx"
      },
    },
    "cs-vm-jmp-01":{
      "pri":{
        "ip":"10.255.15.195",
        "gw":"10.255.15.129",
        "prefix":"27",
        "dc":"cs"
      },
      "sec":{
        "ip":"10.255.15.229",
        "gw":"10.255.15.225",
        "prefix":"27",
        "dc":"cs"
      },
    },
    "cs-vm-dlg-01":{
      "pri":{
        "ip":"10.255.15.196",
        "gw":"10.255.15.193",
        "prefix":"27",
        "dc":"cs"
      },
      "sec":{
        "ip":"10.255.15.230",
        "gw":"10.255.15.225",
        "prefix":"27",
        "dc":"cs"
      },
    },
    "cs-vm-flw-01":{
      "pri":{
        "ip":"10.255.15.197",
        "gw":"10.255.15.193",
        "prefix":"27",
        "dc":"cs"
      },
      "sec":{
        "ip":"10.255.15.231",
        "gw":"10.255.15.225",
        "prefix":"27",
        "dc":"cs"
      },
    },
    "cs-vm-jmp-02":{
      "pri":{
        "ip":"10.255.15.227",
        "gw":"10.255.15.225",
        "prefix":"27",
        "dc":"cs"
      },
      "sec":{
        "ip":"10.255.15.198",
        "gw":"10.255.15.193",
        "prefix":"27",
        "dc":"cs"
      },
    },
    "cs-vm-tucu-02":{
      "pri":{
        "ip":"10.255.15.228",
        "gw":"10.255.15.225",
        "prefix":"27",
        "dc":"cs"
      },
      "sec":{
        "ip":"10.255.15.199",
        "gw":"10.255.15.193",
        "prefix":"27",
        "dc":"cs"
      },
    },
    "gbnotebook":{
      "pri":{
        "ip":"192.168.0.80",
        "gw":"192.168.0.102",
        "prefix":"24",
        "dc":"casa"
      },
      "sec":{
        "ip":"192.168.0.30",
        "gw":"192.168.0.1",
        "prefix":"24",
        "dc":"casa"
      },
    }
  }


  ipr = IPRoute()
  ipdb = IPDB()
  MyHostname = socket.gethostname()

  ## Pruebo si tengo default gw configurado
  try:
    RouteList = ipr.get_default_routes(family=0, table=254)[0]["attrs"]
  except:
    print("No tengo default gw. Me voy.")
    ipr.close()
    quit()

  ## Busco default gateway actual
  for Routes in RouteList:
    if Routes[0] in "RTA_GATEWAY":
      DefGWActual = Routes[1]

  if ping(DefGWActual, size=248, timeout=3):
    print(DefGWActual + " alive")
    print("Todo ok, no se hace nada")
  else:
    print("El default gateway configurado " + DefGWActual + " no responde")
    for MyHostConfig in HostStaticConfig:
      if MyHostConfig in MyHostname:
        for TestLoop in HostStaticConfig[MyHostname]:
          CfgMyDc = HostStaticConfig[MyHostname][TestLoop]["dc"]
          CfgGateway = HostStaticConfig[MyHostname][TestLoop]["gw"]
          CfgIpAddr = HostStaticConfig[MyHostname][TestLoop]["ip"]
          CfgNetmask = HostStaticConfig[MyHostname][TestLoop]["prefix"]
          IpTuple = ipdb.interfaces[ipdb.routes['default']['oif']].ipaddr
          ## Busco direccion ip configurada y valido string
          for val in IpTuple:
            for val2 in val:
              try:
                ValidIP = ipaddress.IPv4Address(str(val2))
                ValidPrefix = val[1]
                break
              except ValueError:
                pass
          IpAddrActual = str(ValidIP)
          PrefixActual = str(ValidPrefix)
          SubnetActual = str(ipcalc.Network(str(ValidIP) + "/" + str(ValidPrefix)).network())


          ## Si el gateway que voy a configurar es el mismo que tengo, no hago nada
          if DefGWActual != CfgGateway:
            print("Eliminar config actual: " + IpAddrActual + "/" + PrefixActual + " via: " + DefGWActual)
            print("Reemplazar por :" + CfgIpAddr + "/" + CfgNetmask + " via: " + CfgGateway)

            ## Saco ip vieja, pongo ip nueva
            try:
              IfIndex = ipdb.interfaces[ipdb.routes['default']['oif']].index
            except:
              print("Sigo sin default gw")

            try:
              ipr.addr('del', index=IfIndex, address=IpAddrActual, mask=int(PrefixActual))
              ipr.addr('add', index=IfIndex, address=CfgIpAddr, mask=int(CfgNetmask))
            except:
              print("Algo salio mal configurando la ip")

            ## Agrego default gateway nuevo
            ipdb.routes.add({'dst': 'default','gateway': CfgGateway}).commit()

            ipdb.release()
            ipr.close()


if __name__ == "__main__":
  main()
