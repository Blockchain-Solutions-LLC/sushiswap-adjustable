#!/usr/bin/python3
from brownie import Temp, network, config, accounts
# v2Pair creation code:
#  0xa070f6ef8b3d965b26d725b614c07089809fdb9c104693e45f886a4eb3e36448
# v2Factor creation code2:
#  0x53e0cb2173988bba3d28b06cb0c7036ed01382b22350b23923ca3cfd28b99f51


DEPLOYED = False

def main():
    pass
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False # Currently having an issue with this
    publish_source = False

    if DEPLOYED:
        temp = Temp[-1]
    else:
        temp = Temp.deploy({'from': accounts[0]})

    print(f'\ntemp: {temp}')
    print(f'v2Pair creation code:\n {temp.INIT_CODE_PAIR_HASH()}')
    print(f'v2Factor creation code2:\n {temp.INIT_CODE_PAIR_HASH2()}')
