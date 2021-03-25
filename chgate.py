#!/usr/bin/env python3

from pyroute2 import IPRoute
from pyroute2 import IPDB
from ping3 import ping
import ipaddress
from time import sleep
import ipcalc
import json
import socket


def main():
  NetDict = {
    "dc4":{
      "1":{
        "subnet":"10.32.80.0/24",
        "dgw":"10.32.80.1"
      },
    },
    "cs":{
      "1":{
        "subnet":"10.255.15.192/27",
        "dgw":"10.255.15.193"
      },
      "2":{
        "subnet":"10.255.15.224/27",
        "dgw":"10.255.15.225"
      }
    },
    "eqx":{
      "1":{
        "subnet":"10.255.15.128/27",
        "dgw":"10.255.15.129"
      },
      "2":{
        "subnet":"10.255.15.160/27",
        "dgw":"10.255.15.161"
      }
    },
    "casa":{
      "1":{
        "subnet":"192.168.0.0/24",
        "dgw":"192.168.0.1"
      }
    }
  }

  HostConfig = {
    "eqx-vm-jmp-01":{
      "ip_ori":"10.255.15.135",
      "gw_ori":"10.255.15.129",
      "ip_alt":"a",
      "gw_alt":"10.255.15.225"
    },
    "eqx-vm-dlg-01":{
      "ip_ori":"10.255.15.136",
      "gw_ori":"10.255.15.129",
      "ip_alt":"10.255.15.167",
      "gw_alt":"10.255.15.225"
    },
    "eqx-vm-flw-01":{
      "ip_ori":"10.255.15.137",
      "gw_ori":"10.255.15.129",
      "ip_alt":"10.255.15.168",
      "gw_alt":"10.255.15.225"
    },
    "eqx-vm-jmp-02":{
      "ip_ori":"10.255.15.165",
      "gw_ori":"10.255.15.225",
      "ip_alt":"10.255.15.138",
      "gw_alt":"10.255.15.129"
    },
    "eqx-vm-tucu-02":{
      "ip_ori":"10.255.15.166",
      "gw_ori":"10.255.15.129",
      "ip_alt":"10.255.15.131",
      "gw_alt":"10.255.15.225"
    },
    "cs-vm-jmp-01":{
      "ip_ori":"10.255.15.195",
      "gw_ori":"10.255.15.129",
      "ip_alt":"10.255.15.229",
      "gw_alt":"10.255.15.225"
    },
    "cs-vm-dlg-01":{
      "ip_ori":"10.255.15.196",
      "gw_ori":"10.255.15.129",
      "ip_alt":"10.255.15.230",
      "gw_alt":"10.255.15.225"
    },
    "cs-vm-flw-01":{
      "ip_ori":"10.255.15.197",
      "gw_ori":"10.255.15.129",
      "ip_alt":"10.255.15.231",
      "gw_alt":"10.255.15.225"
    },
    "cs-vm-jmp-02":{
      "ip_ori":"10.255.15.227",
      "gw_ori":"10.255.15.225",
      "ip_alt":"10.255.15.198",
      "gw_alt":"10.255.15.193"
    },
    "cs-vm-tucu-02":{
      "ip_ori":"10.255.15.228",
      "gw_ori":"10.255.15.225",
      "ip_alt":"10.255.15.198",
      "gw_alt":"10.255.15.193"
    },
  }

dc4-vm-jmp-01	dc4-serv-01	DC4	10.32.80.30	
dc4-vm-dlg-01	dc4-serv-01	DC4	10.32.80.31	
dc4-vm-flw-01	dc4-serv-01	DC4	10.32.80.32	
dc4-vm-jmp-02	dc4-serv-02	DC4	10.32.80.33	
dc4-vm-jmp-03	dc4-serv-03	DC4	10.32.80.34	
dc4-vm-tucu-01	dc4-serv-01	DC4	10.32.80.35	

























  print(json.dumps(NetDict, sort_keys=False, indent=2))

#  ipr = IPRoute()
#  print(ipr.get_addr(family=2))
#  print(ipr.get_default_routes(family=0, table=254))
#  ipr.route("del", dst="default", gateway="192.168.0.40")
#  ipr.route("add", dst="default", gateway="192.168.0.1")

  # obtener mi ip
  DevOK = False
  Device = "wlp5s0"
  ipr = IPRoute()
  SubnetMatch = False
  MyHostname = socket.gethostname()
