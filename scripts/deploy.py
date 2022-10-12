from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import time
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract
    # you can pass stuff into the solidity constructor function
    #   by adding it as a parameter in the deploy function/method
    # if we are on a persistant test network use associated address,
    # if not, use a 'mocks'
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # in the parameters below, the ["verify"] could also be pulled like that, but if you use
    # .get("verify") then this avoids issues if you forget to actually add the verify into the yaml.

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    time.sleep(1)
    print(f"Contract Deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
