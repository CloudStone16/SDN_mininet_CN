#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time

def run():
    setLogLevel('info')
    
    info('*** Creating network\n')
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    
    info('*** Adding controller\n')
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    
    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    
    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    
    info('*** Adding links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    
    # Topology: s1 -- s2 -- s3
    #             \       /
    #              -------
    link_s1_s2 = net.addLink(s1, s2)
    link_s2_s3 = net.addLink(s2, s3)
    link_s1_s3 = net.addLink(s1, s3)
    
    info('*** Starting network\n')
    net.start()
    
    info('*** Waiting for topology discovery (10s)\n')
    time.sleep(10)
    
    info('\n*** Simulating Topology Changes ***\n')
    info('>>> Bringing down link between s1 and s2\n')
    net.configLinkStatus('s1', 's2', 'down')
    time.sleep(5)
    
    info('>>> Bringing up link between s1 and s2\n')
    net.configLinkStatus('s1', 's2', 'up')
    time.sleep(5)
    
    info('>>> Stopping switch s3\n')
    net.get('s3').stop()
    time.sleep(5)
    
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    run()