#  print(ipr.get_addr(family=2))
#  print(ipr.get_links())
#  Links = ipr.get_links()
#  print(Links.get_attr("IFLA_IFNAME"))
#  with IPRoute() as ipr:
#    avail_interfaces = [Link.get_attr("IFLA_IFNAME") for Link in ipr.get_links()]
#  avail_interfaces2 = [Link2.get_attr("IFLA_IFNAME") for Link2 in ipr2.get_links()]

#  for Devs in ipr.get_links():
#    Dev = Devs.get_attr("IFLA_IFNAME")
#    IpAddr = Devs.get_attr("IFA_ADDRESS")
#    if Dev in Device:
#      IpAddr = Devs.get_attr("IFA_ADDRESS")
#      DevOK = True
#      break

#  if DevOK:
#    print("Tengo dev ok")
#    print("IP: " + str(IpAddr))
#  else:
#    print("Dev mal")

#  ifidx = ipr.link_lookup(ifname=Device)[0]
#  print(ipr.get_addr(index=ifidx))

  ipdb = IPDB()
#  print(ipdb.routes['default']['oif'])
#  Testall = ipdb.interfaces[ipdb.routes['default']['oif']]
#  ifname = ipdb.interfaces[ipdb.routes['default']['oif']].ifname
#  Test2 = ipdb.interfaces[ipdb.routes['default']['oif']].address
#  ip1,ip2 = ipdb.interfaces[ipdb.routes['default']['oif']].ipaddr
  IpTuple = ipdb.interfaces[ipdb.routes['default']['oif']].ipaddr
#  print(ifname + " <-> " + str(ip1[0]) + "/" + str(ip1[1]))
#  print(Test2)
#  print(Testall)
#  print("############################################################")
#  print(ip1[0])
 # print(ipr.addr('get', index=ifidx))
#  print(ipr.get_links(index=ifidx))
#  try:
#    ip = ipaddress.IPv4Address(ip1[0])
#   # ip = ipaddress.ip_address(ip1[0])
#    print('%s is a correct IP%s address.' % (ip, ip.version))
#  except ValueError:
#    print('address/netmask is invalid: %s' % ip1[0])



#  print(type(ip1))
#  print(type(ip2))

  for val in IpTuple:
#    print("Tuple: " + str(IpTuple))
#    print("val: " + str(val))
    for val2 in val:
#      print("Segundo for")
#      print("Sec Tuple: " + str(val))
#      print("Sec tuple val: " + str(val2))

 #     print("VAL2: " + str(val2))
      try:
        ValidIP = ipaddress.IPv4Address(str(val2))
        ValidPrefix = val[1]
        break
      except ValueError:
        pass


  print("VALID IP: " + str(ValidIP))
  print("VALID pref: " + str(ValidPrefix))
#  MySubnet = str(ValidIP) + "/" + str(ValidPrefix)
  MySubnet = str(ipcalc.Network(str(ValidIP) + "/" + str(ValidPrefix)).network())
  MyPrefix = str(ValidPrefix)


#  ValidIP = None
#  while not ValidIP:
#    try:
#      ValidIP = ipaddress.IPv4Address(ip1[0])
#      print(ipdb.interfaces[ipdb.routes['default']['oif']].ipaddr)
#    except ValueError:
#      ip1,ip2 = ipdb.interfaces[ipdb.routes['default']['oif']].ipaddr
#      print(ipdb.interfaces[ipdb.routes['default']['oif']].ipaddr)
#      sleep(2)
#      print("wait...")
#      pass

#  print("IP OK: " + str(ValidIP))
#  print(avail_interfaces)

# determinar la red
# determinar el DC

  for dclist in NetDict:
    print(dclist)
    for snid in NetDict[dclist]:
      print(snid)
      Subnet = NetDict[dclist][snid]["subnet"]
      DGW = NetDict[dclist][snid]["dgw"]
      print("######: " + MySubnet + "/" + MyPrefix + "  ########  " + Subnet + " Ping a: " + DGW)

      if MySubnet in Subnet:
        MyDC = dclist
        SubnetMatch = True

  try:
    print("Estoy en: " + MyDC)
  except:
    print("No se encontro DC para subnet " + MySubnet + "/" + MyPrefix)


# probar los gateways de ese DC

  for TestGw in NetDict[MyDC]:
    dgw = NetDict[MyDC][TestGw]["dgw"]
    print("Hace ping a: " + NetDict[MyDC][TestGw]["dgw"])
    if ping(dgw):
      print("Todo ok, no se hace nada")
      print(dgw + " alive")
    else:
      print(dgw + " muerto")
      print("setear ip alternativa")





# configurar segun gateway que responda

  dgw = "192.168.0.1"

  if ping(dgw):
    print(dgw + " alive")
  else:
    print(dgw + " ripeo")


if __name__ == "__main__":
  main()
