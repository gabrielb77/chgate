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
      "prefix_ori":"27",
      "ip_alt":"10.255.15.163",
      "gw_alt":"10.255.15.161",
      "prefix_alt":"27"
    },
    "eqx-vm-dlg-01":{
      "ip_ori":"10.255.15.136",
      "gw_ori":"10.255.15.129",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.167",
      "gw_alt":"10.255.15.161",
      "prefix_alt":"27"
    },
    "eqx-vm-flw-01":{
      "ip_ori":"10.255.15.137",
      "gw_ori":"10.255.15.129",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.168",
      "gw_alt":"10.255.15.161",
      "prefix_alt":"27"
    },
    "eqx-vm-jmp-02":{
      "ip_ori":"10.255.15.165",
      "gw_ori":"10.255.15.161",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.138",
      "gw_alt":"10.255.15.129",
      "prefix_alt":"27"
    },
    "eqx-vm-tucu-02":{
      "ip_ori":"10.255.15.166",
      "gw_ori":"10.255.15.161",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.131",
      "gw_alt":"10.255.15.129",
      "prefix_alt":"27"
    },
    "cs-vm-jmp-01":{
      "ip_ori":"10.255.15.195",
      "gw_ori":"10.255.15.129",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.229",
      "gw_alt":"10.255.15.225",
      "prefix_alt":"27"
    },
    "cs-vm-dlg-01":{
      "ip_ori":"10.255.15.196",
      "gw_ori":"10.255.15.193",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.230",
      "gw_alt":"10.255.15.225",
      "prefix_alt":"27"
    },
    "cs-vm-flw-01":{
      "ip_ori":"10.255.15.197",
      "gw_ori":"10.255.15.193",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.231",
      "gw_alt":"10.255.15.225",
      "prefix_alt":"27"
    },
    "cs-vm-jmp-02":{
      "ip_ori":"10.255.15.227",
      "gw_ori":"10.255.15.225",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.198",
      "gw_alt":"10.255.15.193",
      "prefix_alt":"27"
    },
    "cs-vm-tucu-02":{
      "ip_ori":"10.255.15.228",
      "gw_ori":"10.255.15.225",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.199",
      "gw_alt":"10.255.15.193",
      "prefix_alt":"27"
    },
    "gbnotebook":{
      "ip_ori":"192.168.0.30",
      "gw_ori":"192.168.0.1",
      "prefix_ori":"24",
      "ip_alt":"192.168.0.80",
      "gw_alt":"192.168.0.102",
      "prefix_alt":"24"
    }
  }



  HostConfig2 = {
    "eqx":{
      "eqx-vm-jmp-01":{
        "pri":{
          "ip":"10.255.15.135",
          "gw":"10.255.15.129",
          "prefix":"27"
        },
        "sec":{
          "ip":"10.255.15.163",
          "gw":"10.255.15.161",
          "prefix":"27"
        }
      },
    },
    "eqx-vm-dlg-01":{
      "ip_ori":"10.255.15.136",
      "gw_ori":"10.255.15.129",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.167",
      "gw_alt":"10.255.15.161",
      "prefix_alt":"27"
    },
    "eqx-vm-flw-01":{
      "ip_ori":"10.255.15.137",
      "gw_ori":"10.255.15.129",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.168",
      "gw_alt":"10.255.15.161",
      "prefix_alt":"27"
    },
    "eqx-vm-jmp-02":{
      "ip_ori":"10.255.15.165",
      "gw_ori":"10.255.15.161",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.138",
      "gw_alt":"10.255.15.129",
      "prefix_alt":"27"
    },
    "eqx-vm-tucu-02":{
      "ip_ori":"10.255.15.166",
      "gw_ori":"10.255.15.161",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.131",
      "gw_alt":"10.255.15.129",
      "prefix_alt":"27"
    },
    "cs-vm-jmp-01":{
      "ip_ori":"10.255.15.195",
      "gw_ori":"10.255.15.129",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.229",
      "gw_alt":"10.255.15.225",
      "prefix_alt":"27"
    },
    "cs-vm-dlg-01":{
      "ip_ori":"10.255.15.196",
      "gw_ori":"10.255.15.193",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.230",
      "gw_alt":"10.255.15.225",
      "prefix_alt":"27"
    },
    "cs-vm-flw-01":{
      "ip_ori":"10.255.15.197",
      "gw_ori":"10.255.15.193",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.231",
      "gw_alt":"10.255.15.225",
      "prefix_alt":"27"
    },
    "cs-vm-jmp-02":{
      "ip_ori":"10.255.15.227",
      "gw_ori":"10.255.15.225",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.198",
      "gw_alt":"10.255.15.193",
      "prefix_alt":"27"
    },
    "cs-vm-tucu-02":{
      "ip_ori":"10.255.15.228",
      "gw_ori":"10.255.15.225",
      "prefix_ori":"27",
      "ip_alt":"10.255.15.199",
      "gw_alt":"10.255.15.193",
      "prefix_alt":"27"
    },
    "gbnotebook":{
      "pri":{
        "ip":"192.168.0.30",
        "gw":"192.168.0.1",
        "prefix":"24"
      },
      "sec":{
        "ip":"192.168.0.80",
        "gw":"192.168.0.102",
        "prefix":"24"
      }
    }
  }













