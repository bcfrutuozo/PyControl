from base64 import b64encode
from hashlib import sha1
from crypto.Hash import SHA1
from crypto.Signature import PKCS1_v1_5
from crypto.PublicKey import RSA
from nfse.functions import stringEncode


class RSA:

    @classmethod
    def sign(cls, text, private_key_content):
        digest = SHA1.new(stringEncode(text))
        rsa_key = RSA.importKey(private_key_content)
        signer = PKCS1_v1_5.new(rsa_key)
        signature = signer.sign(digest)
        return b64encode(signature)

    @classmethod
    def digest(cls, text):
        hasher = sha1()
        hasher.update(stringEncode(text))
        digest = hasher.digest()
        return b64encode(digest)
