# Public Key Infrastructure (PKI) Demonstration - India

This project demonstrates the core concepts of Public Key Infrastructure (PKI) as implemented in India, using Python and OpenSSL libraries.

## Overview

Public Key Infrastructure (PKI) in India is managed by the Controller of Certifying Authorities (CCA) under the IT Act, 2000. This project simulates key PKI operations:

1. **Certificate Authority (CA)**: Root CA and intermediate CA operations
2. **Digital Certificates**: X.509 certificate generation and validation
3. **Key Pair Generation**: RSA public-private key pairs
4. **Digital Signatures**: Document signing and verification
5. **Certificate Chain Verification**: Trust chain validation

## India's PKI Framework

India's PKI infrastructure includes:
- **CCA (Controller of Certifying Authorities)**: Regulatory authority
- **Licensed CAs**: Organizations authorized to issue digital certificates
- **Digital Signature Certificates (DSC)**: Used for e-governance, e-filing, etc.
- **Classes of Certificates**:
  - Class 1: Email security
  - Class 2: Business transactions (e-filing, MCA)
  - Class 3: E-commerce, e-tendering (highest assurance)

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
Crypto Project/
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── src/
│   ├── __init__.py
│   ├── certificate_authority.py    # CA implementation
│   ├── digital_certificate.py      # Certificate generation
│   └── digital_signature.py        # Signature operations
├── main.py                   # Main demonstration script
└── certificates/             # Generated certificates directory
```

## Usage

Run the main demonstration:

```bash
python main.py
```

This will:
1. Create a Root Certificate Authority (CA)
2. Generate RSA key pairs
3. Issue digital certificates
4. Sign documents with digital signatures
5. Verify signatures and certificates
6. Display the complete certificate chain

## Components

### 1. Certificate Authority (CA)
- Generates self-signed root certificates
- Issues and signs subordinate certificates
- Manages certificate lifecycle

### 2. Digital Certificates
- X.509 v3 certificates
- Contains public key, identity information, and CA signature
- Supports different certificate classes

### 3. Digital Signatures
- RSA-based signatures
- SHA-256 hashing
- Document integrity and authentication

## Legal Framework in India

- **IT Act, 2000**: Provides legal recognition to digital signatures
- **Second Schedule**: Technical standards for security procedures
- **CCA Guidelines**: Certification practice statements

## Example Output

The demonstration will show:
- Root CA certificate creation
- User certificate generation
- Document signing process
- Signature verification
- Certificate chain validation

## Security Notes

⚠️ **This is for educational purposes only!**
- Do not use these certificates in production
- Real PKI implementations require proper security audits
- Private keys should be securely stored (HSM in production)

## References

- [IT Act, 2000](http://www.dot.gov.in/sites/default/files/it_act_2000_0.pdf)
- [Controller of Certifying Authorities](https://cca.gov.in/)
- [RFC 5280 - X.509 Certificate Standard](https://tools.ietf.org/html/rfc5280)