#  print(json.dumps(NetDict, sort_keys=False, indent=2))
  print(json.dumps(HostConfig, sort_keys=False, indent=2))
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
  index = ipdb.interfaces[ipdb.routes['default']['oif']].index
#  index = ipr.link_lookup(ifname='wlp5s0')[0]
  print(index)
  print(ipdb.interfaces[ipdb.routes['default']['oif']])
  try:
    ipr.addr('add', index, address='192.168.0.123', mask=24)
  except:
    print("Algo salio mal")

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
    if ping(dgw, size=248, timeout=3):
      print("Todo ok, no se hace nada")
      print(dgw + " alive")
    else:
      print(dgw + " muerto")
      print("setear ip alternativa")
      for Lala in HostConfig:
        print("------------------------------------------------------------------")
        print(Lala)
        print(MyHostname)
        if MyHostname in Lala:
          print("Estoy en config")
          IpAlt = HostConfig[Lala]["ip_alt"]
          PrefixAlt = HostConfig[Lala]["prefix_alt"]
          CIDRAlt = HostConfig[Lala]["ip_alt"] + "/" + HostConfig[Lala]["prefix_alt"]
          GatewayAlt = HostConfig[Lala]["gw_alt"]
          GatewayOri = HostConfig[Lala]["gw_ori"]
          print("IP ORI: " + HostConfig[Lala]["ip_ori"])
          print("GW ORI: " + HostConfig[Lala]["gw_ori"])
          print("IP ALT: " + HostConfig[Lala]["ip_alt"])
          print("GW ALT: " + HostConfig[Lala]["gw_alt"])
          print("CIDR ALT: " + CIDRAlt)
          ipdb.interfaces[ipdb.routes['default']['oif']].add_ip(CIDRAlt)
          try:
            ipr.route("del", dst="0.0.0.0", gateway=GatewayOri)
          except:
            print("No se pudo borrar gateway" + GatewayOri)
          try:
            ipdb.routes.add({'dst': 'default','gateway': GatewayAlt}).commit()
          except:
            print("No se pudo agregar gw" + GatewayAlt)
          try:
            index = ipdb.interfaces[ipdb.routes['default']['oif']].index
            ipr.addr('add', index, address='192.168.0.123', mask=24)
          except:
            print("Algo salio mal")
        else:
          print("No estoy en config")





# configurar segun gateway que responda

  dgw = "192.168.0.1"

  if ping(dgw):
    print(dgw + " alive")
  else:
    print(dgw + " ripeo")


if __name__ == "__main__":
  main()
