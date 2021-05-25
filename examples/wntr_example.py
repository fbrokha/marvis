#!/usr/bin/env python3

from marvis import ArgumentParser, Network, DockerNode, Node, Scenario, WiFiChannel, SwitchNode
from marvis.mobility_input import WNTRMobilityInput
import wntr


def main():
    scenario = Scenario()

    simulation_time = 1*3600  # in seconds

    net = Network("10.0.0.0", "255.255.255.0", default_channel_type=WiFiChannel, frequency=5860, channel_width=10,
                  tx_power=18.0, standard=WiFiChannel.WiFiStandard.WIFI_802_11p,
                  data_rate=WiFiChannel.WiFiDataRate.OFDM_RATE_BW_6Mbps)

    bridge = SwitchNode('br-1')

    n1 = DockerNode('n1', docker_build_dir='./docker/wntr', command='python3 test_code.py --node_name n1')
    n4 = DockerNode('n4', docker_build_dir='./docker/wntr', command='python3 test_code.py --node_name n4')
    server = DockerNode('server', docker_image='httpd:2.4')

    channel_sb = net.create_channel()
    channel_sb.connect(server)
    channel_sb.connect(bridge)

    channel_1b = net.create_channel()
    channel_1b.connect(n1)
    channel_1b.connect(bridge)

    channel_2b = net.create_channel()
    channel_2b.connect(n4)
    channel_2b.connect(bridge)

    scenario.add_network(net)

    # wn = WNTRMobilityInput(duration=simulation_time, inp_path='docker/wntr/scenario/L-TOWN.inp', step_length=60)
    wn = wntr.network.WaterNetworkModel('docker/wntr/scenario/L-TOWN.inp')
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    for node in scenario.nodes():
        node_pressure = results.node['pressure'].loc[:, node.name]
        node_pressure.to_csv('docker/wntr/filetransfer/' + node.name + '.csv')

    # wntr.add_node_to_mapping(n1, 'n1', 'junction')
    # wntr.add_node_to_mapping(n2, 'n4', 'junction')

    # scenario.add_mobility_input(wntr)

    with scenario as sim:
        # To simulate forever, just do not specifiy the simulation_time parameter.
        sim.simulate(simulation_time=simulation_time)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
