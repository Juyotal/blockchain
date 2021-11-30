from re import match
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
        blockchain.add_block(i)
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