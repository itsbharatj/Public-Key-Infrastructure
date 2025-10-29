# Quick Start Guide - PKI Demonstration for India

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Demonstration

**Run the main demonstration:**
```bash
python main.py
```

This interactive demonstration will guide you through:
- Creating a Root Certificate Authority (CA)
- Issuing Class 3 Digital Certificates
- Creating Digital Signatures
- Verifying Signatures and Certificates
- Certificate Chain Validation
- Timestamping

## What Gets Generated

After running the demonstration, you'll find these files in the `certificates/` directory:

- `root_ca.pem` - Root CA certificate
- `root_ca_key.pem` - Root CA private key (keep secure!)
- `user_certificate.pem` - User's digital certificate (Class 3)
- `user_private_key.pem` - User's private key (keep secure!)
- `tender_submission.txt` - Sample signed document
- `tender_submission.sig` - Digital signature file

## Key Concepts Demonstrated

### 1. Certificate Authority (CA)
The CA is the trusted entity that issues digital certificates. In India, CAs must be licensed by the Controller of Certifying Authorities (CCA).

### 2. Digital Certificates
X.509 certificates that bind a public key to an identity. India uses three classes:
- **Class 1**: Email security
- **Class 2**: Business transactions (e-filing, MCA)
- **Class 3**: E-commerce, e-tendering (highest assurance)

### 3. Digital Signatures
RSA-based signatures that provide:
- **Authentication**: Proves signer identity
- **Integrity**: Detects any tampering
- **Non-repudiation**: Signer cannot deny signing

## Legal Framework

Digital signatures in India are governed by:
- **IT Act, 2000** - Legal recognition framework
- **Section 3A** - Digital signatures = Handwritten signatures
- **Section 5** - Electronic records admissible as evidence
- **CCA** - Regulatory authority under Ministry of Electronics and IT

## Security Warning

⚠️ **This project is for educational purposes only!**

- Do NOT use these certificates in production
- Real PKI requires Hardware Security Modules (HSM)
- Get certificates from CCA-licensed CAs for legal use
- Keep private keys secure and never share them

## Common Use Cases in India

1. **Income Tax E-filing** - Class 2 certificate
2. **MCA (Ministry of Corporate Affairs) Filing** - Class 2/3
3. **GST Registration & Returns** - Class 2
4. **E-Tendering/E-Procurement** - Class 3
5. **Import/Export (DGFT)** - Class 2/3
6. **Patent/Trademark Filing** - Class 2

## Resources

- CCA India: https://cca.gov.in/
- IT Act, 2000: http://www.dot.gov.in/
- Licensed CAs: Check CCA repository
