from scripts.helpful_scripts import get_account, get_weth, approve_erc20, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import ContributorLender, network, config, interface, exceptions
from web3 import Web3
import pytest


def test_can_deposit():
    # only or mainnet-fork
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Admin account
    account = get_account()
    lender_contract = ContributorLender.deploy({"from": account})

    # set lendingPool provider
    pool_provider_address = config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    tx_pool = lender_contract.setPoolProvider(pool_provider_address, {"from": account})
    tx_pool.wait(1)

    # set tokens that can be staked
    tokens_list = ["weth_token", "dai_token"]
    for token in tokens_list:
        token_address = config["networks"][network.show_active()][token]
        tx_stake = lender_contract.setPoolTokens(token_address, {"from": account})
        tx_stake.wait(1)

    # get contributor 1 ready
    weth_token = config["networks"][network.show_active()]["weth_token"]
    contributor_1 = get_account(index=1)
    get_weth(address=weth_token, account=contributor_1)
    CONTRIBUTION = Web3.toWei(0.1, "ether")
    tx_approve = approve_erc20(CONTRIBUTION,
                               lender_contract.address,
                               weth_token,
                               contributor_1)
    tx_contrib = lender_contract.poolDeposit(weth_token,
                                             CONTRIBUTION,
                                             {"from": contributor_1})
    tx_contrib.wait(1)
    aWeth_token = config["networks"][network.show_active()]["aWeth_token"]
    eip20 = interface.EIP20Interface(aWeth_token)
    assert eip20.balanceOf(lender_contract.address) >= Web3.toWei(0.1, "ether")
