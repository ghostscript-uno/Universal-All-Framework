# Example: using Python
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import base64, json

with open("universal_ownership_cross_anchored_55847627305241977_2025-09-20T00-00-00Z.json") as f:
    data = json.load(f)

vk = VerifyKey(bytes.fromhex(data["signer_pk"]))
msg = json.dumps({k:v for k,v in data.items() if k!="root_signature"}, sort_keys=True).encode()

try:
    vk.verify(msg, bytes.fromhex(data["root_signature"]))
    print("Signature verified ✅")
except BadSignatureError:
    print("Signature invalid ❌")
