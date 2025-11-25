"""
Mininet script to create a 3-router network topology
Each router connects to 2 hosts on separate LANs
Routers are interconnected on network 20.10.100.0/24

LAN A: 20.10.172.128/26 (62 usable hosts)
LAN B: 20.10.172.0/25 (126 usable hosts)
LAN C: 20.10.172.192/27 (30 usable hosts)
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""
    
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')
    
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    """Network topology with 3 routers and 6 hosts"""
    
    def build(self, **_opts):
        routerA = self.addNode('rA', cls=LinuxRouter, ip='20.10.100.1/24')
        routerB = self.addNode('rB', cls=LinuxRouter, ip='20.10.100.2/24')
        routerC = self.addNode('rC', cls=LinuxRouter, ip='20.10.100.3/24')
        
        switchA = self.addSwitch('s1')
        switchB = self.addSwitch('s2')
        switchC = self.addSwitch('s3')
        
        switchRouter = self.addSwitch('s4')
        
        hostA1 = self.addHost('hA1', ip='20.10.172.130/26', 
                              defaultRoute='via 20.10.172.129')
        hostA2 = self.addHost('hA2', ip='20.10.172.131/26', 
                              defaultRoute='via 20.10.172.129')

        hostB1 = self.addHost('hB1', ip='20.10.172.2/25', 
                              defaultRoute='via 20.10.172.1')
        hostB2 = self.addHost('hB2', ip='20.10.172.3/25', 
                              defaultRoute='via 20.10.172.1')
        
        hostC1 = self.addHost('hC1', ip='20.10.172.194/27', 
                              defaultRoute='via 20.10.172.193')
        hostC2 = self.addHost('hC2', ip='20.10.172.195/27', 
                              defaultRoute='via 20.10.172.193')
        
        self.addLink(switchRouter, routerA,
                    intfName2='rA-eth1',
                    params2={'ip': '20.10.100.1/24'})
        
        self.addLink(switchRouter, routerB,
                    intfName2='rB-eth1',
                    params2={'ip': '20.10.100.2/24'})
        
        self.addLink(switchRouter, routerC,
                    intfName2='rC-eth1',
                    params2={'ip': '20.10.100.3/24'})
        
        self.addLink(switchA, routerA,
                    intfName2='rA-eth0',
                    params2={'ip': '20.10.172.129/26'})
        
        self.addLink(switchB, routerB,
                    intfName2='rB-eth0',
                    params2={'ip': '20.10.172.1/25'})
        
        self.addLink(switchC, routerC,
                    intfName2='rC-eth0',
                    params2={'ip': '20.10.172.193/27'})
        
        self.addLink(hostA1, switchA)
        self.addLink(hostA2, switchA)
        self.addLink(hostB1, switchB)
        self.addLink(hostB2, switchB)
        self.addLink(hostC1, switchC)
        self.addLink(hostC2, switchC)


def run():
    """Create and test the network"""
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    
    info('Starting network\n')
    net.start()
    
    info('Network configuration:\n')
    info('LAN A: 20.10.172.128/26 (Router A at 20.10.172.129)\n')
    info('  hA1: 20.10.172.130\n')
    info('  hA2: 20.10.172.131\n')
    info('LAN B: 20.10.172.0/25 (Router B at 20.10.172.1)\n')
    info('  hB1: 20.10.172.2\n')
    info('  hB2: 20.10.172.3\n')
    info('LAN C: 20.10.172.192/27 (Router C at 20.10.172.193)\n')
    info('  hC1: 20.10.172.194\n')
    info('  hC2: 20.10.172.195\n')
    info('Router interconnect: 20.10.100.0/24\n')
    info('  rA: 20.10.100.1\n')
    info('  rB: 20.10.100.2\n')
    info('  rC: 20.10.100.3\n\n')
    
    info('Testing connectivity within each LAN using pingall\n')
    net.pingAll()
    
    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()