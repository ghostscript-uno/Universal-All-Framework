#!/usr/bin/env python3
import json
import hashlib

with open("universal_authority_certificate_cross_anchored_55847627305241977_2025-09-20T03-04-00Z.json") as f:
    data = json.load(f)

data_for_hash = data.copy()
data_for_hash.pop("merkle_root", None)

computed_hash = hashlib.sha3_512(json.dumps(data_for_hash, sort_keys=True).encode()).hexdigest()

print("Computed SHA3-512 hash:", computed_hash)
print("Stored Merkle root:", data["merkle_root"])

if computed_hash == data["merkle_root"]:
    print("✅ UAC integrity verified")
else:
    print("❌ UAC hash mismatch — file may be altered")
