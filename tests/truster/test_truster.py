from brownie import TrusterLenderPool, DamnValuableToken, Attacker, Wei, accounts, reverts


# deploy the contracts / set up
# come up with the exploit
# test your exploit

# Pool has 1M * 10**18 tokens
TOKENS_IN_POOL = Wei("1000000 ether")
INITIAL_ATTACKER_TOKEN_BALANCE = Wei("0 ether")


def setup_contracts():
    deployer = accounts[0]
    attacker = accounts[1]

    #deploying contracts 🚀
    token = DamnValuableToken.deploy({"from": deployer})
    pool = TrusterLenderPool.deploy(token, {"from": deployer})

    #configuring the contracts 🧑‍💻
    token.approve(pool, TOKENS_IN_POOL, {"from": deployer})
    token.transfer(pool, TOKENS_IN_POOL, {"from": deployer})

    
    #ensure that the correct balances have been transfered

    assert token.balanceOf(pool) == TOKENS_IN_POOL
    assert token.balanceOf(attacker) == INITIAL_ATTACKER_TOKEN_BALANCE

    return deployer, attacker, token, pool
    


def test_attacking_the_contract():
    
    deployer, attacker, token, pool  = setup_contracts()

    # CODE YOUR EXPLOIT HERE 😈
    attacker_contract = Attacker.deploy({"from": attacker})

    attacker_contract.attack(pool, token)
    # SUCCESS CONDITIONS 🕺
    # All of the tokens have been withdrawn from the pool
    assert token.balanceOf(attacker) == TOKENS_IN_POOL    
    assert token.balanceOf(pool) == INITIAL_ATTACKER_TOKEN_BALANCE
    
