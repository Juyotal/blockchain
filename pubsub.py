from typing import List
import time
from backend.tests.blockchain.test_blockchain import blockchain
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-d9e30d10-51db-11ec-9668-6eac75df5fc1'
pnconfig.publish_key = 'pub-c-8295b3cf-d235-4ddd-a2f8-b7816095df6b'



CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, messaage_object):
        print(f'\n-- Channel: {messaage_object.channel} | Message: {messaage_object.message}')

        if messaage_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(messaage_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n -- Succesfully replaced the local chain')
            except Exception as e:
                print(f"\n -- Did not replace chain: {e}")


class PubSub():
    """
    Handles the public subscribe layer of hee application.
    Provides communication between the nodes of the blockchain network
    """

    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())



def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})

if __name__ == '__main__':
    main()

