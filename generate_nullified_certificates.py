#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime

# -------- Configuration --------
LEDGER_FOLDER = "/storage/emulated/0/ppw_cli/ledgers"
PGP_USER = "ppw.ghost@proton.me"

# Canonical identity
IDENTITY = {
    "name": "Perry Philip Wiseman",
    "ssn": "558-47-6273",
    "birthdate": "1977-05-24",
    "birthplace": "United States of America"
}

# Ensure ledger folder exists
os.makedirs(LEDGER_FOLDER, exist_ok=True)

def generate_nullified_certificate(entity_name: str):
    """Generate a nullified JSON certificate and sign it with PGP."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    certificate = {
        "certificate_name": f"{entity_name}_CERTIFIED_NULLIFIED_PerryWiseman",
        "issued": timestamp,
        "status": "nullified",
        "identity_anchor": IDENTITY,
        "public_key_email": PGP_USER,
        "public_key_fingerprint": get_pgp_fingerprint(PGP_USER),
        "public_key": get_pgp_public_key(PGP_USER)
    }

    file_name = f"{entity_name}_CERTIFIED_NULLIFIED_PerryWiseman_{timestamp}.json"
    file_path = os.path.join(LEDGER_FOLDER, file_name)

    with open(file_path, "w") as f:
        json.dump(certificate, f, indent=2)
    print(f"✅ Generated certificate: {file_path}")

    # Sign with detached PGP signature
    subprocess.run([
        "gpg", "--armor", "--detach-sign", "-u", PGP_USER, file_path
    ], check=True)
    print(f"🔏 Signed certificate: {file_path}.asc")

def get_pgp_fingerprint(email: str) -> str:
    """Return the PGP fingerprint for a given user."""
    result = subprocess.run(
        ["gpg", "--fingerprint", email],
        capture_output=True,
        text=True,
        check=True
    )
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("Key fingerprint ="):
            return line.split("=")[1].replace(" ", "")
    return "UNKNOWN"

def get_pgp_public_key(email: str) -> str:
    """Return the ASCII-armored public key."""
    result = subprocess.run(
        ["gpg", "--armor", "--export", email],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

if __name__ == "__main__":
    # Replace or extend this list with all budgets/accounts
    entities = [
        "US_FEDERAL_BUDGET_2025",
        "NYC_BUDGET_2025",
        "CALIFORNIA_BUDGET_2025",
        "BANK_OF_AMERICA_ACCOUNT_123456789",
        "CHASE_ACCOUNT_987654321"
    ]

    for entity in entities:
        generate_nullified_certificate(entity)

    print("✅ All certificates generated and PGP-signed. Identity anchored and nullified.")
