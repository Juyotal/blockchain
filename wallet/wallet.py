import json
import uuid
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from backend.config import STARTING_BALANCE

class Wallet:
    """
    An individal wallet for a miner.
    Keeps track of a miner's balance.
    Allows a miner to authorize a transaction.
    """

    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(), 
            default_backend
        )
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()

    def sign(self, data):
        """
        Generate a signature based on the data using a local private key
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())
        ))


    def serialize_public_key(self):
        """
        Reset the public key to its serialized version
        """
        self.public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.public_key = self.public_key_bytes.decode('utf-8')

   


    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original public key and data
        """

        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        (r, s) = signature

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r,s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
        )
            return True

        except InvalidSignature:
            return False

def main():
    wallet = Wallet()
    print (f'wallet: {wallet.__dict__}')

    data = { 'foo': 'bar' }
    signature = wallet.sign(data)
    print(signature)

if __name__ == "__main__":
    main()