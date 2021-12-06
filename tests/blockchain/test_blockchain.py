from re import match
from backend.wallet.transactions import Transaction
from backend.wallet.wallet import Wallet
import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA, Block



def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test_data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data


@pytest.fixture
def blockchain():
    blockchain = Blockchain()

    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain


def test_is_valid_chain(blockchain):
    Blockchain.is_valid_chain(blockchain.chain)


def test_is_valid_chain_bad_genesis(blockchain):
    blockchain.chain[0].hash = 'evil_hash'

    with pytest.raises(Exception, match='genesis block must be valid'):
        Blockchain.is_valid_chain(blockchain.chain)


def test_replace_chain(blockchain):
    blockchain_old = Blockchain()
    blockchain_old.replace_chain(blockchain.chain)

    assert blockchain_old.chain == blockchain.chain

def test_replace_chain_not_longer(blockchain):
    blockchain_old = Blockchain()

    with pytest.raises(Exception, match='The incoming chain must be longer'):
        blockchain.replace_chain(blockchain_old.chain)

def test_replace_chain_bad_chain(blockchain):
    blockchain_old = Blockchain()
    blockchain.chain[1].hash = 'evil_hash'

    with pytest.raises(Exception, match = "the incoming chain is invalid"):
        blockchain_old.replace_chain(blockchain.chain)


def test_valid_transaction_chain(blockchain):
    Blockchain.is_valid_transaction_chain(blockchain.chain)

def test_is_valid_transaction_chain_duplicate_transactions(blockchain):
    transaction = Transaction(Wallet(), 'recipient', 1).to_json()

    blockchain.add_block([transaction, transaction])

    with pytest.raises(Exception, match='is not unique'):
        Blockchain.is_valid_transaction_chain(blockchain.chain)

def test_is_valid_transaction_chain_multiple_transactions(blockchain):
    reward_1 = Transaction.reward_transaction(Wallet()).to_json()
    reward_2 = Transaction.reward_transaction(Wallet()).to_json()

    blockchain.add_block([reward_1, reward_2])

    with pytest.raises(Exception, match='one mining reward per Block'):
        Blockchain.is_valid_transaction_chain(blockchain.chain)


def test_is_valid_transaction_chain_bad_historic_balance(blockchain):
    wallet = Wallet()
    bad_transaction = Transaction(wallet, 'recipient', 1)
    bad_transaction.output[wallet.address] = 9000
    bad_transaction.input['amount'] = 9001
    bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

    blockchain.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception, match= 'has an invalid input amount'):
        Blockchain.is_valid_transaction_chain(blockchain.chain)