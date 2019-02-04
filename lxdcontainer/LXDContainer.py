import random
import string
import subprocess

from ns.network import Node
import ns.tap_bridge

from tuntap.TunTapDevice import TunTapDevice
from bridge.BridgeDevice import BridgeDevice

class LXDContainer:

    def __init__(self, name, image):
        self.tun = None
        self.br = None
        self.name = name
        self.image = image
        self.node = None
        self.tapbridge = None
        self.domain = None
        self.interfaces = []

    def create(self):
        subprocess.call(["lxc", "init", self.image, self.name])

    def connect_to_netdevice(self, ns3node, netdevice, ipv4_addr, ip_prefix, broadcast_addr, bridge_addr):
        print("k1")
        # Create Tun-Tap Device and Bridge
        self.tun = TunTapDevice("tun-"+self.name)
        self.tun.create()
        self.tun.up()

        print("k2")
        self.br = BridgeDevice("br-"+self.name)
        self.br.create()
        self.br.add_interface(self.tun)
        self.br.up()
        #subprocess.call(["sudo", "ip", "addr", "add", bridge_addr + "/" + str(ip_prefix), "broadcast",
        #                 broadcast_addr, "dev", self.br.name])

        print("k3")
        suffix_length = 5
        interface_name = "vnet" + ''.join(random.choice(string.ascii_lowercase) for _ in range(suffix_length))
        while interface_name in self.interfaces:
            interface_name = "vnet" + ''.join(random.choice(string.ascii_lowercase) for _ in range(suffix_length))
        self.interfaces.append(interface_name)

        print(subprocess.call(["lxc", "config", "device", "add", self.name, interface_name, "nic",
                               "name="+interface_name, "nictype=bridged", "parent="+self.br.name]))
        self.execute_command("ifconfig " + interface_name + " up")
        #self.execute_command("ip addr add " + ipv4_addr + "/" + ip_prefix + " broadcast " +
        #                     broadcast_addr + " dev " + interface_name)
        self.execute_command("ip addr add " + ipv4_addr + "/" + ip_prefix + " dev " + interface_name)
        self.execute_command("ifconfig eth0 down")
        # self.execute_command("route add default gw "+bridge_addr+" "+interface_name)
        # self.execute_command("route add default gw 0.0.0.0 "+interface_name)

        #netdevice = ns.csma.CsmaNetDevice()
        print("1")
        # Connect to ns-3
        self.tapbridge = ns.tap_bridge.TapBridgeHelper()
        print("2")
        self.tapbridge.SetAttribute("Mode", ns.core.StringValue("UseBridge"))
        print("3")
        self.tapbridge.SetAttribute("DeviceName", ns.core.StringValue(self.tun.name))
        print("3b")
        #self.node = Node()
        print("4")
        #print(netdevice)
        #print(type(netdevice))
        #self.node.AddDevice(netdevice)
        self.tapbridge.Install(ns3node, netdevice)
        print("5")
        print("6")
        return netdevice

    def execute_command(self, command, sudo=False):
        print("exec: "+str(["lxc", "exec", self.name, "--", command]))
        if sudo:
            print(subprocess.call("lxc exec " + self.name + " -- sudo " + command, shell=True)) # TODO: Verify that sudo works without password
        else:
            print(subprocess.call("lxc exec " + self.name + " -- " + command, shell=True))

    def start(self):
        subprocess.call(["lxc", "start", self.name])

    def stop(self):
        subprocess.call(["lxc", "stop", self.name])

    def destroy(self):
        self.stop()
        subprocess.call(["lxc", "delete", self.name])
        if self.br:
            self.br.down()
            self.br.destroy()
        if self.tun:
            self.tun.down()
            self.tun.destroy()

