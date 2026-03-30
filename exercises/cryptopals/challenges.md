# Cryptopals — full challenge index

**Site:** [cryptopals.com](https://cryptopals.com/) · **Exercises hub:** [../README.md](../README.md)

Source: Cryptography Services / NCC Group. Global numbering runs **1–66** across sets.

---

## How to use this file (practical)

This index doubles as a **study guide**: each set has a short “how to solve” checklist, plus small **demo snippets** and “common gotchas”. It’s intentionally **hint-heavy** but does not paste full final outputs.

### Suggested repo layout (when you start coding)

- `exercises/cryptopals/solutions/`
  - `set1/`, `set2/`, ...
  - `lib/` (shared helpers: xor, padding, block modes, scoring)

### Minimal tooling (Python 3)

- **No deps needed** for Set 1–6 if you implement AES + hashes yourself (Cryptopals often wants you to).
- If you *do* allow a cipher library for early sets while learning, keep it consistent (e.g., `pycryptodome`), but still implement the mode logic yourself when asked.

### Demo helpers (tiny, reusable patterns)

```python
import base64
from itertools import cycle

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def xor_repeat(pt: bytes, key: bytes) -> bytes:
    return bytes(p ^ k for p, k in zip(pt, cycle(key)))

def chunks(b: bytes, n: int):
    for i in range(0, len(b), n):
        yield b[i:i+n]

def hamming(a: bytes, b: bytes) -> int:
    # popcount of XOR
    return sum((x ^ y).bit_count() for x, y in zip(a, b))
```

---

## Set 1 — Basics

| # | Title |
|---|--------|
| 1 | [Convert hex to base64](https://cryptopals.com/sets/1/challenges/1) |
| 2 | [Fixed XOR](https://cryptopals.com/sets/1/challenges/2) |
| 3 | [Single-byte XOR cipher](https://cryptopals.com/sets/1/challenges/3) |
| 4 | [Detect single-character XOR](https://cryptopals.com/sets/1/challenges/4) |
| 5 | [Implement repeating-key XOR](https://cryptopals.com/sets/1/challenges/5) |
| 6 | [Break repeating-key XOR](https://cryptopals.com/sets/1/challenges/6) |
| 7 | [AES in ECB mode](https://cryptopals.com/sets/1/challenges/7) |
| 8 | [Detect AES in ECB mode](https://cryptopals.com/sets/1/challenges/8) |

### Set 1 — how to solve (what to practice)

- **Byte discipline**: treat everything as `bytes`, not text, until the last moment.
- **XOR tooling**: fixed XOR, single-byte XOR, repeating XOR all become one-liners once `xor_bytes` + `xor_repeat` exist.
- **Scoring English**: you need a plaintext “looks like English” score.
- **ECB detection**: repeated 16-byte blocks are the signature.

### Set 1 — demos + hints by challenge

- **1 Convert hex to base64**
  - **Hint**: parse hex → bytes → base64.

```python
raw = bytes.fromhex("48656c6c6f")      # b"Hello"
print(base64.b64encode(raw).decode())
```

- **2 Fixed XOR**
  - **Hint**: decode both hex strings → XOR → re-hex.

- **3 Single-byte XOR cipher**
  - **Hint**: brute-force key `0..255`, score plaintext; return best.
  - **English score**: count common chars (`etaoin`), reward letters/spaces, penalize non-printables.

- **4 Detect single-character XOR**
  - **Hint**: run challenge 3 on each line, keep best global score.

- **5 Implement repeating-key XOR**
  - **Hint**: `xor_repeat(plaintext, key)`; output hex.

- **6 Break repeating-key XOR**
  - **Hint**: guess keysize by **normalized hamming distance** across first few blocks.
  - Then transpose blocks by key byte position; solve each as single-byte XOR (challenge 3).
  - **Gotcha**: normalize by keysize; average across several block pairs to reduce noise.

- **7 AES in ECB mode**
  - **Hint**: ECB decrypt = block-by-block AES decrypt; no chaining.
  - **Gotcha**: input is base64; decode first.

- **8 Detect AES in ECB mode**
  - **Hint**: for each ciphertext, split into 16-byte blocks; count duplicates; max duplicates wins.

---

## Set 2 — Block crypto

| # | Title |
|---|--------|
| 9 | [Implement PKCS#7 padding](https://cryptopals.com/sets/2/challenges/9) |
| 10 | [Implement CBC mode](https://cryptopals.com/sets/2/challenges/10) |
| 11 | [An ECB/CBC detection oracle](https://cryptopals.com/sets/2/challenges/11) |
| 12 | [Byte-at-a-time ECB decryption (Simple)](https://cryptopals.com/sets/2/challenges/12) |
| 13 | [ECB cut-and-paste](https://cryptopals.com/sets/2/challenges/13) |
| 14 | [Byte-at-a-time ECB decryption (Harder)](https://cryptopals.com/sets/2/challenges/14) |
| 15 | [PKCS#7 padding validation](https://cryptopals.com/sets/2/challenges/15) |
| 16 | [CBC bitflipping attacks](https://cryptopals.com/sets/2/challenges/16) |

### Set 2 — how to solve

- Learn **block boundaries**: everything is 16-byte blocks (AES).
- Implement **PKCS#7 pad** and **unpad** early; you will reuse it constantly.
- CBC = XOR with previous ciphertext (or IV) before block decrypt/encrypt.
- ECB “oracles” are solved by carefully crafting inputs that align blocks.

### Set 2 — demos + hints

- **9 PKCS#7 padding**
  - **Hint**: pad value = number of pad bytes; always pad (even if already aligned).

```python
def pkcs7_pad(b: bytes, block: int) -> bytes:
    pad = block - (len(b) % block)
    return b + bytes([pad]) * pad
```

- **10 Implement CBC mode**
  - **Hint**: encryption:
    - `c0 = AES( p0 XOR iv )`
    - `c1 = AES( p1 XOR c0 )` ...
  - decryption:
    - `p0 = AES^-1(c0) XOR iv`
    - `p1 = AES^-1(c1) XOR c0` ...

- **11 ECB/CBC detection oracle**
  - **Hint**: feed repeating plaintext (`b"A"*64`), observe duplicate ciphertext blocks → ECB.

- **12 Byte-at-a-time ECB (simple)**
  - **Hint**: discover block size by increasing input until ciphertext length jumps.
  - Confirm ECB by duplicate blocks.
  - Then recover unknown suffix one byte at a time:
    - choose padding so unknown byte lands at end of a block
    - build dictionary of `pad + known + guess` → first block ciphertext
    - match oracle output block

- **13 ECB cut-and-paste**
  - **Hint**: make `role=admin` occupy its own block; splice blocks from two ciphertexts.

- **14 Byte-at-a-time ECB (harder)**
  - **Hint**: there’s a random-length prefix; you must find alignment:
    - send varying pad until you create two equal adjacent blocks (marker)
    - compute prefix padding needed to align your controlled bytes to a block boundary

- **15 PKCS#7 padding validation**
  - **Hint**: validate that last byte `n` is 1..block and last `n` bytes all equal `n`.
  - **Gotcha**: reject `... 00` and reject `n` larger than buffer.

- **16 CBC bitflipping**
  - **Hint**: in CBC, flipping a bit in `C[i]` flips the same bit in plaintext block `P[i+1]`.
  - So you can forge `;admin=true;` by:
    - submitting a payload with placeholders
    - XOR-diff into prior ciphertext block to force desired bytes after decrypt

---

## Set 3 — Block & stream crypto

| # | Title |
|---|--------|
| 17 | [The CBC padding oracle](https://cryptopals.com/sets/3/challenges/17) |
| 18 | [Implement CTR, the stream cipher mode](https://cryptopals.com/sets/3/challenges/18) |
| 19 | [Break fixed-nonce CTR mode using substitutions](https://cryptopals.com/sets/3/challenges/19) |
| 20 | [Break fixed-nonce CTR statistically](https://cryptopals.com/sets/3/challenges/20) |
| 21 | [Implement the MT19937 Mersenne Twister RNG](https://cryptopals.com/sets/3/challenges/21) |
| 22 | [Crack an MT19937 seed](https://cryptopals.com/sets/3/challenges/22) |
| 23 | [Clone an MT19937 RNG from its output](https://cryptopals.com/sets/3/challenges/23) |
| 24 | [Create the MT19937 stream cipher and break it](https://cryptopals.com/sets/3/challenges/24) |

### Set 3 — how to solve

- CTR mode turns a block cipher into a **stream cipher**: keystream XOR plaintext.
- Padding oracle: use a boolean oracle to recover bytes (careful bookkeeping).
- MT19937: implement exactly; then reverse the tempering function to clone state.

### Set 3 — hints

- **17 CBC padding oracle**
  - **Hint**: classic 16-byte backward byte recovery:
    - target last byte first (force pad `0x01`)
    - adjust bytes you’ve solved to maintain pad length
    - handle the “accidental valid padding” edge case (try a second confirm query)

- **18 Implement CTR**
  - **Hint**: keystream block = `AES(key, nonce || counter)`; XOR with plaintext.
  - **Gotcha**: nonce/counter endianness matters; follow challenge text.

- **19/20 Break fixed-nonce CTR**
  - **Hint**: same keystream reused across many ciphertexts → multi-time pad.
  - Approach A (19): do substitutions/crib-dragging manually with scoring.
  - Approach B (20): treat it like repeating-key XOR across columns; score each keystream byte.

- **21–24 MT19937**
  - **Hint**: write `mt19937.py` with `extract_number()` and `twist()`.
  - **23 Clone RNG**: invert tempering (unshift/xor & masks).
  - **24 Stream cipher**: XOR MT outputs; recover seed via known plaintext suffix (common trick: known `A...A` tail).

---

## Set 4 — Stream crypto and randomness

| # | Title |
|---|--------|
| 25 | [Break "random access read/write" AES CTR](https://cryptopals.com/sets/4/challenges/25) |
| 26 | [CTR bitflipping](https://cryptopals.com/sets/4/challenges/26) |
| 27 | [Recover the key from CBC with IV=Key](https://cryptopals.com/sets/4/challenges/27) |
| 28 | [Implement a SHA-1 keyed MAC](https://cryptopals.com/sets/4/challenges/28) |
| 29 | [Break a SHA-1 keyed MAC using length extension](https://cryptopals.com/sets/4/challenges/29) |
| 30 | [Break an MD4 keyed MAC using length extension](https://cryptopals.com/sets/4/challenges/30) |
| 31 | [Implement and break HMAC-SHA1 with an artificial timing leak](https://cryptopals.com/sets/4/challenges/31) |
| 32 | [Break HMAC-SHA1 with a slightly less artificial timing leak](https://cryptopals.com/sets/4/challenges/32) |

### Set 4 — how to solve

- CTR “edit” = malleability; if you can edit ciphertext, you can recover plaintext.
- MACs: implement SHA-1/MD4 **from scratch** if the set expects it.
- Length extension: internal hash state + message length are enough to append data.
- Timing leak: build a robust measurement loop (median of multiple samples).

### Set 4 — hints

- **25 Break random-access CTR**
  - **Hint**: with an edit oracle, recover keystream:
    - ask oracle to “edit” ciphertext with all-zero plaintext at offset 0
    - output is keystream; XOR with ciphertext to get plaintext

- **26 CTR bitflipping**
  - **Hint**: CTR is XOR; flip bytes in ciphertext to force bytes in plaintext at same positions.

- **27 Recover key from CBC with IV=Key**
  - **Hint**: craft ciphertext blocks so plaintext reveals key when error leaks raw plaintext (per challenge design).

- **28–30 SHA-1/MD4 keyed MAC + length extension**
  - **Hint**: implement hash that can start from a provided internal state and message length.
  - Guess key length (reasonable range), compute glue padding for `key||msg`, forge `msg||pad||suffix`, recompute MAC.

- **31/32 Timing leak**
  - **Hint**: attack one byte at a time; for each candidate byte, take many measurements; keep the slowest.
  - **Gotcha**: network jitter dominates; use retries/backoff; compare relative deltas, not absolute times.

---

## Set 5 — Diffie-Hellman and friends

| # | Title |
|---|--------|
| 33 | [Implement Diffie-Hellman](https://cryptopals.com/sets/5/challenges/33) |
| 34 | [Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection](https://cryptopals.com/sets/5/challenges/34) |
| 35 | [Implement DH with negotiated groups, and break with malicious "g" parameters](https://cryptopals.com/sets/5/challenges/35) |
| 36 | [Implement Secure Remote Password (SRP)](https://cryptopals.com/sets/5/challenges/36) |
| 37 | [Break SRP with a zero key](https://cryptopals.com/sets/5/challenges/37) |
| 38 | [Offline dictionary attack on simplified SRP](https://cryptopals.com/sets/5/challenges/38) |
| 39 | [Implement RSA](https://cryptopals.com/sets/5/challenges/39) |
| 40 | [Implement an E=3 RSA Broadcast attack](https://cryptopals.com/sets/5/challenges/40) |

### Set 5 — how to solve

- You’ll write small “toy protocols” (DH, SRP) plus MITM adversaries.
- Get comfortable with modular arithmetic and big integers.

### Set 5 — hints

- **33 Implement Diffie-Hellman**
  - **Hint**: `A = g^a mod p`, `B = g^b mod p`, shared = `B^a mod p = A^b mod p`.

- **34–35 DH MITM / malicious g**
  - **Hint**: by swapping parameters, force shared secret into a small set (often 0, 1, or p-1).

- **36–38 SRP**
  - **Hint**: implement exactly; log intermediate values; test with fixed vectors you create.
  - **37 zero key**: choose `A` so shared secret becomes 0.
  - **38 offline dictionary**: reduce SRP so attacker can test guesses locally by recomputing HMAC.

- **39 RSA**
  - **Hint**: keygen:
    - choose primes p,q
    - `n = p*q`, `phi=(p-1)(q-1)`
    - choose e (e.g. 65537), compute d = inv(e, phi)

- **40 e=3 broadcast**
  - **Hint**: same message encrypted to 3 recipients with e=3 → use CRT to get `m^3`, take integer cube root.

---

## Set 6 — RSA and DSA

| # | Title |
|---|--------|
| 41 | [Implement unpadded message recovery oracle](https://cryptopals.com/sets/6/challenges/41) |
| 42 | [Bleichenbacher's e=3 RSA Attack](https://cryptopals.com/sets/6/challenges/42) |
| 43 | [DSA key recovery from nonce](https://cryptopals.com/sets/6/challenges/43) |
| 44 | [DSA nonce recovery from repeated nonce](https://cryptopals.com/sets/6/challenges/44) |
| 45 | [DSA parameter tampering](https://cryptopals.com/sets/6/challenges/45) |
| 46 | [RSA parity oracle](https://cryptopals.com/sets/6/challenges/46) |
| 47 | [Bleichenbacher's PKCS 1.5 Padding Oracle (Simple Case)](https://cryptopals.com/sets/6/challenges/47) |
| 48 | [Bleichenbacher's PKCS 1.5 Padding Oracle (Complete Case)](https://cryptopals.com/sets/6/challenges/48) |

### Set 6 — hints

- **41 unpadded message recovery oracle**
  - **Hint**: RSA is multiplicative: `E(m)*E(s) = E(m*s)`; oracle that tells you “valid” can be used to scale and recover.

- **42 Bleichenbacher e=3 RSA attack**
  - **Hint**: cube root works when padding is weak and message small enough; careful with bounds.

- **43–45 DSA nonce attacks**
  - **Hint**: if nonce `k` leaks or repeats, you can solve for private key x.

- **46 RSA parity oracle**
  - **Hint**: multiply ciphertext by `2^e mod n` each step; parity of decrypted plaintext gives a bit of info; do interval halving.

- **47/48 PKCS#1.5 padding oracle**
  - **Hint**: classic Bleichenbacher: maintain interval for plaintext `m`, search for s values that make padding valid, narrow interval.

---

## Set 7 — Hashes

| # | Title |
|---|--------|
| 49 | [CBC-MAC Message Forgery](https://cryptopals.com/sets/7/challenges/49) |
| 50 | [Hashing with CBC-MAC](https://cryptopals.com/sets/7/challenges/50) |
| 51 | [Compression Ratio Side-Channel Attacks](https://cryptopals.com/sets/7/challenges/51) |
| 52 | [Iterated Hash Function Multicollisions](https://cryptopals.com/sets/7/challenges/52) |
| 53 | [Kelsey and Schneier's Expandable Messages](https://cryptopals.com/sets/7/challenges/53) |
| 54 | [Kelsey and Kohno's Nostradamus Attack](https://cryptopals.com/sets/7/challenges/54) |
| 55 | [MD4 Collisions](https://cryptopals.com/sets/7/challenges/55) |
| 56 | [RC4 Single-Byte Biases](https://cryptopals.com/sets/7/challenges/56) |

### Set 7 — hints

- CBC-MAC forgery relies on the chaining XOR and controllable IV/length rules.
- Compression ratio side-channel: adaptively guess bytes and observe compressed size change.
- Multicollisions / Nostradamus: build trees of collisions and stitch them.
- MD4 collisions: heavy; follow the structure (this is where many people slow down).
- RC4 biases: collect lots of samples; statistical key recovery.

---

## Set 8 — Abstract algebra

| # | Title |
|---|--------|
| 57 | [Diffie-Hellman Revisited: Small Subgroup Confinement](https://cryptopals.com/sets/8/challenges/57) |
| 58 | [Pollard's Method for Catching Kangaroos](https://cryptopals.com/sets/8/challenges/58) |
| 59 | [Elliptic Curve Diffie-Hellman and Invalid-Curve Attacks](https://cryptopals.com/sets/8/challenges/59) |
| 60 | [Single-Coordinate Ladders and Insecure Twists](https://cryptopals.com/sets/8/challenges/60) |
| 61 | [Duplicate-Signature Key Selection in ECDSA (and RSA)](https://cryptopals.com/sets/8/challenges/61) |
| 62 | [Key-Recovery Attacks on ECDSA with Biased Nonces](https://cryptopals.com/sets/8/challenges/62) |
| 63 | [Key-Recovery Attacks on GCM with Repeated Nonces](https://cryptopals.com/sets/8/challenges/63) |
| 64 | [Key-Recovery Attacks on GCM with a Truncated MAC](https://cryptopals.com/sets/8/challenges/64) |
| 65 | [Truncated-MAC GCM Revisited: Improving the Key-Recovery Attack via Ciphertext Length Extension](https://cryptopals.com/sets/8/challenges/65) |
| 66 | [Exploiting Implementation Errors in Diffie-Hellman](https://cryptopals.com/sets/8/challenges/66) |

### Set 8 — hints

These are “math + engineering” problems. Keep code clean:

- Build small finite-field helpers (add/mul/inv), then reuse them across DH/GCM/ECC.
- Validate every step with tiny hand-checkable examples.
- Expect a lot of debugging time; write assertions.

**Total: 66 challenges** (8 + 8 + 8 + 8 + 8 + 8 + 8 + 10).

If a Set 8 URL 404s in the browser, try the same path with or without a `.txt` suffix — the site index sometimes links plaintext copies.
