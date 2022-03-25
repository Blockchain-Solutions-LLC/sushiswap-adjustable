from brownie import UniswapV2Factory, UniswapV2Router02, Token, WETH9, network, config, accounts, Contract
import pytest
import math
from brownie.network.state import Chain
initial_setup_complete = False


CREATE_INITIAL_LIQUIDITY = True
# FACTORY_ADDRESS = '0x058E5b32AE3db4b3e3910858900B284ba8AB1466'
# TESTING_ACCOUNT_TWO = '0xAb0517Ed8EED859deD85Bad8018D462f236e2c07'


def main():
#    deploy_token()
    pass

def initial_setup():
    # deploy router
    # deploy token
    # create liquidity
    dev = accounts.add(config["wallets"]["from_key"])
    global FACTORY_ADDRESS

    # chain = network.state.Chain()
    # current_block = chain.time()
    # big_num = 10**18

    if CREATE_INITIAL_LIQUIDITY:
        print(f'creating initial liquidity...')
        # factory_address = '0x287206ac9b8791ab73767db09eF0Dc497d7f281a'
        # factory_address = '0x6b175474e89094c44da98b954eedeac495271d0f'
        weth = WETH9.deploy({'from': accounts[0]})
        weth_address = weth.address
        token = deploy_token()
        # tokens_to_add = 10 ** 10
        # ETH_to_add = 10 ** 10
        fee_to_setter = accounts[0]

        factory = UniswapV2Factory.deploy(accounts[0], {'from': accounts[0]})
        router = UniswapV2Router02.deploy(factory.address, weth_address, {'from': accounts[0]})

        add_liquidity()
        # tx = factory.setFeeTo(accounts[1], {'from': accounts[0]})
        # tx = weth.deposit({'from': accounts[0], 'value': ETH_to_add})
        # tx = token.approve(router.address, tokens_to_add, {'from': accounts[0]})
        # tx = weth.approve(router.address, ETH_to_add, {'from': accounts[0]})
        #
        # # setFeeTo
        # tx = router.addLiquidity(token.address, weth_address, tokens_to_add, ETH_to_add,
        #                     1, 1, accounts[0], current_block + big_num, {'from': accounts[0]})
        #
        # for k, v in tx.events.items():
        #     print(f'{k}: {v}')

        # print(f'\n adding liquidity again...')
        # swap_tokens()
        # tx = weth.deposit({'from': accounts[0], 'value': ETH_to_add})
        # tx = token.approve(router.address, tokens_to_add, {'from': accounts[0]})
        # tx = weth.approve(router.address, ETH_to_add, {'from': accounts[0]})
        #
        # # setFeeTo
        # tx = router.addLiquidity(token.address, weth_address, tokens_to_add, ETH_to_add,
        #                     1, 1, accounts[0], current_block + big_num, {'from': accounts[0]})
        #
        # for k, v in tx.events.items():
        #     print(f'{k}: {v}')


        # router.addLiquidityETH(token.address, tokens_to_add, 0, 0, accounts[0], current_block + 600,
        #                        {'from': accounts[0], 'value': ETH_to_add})

@pytest.fixture
def recurring_setup():
    global initial_setup_complete
    if not initial_setup_complete:
        initial_setup()


def deploy_token():
    dev = accounts.add(config["wallets"]["from_key"])
    token = Token.deploy('my_token', 'MT', 18, 10**22, {'from': accounts[0]})
    return token


def add_liquidity(tokens_to_add=10**10, ETH_to_add=10**10):
    chain = network.state.Chain()
    current_block = chain.time()
    big_num = 10**18

    factory = UniswapV2Factory[-1]
    router  = UniswapV2Router02[-1]
    weth = WETH9[-1]
    token = Token[-1]

    tx = factory.setFeeTo(accounts[1], {'from': accounts[0]})
    tx = weth.deposit({'from': accounts[0], 'value': ETH_to_add})
    tx = token.approve(router.address, tokens_to_add, {'from': accounts[0]})
    tx = weth.approve(router.address, ETH_to_add, {'from': accounts[0]})

    # setFeeTo
    tx = router.addLiquidity(token.address, weth.address, tokens_to_add, ETH_to_add,
                             1, 1, accounts[0], current_block + big_num, {'from': accounts[0]})


def swap_tokens(amount_to_swap=10**6, reverse = False):
    dev = accounts.add(config["wallets"]["from_key"])
    factory = UniswapV2Factory[-1]
    router = UniswapV2Router02[-1]
    weth = WETH9[-1]
    token = Token[-1]
    path = [WETH9[-1].address, Token[-1].address]
    if reverse:
        path = path[::-1]
    # pair_contract_address = factory.getPair(path[0], path[1])
    # pair_contract = interface.IUniswapV2Pair(pair_contract_address)
    chain = network.state.Chain()
    current_block = chain.time()
    big_num = 10**18

    tx = weth.deposit({'from': accounts[0], 'value': amount_to_swap})
    tx = token.approve(router.address, amount_to_swap, {'from': accounts[0]})
    tx = weth.approve(router.address, amount_to_swap, {'from': accounts[0]})

    tx = router.swapExactTokensForTokens(amount_to_swap, 1, path, accounts[0], current_block + big_num)


