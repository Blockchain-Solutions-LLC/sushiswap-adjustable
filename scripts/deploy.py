#!/usr/bin/python3
from brownie import UniswapV2Factory, UniswapV2Router02, WETH9, network, config, accounts
# from brownie import  WETH9, network, config, accounts

DEVELOPMENT = True

def main():
    pass
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False # Currently having an issue with this
    publish_source = False

    # deploy token
    global DEVELOPMENT
    global factor_address
    global weth_address

    if DEVELOPMENT:
        weth = WETH9.deploy({'from': accounts[0]})
        weth_address = weth.address

    print(f'weth: {weth_address}')

    factory = UniswapV2Factory.deploy(accounts[0],{'from': accounts[0]})

    router = UniswapV2Router02.deploy(factory.address, weth_address, {'from': accounts[0]})

    # print(f'router: {router}') #
