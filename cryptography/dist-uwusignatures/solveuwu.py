from pwn import process
from Crypto.Util.number import *
import hashlib
import json
from math import gcd
import random

def hash_m(m):
    sha = hashlib.sha256()
    sha.update(long_to_bytes(m))
    return bytes_to_long(sha.digest())

def safe_recvuntil(io, delim, timeout=5):
    try:
        return io.recvuntil(delim, timeout=timeout)
    except EOFError:
        print(f"EOFError while waiting for {delim.decode()}")
        print("Remaining output:\n" + io.recvall(timeout=2).decode())
        exit()

def get_signature(io, m):
    safe_recvuntil(io, b"> ")
    io.sendline(b"2")
    safe_recvuntil(io, b"Send me a message:")
    io.sendline(json.dumps({"m": m}).encode())
    out = safe_recvuntil(io, b"\n").decode()
    print(f"Signature response: {out.strip()}")
    s = int(out.strip().split()[-1])
    return s

# Start local challenge
io = process(["python3", "uwusignatures.py"])

# Skip welcome line
print(safe_recvuntil(io, b"\n").decode().strip())

# Read lines until one contains 3 integers (p, g, y)
while True:
    line = safe_recvuntil(io, b"\n").decode().strip()
    print(f"Read line: '{line}'")
    parts = line.split()
    if len(parts) == 3:
        try:
            p, g, y = map(int, parts)
            print("[✓] Parsed p, g, y successfully.")
            break
        except ValueError:
            continue

# Read k
line2 = safe_recvuntil(io, b"\n").decode().strip()
print(f"k line: {line2}")
k_printed = int(line2.split(":")[1].strip())

# Compute r = g^k mod p
r = pow(g, k_printed, p)

# === Try up to 10 times to get invertible signature pair ===
for attempt in range(10):
    print(f"\nAttempt {attempt+1} to get valid signature pair")

    m1 = random.randint(2, p - 2)
    m2 = random.randint(2, p - 2)
    if m1 == m2:
        continue

    s1 = get_signature(io, m1)
    s2 = get_signature(io, m2)

    if s1 == s2:
        print("Signatures are equal, skipping")
        continue

    h1 = hash_m(m1)
    h2 = hash_m(m2)

    diff = (s1 - s2) % (p - 1)
    if gcd(diff, p - 1) == 1:
        sign = 1
    else:
        diff = (s2 - s1) % (p - 1)
        if gcd(diff, p - 1) != 1:
            print("Diff not invertible, retrying...\n")
            continue
        sign = -1

    print("[✓] Found suitable pair!")
    k_recovered = (sign * (h1 - h2) * inverse(diff, p - 1)) % (p - 1)
    x = ((h1 - s1 * k_recovered) * inverse(r, p - 1)) % (p - 1)
    break
else:
    print("❌ Failed to find usable signature pair after 10 attempts.")
    exit()

# === Forge signature on forbidden message ===
target_msg = b"gib flag pls uwu"
m = bytes_to_long(target_msg)
h = hash_m(m)

s_target = ((h - x * r) * inverse(k_recovered, p - 1)) % (p - 1)

# === Submit forged signature ===
safe_recvuntil(io, b"> ")
io.sendline(b"1")
safe_recvuntil(io, b"Send me a message and a signature:")

payload = {
    "m": m,
    "r": r,
    "s": s_target
}
io.sendline(json.dumps(payload).encode())

# === Print final output ===
try:
    final_output = io.recvall(timeout=5).decode()
    print("\n🎉 Final output:")
    print(final_output)
except EOFError:
    print("EOF reached before reading final output.")
