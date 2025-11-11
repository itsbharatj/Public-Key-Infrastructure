# Public Key Infrastructure (PKI) Demonstration - India

THIS IS THE BEST PROJECT! KEEP IT UP BHARAT JAIN
This project demonstrates a **complete, RFC 5280-compliant Public Key Infrastructure (PKI)** system as implemented in India, using Python and OpenSSL libraries.

## 🎯 Project Overview

This is a **comprehensive PKI demonstration** that includes:

- ✅ **Certificate Authority (CA)** with proper certificate issuance
- ✅ **Digital Certificates** (Class 2 and Class 3 per Indian standards)
- ✅ **Digital Signatures** with RSA-PSS and SHA-256
- ✅ **Certificate Chain Validation** (RFC 5280 compliant)
- ✅ **Certificate Expiration Checking** (proper PKI validation)
- ✅ **Key Usage Validation** (digitalSignature, keyCertSign)
- ✅ **Client-Server Communication** with full PKI security
- ✅ **Attack Detection** (impersonation, tampering, fake signatures)

**This implementation demonstrates REAL PKI, not just cryptography!**

## ✨ Key Features

### 🔐 Security Features
- **Expiration Validation**: Certificates are checked for validity period
- **Chain Validation**: Full RFC 5280 compliant certificate chain verification
- **Key Usage Enforcement**: Certificates validated for intended purpose
- **Attack Prevention**: 100% detection rate for common attacks
- **Non-Repudiation**: Legal digital signatures per IT Act, 2000

### 📋 Standards Compliance
- **RFC 5280**: X.509 Certificate and CRL Profile
- **IT Act, 2000**: Digital Signatures (India)
- **CCA Guidelines**: Certificate Classes and Standards

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

## 📁 Project Structure

```
Crypto Project/
├── requirements.txt                   # Python dependencies
├── README.md                          # Project overview (this file)
├── CLIENT_SERVER_DOCUMENTATION.md     # Technical documentation
├── PKI_VALIDATION_FIXES.md           # Validation improvements documentation
├── TESTING_RESULTS.md                 # Complete testing results
├── src/
│   ├── __init__.py
│   ├── certificate_authority.py      # CA with proper validation
│   ├── digital_certificate.py        # RFC 5280 chain validation
│   └── digital_signature.py          # Signature with certificate validation
├── main.py                            # Interactive demo
├── examples.py                        # Programmatic examples
├── client_server_example.py          # Client-server with PKI
├── verify_certificate_example.py     # Certificate verification demo
├── pki_validation_demo.py            # Validation improvements demo
└── certificates/                      # Generated certificates (created at runtime)
```

## 🚀 Usage

### 1. Interactive Demo (Recommended for Beginners)
```bash
python main.py
```
Provides an interactive menu to:
- Create Certificate Authority
- Generate certificates
- Sign documents
- Verify signatures
- View certificate chains

### 2. Client-Server Communication Demo (Shows Real-World Usage)
```bash
python client_server_example.py
```
Demonstrates:
- ✅ Legitimate authenticated messages (ACCEPTED)
- ❌ Unauthenticated messages (REJECTED)
- ❌ Impersonation attacks (DETECTED)
- ❌ Fake signatures (DETECTED)
- ❌ Message tampering (DETECTED)

**All with full PKI validation!**

### 3. PKI Validation Demo (Shows Technical Improvements)
```bash
python pki_validation_demo.py
```
Demonstrates:
- Certificate expiration checking
- RFC 5280 chain validation
- Key usage validation
- Before/after comparison

### 4. Certificate Verification Example
```bash
python verify_certificate_example.py
```
Shows:
- How CA verifies certificates
- Valid vs invalid certificates
- Proper PKI validation

### 5. Programmatic Examples
```bash
python examples.py
```
Shows code examples for developers.

## 🔧 Components

### 1. Certificate Authority (CA) - `src/certificate_authority.py`
- Generates self-signed root certificates (4096-bit RSA)
- Issues Class 2 and Class 3 certificates
- **✅ Proper validation**: Checks expiration, signature, constraints, key usage

### 2. Digital Certificates - `src/digital_certificate.py`
- X.509 v3 certificates with extensions
- **✅ RFC 5280 chain validation**: Validates each link cryptographically
- Supports certificate hierarchies (Root → Intermediate → End User)

### 3. Digital Signatures - `src/digital_signature.py`
- RSA-PSS with SHA-256 hashing
- **✅ 4-step verification**: Certificate → Key Usage → Signature → Integrity
- Non-repudiation support (IT Act, 2000 compliant)

## 📚 Documentation

- **[README.md](README.md)** - This file (project overview)
- **[CLIENT_SERVER_DOCUMENTATION.md](CLIENT_SERVER_DOCUMENTATION.md)** - Detailed technical documentation with all scenarios
- **[PKI_VALIDATION_FIXES.md](PKI_VALIDATION_FIXES.md)** - Complete explanation of PKI validation improvements
- **[TESTING_RESULTS.md](TESTING_RESULTS.md)** - Comprehensive testing results and compliance verification

## Legal Framework in India

- **IT Act, 2000**: Provides legal recognition to digital signatures
- **Second Schedule**: Technical standards for security procedures
- **CCA Guidelines**: Certification practice statements

## 📊 Testing Results

✅ **ALL TESTS PASSED**

- **Certificate Expiration Validation:** PASSED
- **Certificate Chain Validation:** PASSED (RFC 5280 compliant)
- **Key Usage Validation:** PASSED
- **Signature Verification:** PASSED (4-step process)
- **Client-Server Communication:** PASSED
- **Attack Detection Rate:** 100%

See [TESTING_RESULTS.md](TESTING_RESULTS.md) for complete details.

## 🛡️ Security Features

### Attack Prevention (100% Detection Rate)

| Attack Type | Detection | Result |
|-------------|-----------|---------|
| Unauthenticated messages | ✅ Detected | ❌ Rejected |
| Impersonation attempts | ✅ Detected | ❌ Rejected |
| Fake signatures | ✅ Detected | ❌ Rejected |
| Message tampering | ✅ Detected | ❌ Rejected |
| Expired certificates | ✅ Detected | ❌ Rejected |

### PKI Validation (RFC 5280 Compliant)

✅ Certificate expiration checking  
✅ Certificate chain validation  
✅ CA authorization validation  
✅ Path length constraints  
✅ Key usage validation  
✅ Signature verification  
✅ Non-repudiation support

## Example Output

### Client-Server Communication
```
[Step 1/4] Validating Signer's Certificate
✓ Certificate is currently valid

[Step 2/4] Checking Certificate Key Usage
✓ Certificate authorized for digital signatures
✓ Non-repudiation enabled (legally binding)

[Step 3/4] Verifying Cryptographic Signature
✓ Signature verification SUCCESSFUL

[Step 4/4] Verifying Document Integrity
✓ Document hash: be49f1468c69e29d...

VERIFICATION RESULT: ✓ VALID
```

### Attack Detection
```
✗ Signature verification FAILED
✗ Message REJECTED - possible tampering detected
```

## Security Notes

⚠️ **This is for educational purposes only!**
- Do not use these certificates in production
- Real PKI implementations require proper security audits
- Private keys should be securely stored (HSM in production)

## References

- [IT Act, 2000](http://www.dot.gov.in/sites/default/files/it_act_2000_0.pdf)
- [Controller of Certifying Authorities](https://cca.gov.in/)
- [RFC 5280 - X.509 Certificate Standard](https://tools.ietf.org/html/rfc5280)
