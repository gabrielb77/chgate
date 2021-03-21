#!/usr/bin/env python3

from pythonping import ping
from pyroute2 import IPRoute


def main():
#    print("Hello World!")
#    ping('192.168.0.1', verbose=True, size=248, count=3)
#    ping('www.google.com', verbose=True, size=248, count=3)

  response = ping("192.168.0.33", size=248, count=1)
  if response is response:
    print("Dio timeout")

  ipr = IPRoute()

  print(ipr.get_addr(family=2))

  print(ipr.get_default_routes(family=0, table=254))

  ipr.route("del", dst="default", gateway="192.168.0.40")
  ipr.route("add", dst="default", gateway="192.168.0.1")


if __name__ == "__main__":
  main()
