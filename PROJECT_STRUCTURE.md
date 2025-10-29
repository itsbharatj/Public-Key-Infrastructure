# Project Structure

```
Crypto Project/
│
├── README.md                      # Comprehensive project documentation
├── QUICKSTART.md                  # Quick start guide
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
├── main.py                        # Main demonstration script (interactive)
├── examples.py                    # Programmatic usage examples
│
├── src/                           # Source code modules
│   ├── __init__.py
│   ├── certificate_authority.py  # CA implementation
│   ├── digital_certificate.py    # Certificate operations
│   └── digital_signature.py      # Signature operations
│
└── certificates/                  # Generated certificates (not in git)
    ├── .gitkeep
    ├── root_ca.pem               # Root CA certificate
    ├── root_ca_key.pem           # Root CA private key
    ├── user_certificate.pem      # User digital certificate
    ├── user_private_key.pem      # User private key
    ├── tender_submission.txt     # Sample signed document
    └── tender_submission.sig     # Digital signature
```

## Module Overview

### 1. `certificate_authority.py`
- **Class: `CertificateAuthority`**
  - Generate self-signed root certificates
  - Issue and sign subordinate certificates
  - Verify certificate signatures
  - Save certificates and keys to files

### 2. `digital_certificate.py`
- **Class: `DigitalCertificate`**
  - Display certificate information
  - Load certificates from files
  - Calculate certificate fingerprints
  - Export public keys
  - Describe certificate classes (India-specific)

- **Class: `CertificateChain`**
  - Manage certificate chains
  - Display chain hierarchy
  - Validate trust chains

### 3. `digital_signature.py`
- **Class: `DigitalSignature`**
  - Generate RSA key pairs
  - Sign documents with private keys
  - Verify signatures with public keys
  - Save/load signatures
  - Demonstrate hash functions

- **Class: `TimestampAuthority`**
  - Create trusted timestamps
  - Timestamp documents for legal compliance

## Key Features

✅ **Complete PKI Implementation**
- Root CA creation
- Certificate issuance and signing
- Certificate chain validation

✅ **Digital Signatures**
- RSA-PSS with SHA-256
- Document signing and verification
- Non-repudiation support

✅ **India-Specific**
- Three certificate classes (1, 2, 3)
- IT Act, 2000 compliance
- CCA framework alignment

✅ **Security Best Practices**
- 2048/4096-bit RSA keys
- SHA-256 hashing
- PSS padding for signatures
- Secure key storage

## Running the Project

### Interactive Demo
```bash
python main.py
```
Runs through all PKI operations step-by-step with explanations.

### Programmatic Examples
```bash
python examples.py
```
Shows how to use the modules in your own code.

## Technologies Used

- **Python 3.13+**
- **cryptography** - Modern cryptographic library
- **pyOpenSSL** - Python wrapper for OpenSSL
- **X.509 v3** - Certificate standard
- **RSA** - Public key cryptography
- **SHA-256** - Cryptographic hash function

## Educational Value

This project demonstrates:
1. **Public Key Cryptography** - Asymmetric encryption
2. **Digital Certificates** - X.509 standard
3. **Certificate Authorities** - Trust infrastructure
4. **Digital Signatures** - Authentication and integrity
5. **Hash Functions** - One-way cryptographic functions
6. **PKI in India** - Real-world regulatory framework
