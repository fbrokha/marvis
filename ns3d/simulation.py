import argparse
import os
import shutil
import subprocess
import sys
import yaml

class Simulation:

    def __init__(self):
        self.ns3_home_dir = os.getenv('NS3_HOME', None)
        if self.ns3_home_dir is None:
            print('Please set the "NS3_HOME" environment variable containing the ns3-sources and waf!',
                  file=sys.stderr)
            exit(-1)
        if self.__setup() != 0:
            print('There was an error setting up iptables for the simulation. Exiting!', file=sys.stderr)
            exit(-1)

        self.networks = set()

    def __setup(self):
        return_code = subprocess.call("sudo net/fix-iptables.sh", shell=True, stdout=subprocess.PIPE)
        return return_code

    def prepare(self):
        """Prepares the simulation by building docker containers.
        """
        pass

    def simulate(self, time):
        """Simulate the network

        :param float time: The simulation timeout in seconds.
        """
        pass

    def teardown(self):
        """Tear down the simulation.
        This also stops and destroys docker containers.
        """
        pass

    def add_network(self, network):
        """Add a network to be simulated.
        """
        self.networks.append(network)