def test_can_trade(recurring_setup):
    dev = accounts.add(config["wallets"]["from_key"])
    router = UniswapV2Router02[-1]
    amount_of_tokens_to_swap = 5000
    eth_to_send = 5000000
    token = Token[-1]
    weth = WETH9[-1]
    chain = network.state.Chain()
    current_block = chain.time()

    initial_eth = accounts[0].balance()
    initial_tokens = token.balanceOf(accounts[0])
    tx = router.swapExactETHForTokens(0, [weth.address, token.address],
                                      accounts[0], current_block + 360, {'from': accounts[0], 'value': eth_to_send} )

    final_eth = accounts[0].balance()
    final_tokens = token.balanceOf(accounts[0])
    assert final_eth < initial_eth
    assert final_tokens > initial_tokens


def test_get_pair_info(interface):
    factory = UniswapV2Factory[-1]
    path = [WETH9[-1].address, Token[-1].address]
    pair_contract_address = factory.getPair(path[0], path[1])

    pair_contract = interface.IUniswapV2Pair(pair_contract_address)


def test_receive_fee(interface):
    dev = accounts.add(config["wallets"]["from_key"])
    factory = UniswapV2Factory[-1]
    router = UniswapV2Router02[-1]
    weth = WETH9[-1]
    token = Token[-1]
    path = [WETH9[-1].address, Token[-1].address]
    pair_contract_address = factory.getPair(path[0], path[1])
    pair_contract = interface.IUniswapV2Pair(pair_contract_address)
    amount_to_swap = 10**6
    chain = network.state.Chain()
    current_block = chain.time()
    big_num = 10**18

    print(f'\n\n*****')
    fee_to = factory.feeTo()
    as_int = int(fee_to, 16)
    assert as_int != 0

    # Test1 -- receive nothing when fees very low
    # flush delta kLast
    add_liquidity(tokens_to_add=10, ETH_to_add=10)
    tx = factory.setProtocolFeePercentage(1, {'from': accounts[0]})

    initial_balance_fee_to = pair_contract.balanceOf(accounts[1])
    initial_balance_provider = pair_contract.balanceOf(accounts[0])

    swap_tokens(amount_to_swap)
    add_liquidity(tokens_to_add=10, ETH_to_add=10)

    final_balance_fee_to = pair_contract.balanceOf(accounts[1])
    final_balance_provider = pair_contract.balanceOf(accounts[0])

    # print(f'total fee: {amount_to_swap*3/1000}')
    # weight of lp token : 1 / 2 (because it is one to one)
    # expected_fee = amount_to_swap*(3/1000)*(1/6)*(1/2)
    actual_difference = final_balance_fee_to - initial_balance_fee_to
    print(f'fee received: {actual_difference}, expecting near 0')
    assert actual_difference < 10, f'fee received for protocol: {actual_difference}, whould have been near 0.'


    # Test 2 -- receive everything when fee set to max (10000)
    # flush delta kLast
    # add_liquidity(tokens_to_add=10, ETH_to_add=10)
    tx = factory.setProtocolFeePercentage(10000, {'from': accounts[0]})

    initial_balance_fee_to = pair_contract.balanceOf(accounts[1])
    initial_balance_provider = pair_contract.balanceOf(accounts[0])

    swap_tokens(amount_to_swap)
    add_liquidity(tokens_to_add=10, ETH_to_add=10)

    final_balance_fee_to = pair_contract.balanceOf(accounts[1])
    final_balance_provider = pair_contract.balanceOf(accounts[0])

    # print(f'total fee: {amount_to_swap*3/1000}')
    # weight of lp token : 1 / 2 (because it is one to one)
    expected_fee = amount_to_swap*(3/1000)*(1/2)
    actual_difference = final_balance_fee_to - initial_balance_fee_to
    percent_off_from_calculations = abs(expected_fee - actual_difference) / expected_fee * 100

    print(f'fee received: {actual_difference}, expecting {expected_fee}')
    assert percent_off_from_calculations < 1, f'fee received not accurate'


    assert final_balance_fee_to > initial_balance_fee_to


def test_get_amounts_out():
    dev = accounts.add(config["wallets"]["from_key"])
    router = UniswapV2Router02[-1]
    path = [WETH9[-1].address, Token[-1].address]
    (funds_out, funds_in) = router.getAmountsOut(100000, path)
    print(f'Putting in 100000, will receive: {funds_in}')

def test_fee_receiver():
    dev = accounts.add(config["wallets"]["from_key"])
    router = UniswapV2Router02[-1]
    path = [WETH9[-1].address, Token[-1].address]
    (funds_out, funds_in) = router.getAmountsOut(100000, path)
    print(f'Putting in 100000, will receive: {funds_in}')




def test_change_protocol_fee():
    dev = accounts.add(config["wallets"]["from_key"])
    # factory = Contract.from_explorer(FACTORY_ADDRESS)
    # percentage = factory.protocolFeePercentage()
    # print(f'percentage: {percentage}')
    # assert percentage == 8000
    # factory = Contract.from_explorer(FACTORY_ADDRESS)
    factory = UniswapV2Factory[-1]


    # set fee
    new_percentage = 10000
    tx = factory.setProtocolFeePercentage(new_percentage, {'from': accounts[0]})
    percentage = factory.protocolFeePercentage()

    assert percentage == new_percentage
