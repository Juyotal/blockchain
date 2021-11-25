import hashlib
import json



def crypto_hash(*args):
    """
    Return a sha-256 hash of a given arguments
    """


    string_args = sorted(map(lambda data: json.dumps(data), args))

    joined_data = ''.join(string_args)
    
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash(): {crypto_hash(2,'one', 'two', 'three')}")

if __name__ == '__main__':
    main()