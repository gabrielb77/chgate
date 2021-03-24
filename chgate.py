#!/usr/bin/env python3

from pyroute2 import IPRoute
from pyroute2 import IPDB
from ping3 import ping
import ipaddress
from time import sleep
import ipcalc

def main():
  NetDict = {
    "dc4-sn1":{
      "subnet":"10.32.80.0/24",
      "dgw":"10.32.80.1"
    },
    "cs-sn1":{
      "subnet":"10.255.15.192/27",
      "dgw":"10.255.15.193"
    },
    "cs-sn2":{
      "subnet":"10.255.15.224/27",
      "dgw":"10.255.15.225"
    },
    "eqx-sn1":{
      "subnet":"10.255.15.128/27",
      "dgw":"10.255.15.129"
    },
    "eqx-sn2":{
      "subnet":"10.255.15.160/27",
      "dgw":"10.255.15.161"
    }
  }

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
  MySubnet = ipcalc.Network(str(ValidIP) + "/" + str(ValidPrefix))
  MySubnet = MySubnet.network()

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
    Subnet = NetDict[dclist]["subnet"]
    DGW = NetDict[dclist]["dgw"]
    print("######: " + str(MySubnet) + "  ########  " + Subnet)

    if str(MySubnet) in Subnet:
      print("Estoy en dclist")
      MyDC = dclist
      SubnetMatch = True

  try:
    print(MyDC)
  except:
    print("No se encontro DC para subnet " + str(MySubnet))
#  print(NetDict)


# probar los gateways de ese DC
# configurar segun gateway que responda

  dgw = "192.168.0.1"

  if ping(dgw):
    print(dgw + " alive")
  else:
    print(dgw + " ripeo")


if __name__ == "__main__":
  main()
