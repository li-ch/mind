"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- host
         \          /
          \ switch /

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        switch1 = self.addSwitch( 's1' )
        switch2 = self.addSwitch( 's2' )

        # Add links
        self.addLink( leftHost, switch1 )
        self.addLink( leftHost, switch2 )
        self.addLink( switch1, rightHost )
        self.addLink( switch2, rightHost )

topos = { 'mytopo': ( lambda: MyTopo() ) }
