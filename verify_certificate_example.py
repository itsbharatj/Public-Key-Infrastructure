#!/usr/bin/env python3
"""
Certificate Verification Example

This example demonstrates how to verify if a certificate was signed by a CA.
It shows both valid and invalid certificate scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from certificate_authority import CertificateAuthority
from digital_certificate import DigitalCertificate
from digital_signature import DigitalSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def verify_certificate_manually(ca_certificate, user_certificate):
    """
    Manually verify if a certificate was signed by a CA
    
    Args:
        ca_certificate: The CA's certificate
        user_certificate: The certificate to verify
        
    Returns:
        bool: True if certificate is valid and signed by CA
    """
    print(f"\n{'='*70}")
    print("Manual Certificate Verification Process")
    print(f"{'='*70}\n")
    
    try:
        # Step 1: Check issuer matches CA subject
        print("[Step 1] Checking if issuer matches CA...")
        issuer_match = user_certificate.issuer == ca_certificate.subject
        
        if issuer_match:
            print("✓ Issuer matches CA subject")
            print(f"  CA Subject: {ca_certificate.subject.rfc4514_string()}")
            print(f"  Cert Issuer: {user_certificate.issuer.rfc4514_string()}")
        else:
            print("✗ Issuer does NOT match CA subject")
            return False
        
        # Step 2: Verify the signature
        print("\n[Step 2] Verifying cryptographic signature...")
        print(f"  Signature algorithm: {user_certificate.signature_algorithm_oid._name}")
        print(f"  Signature size: {len(user_certificate.signature)} bytes")
        
        # Get CA's public key
        ca_public_key = ca_certificate.public_key()
        
        # Verify signature on certificate
        ca_public_key.verify(
            user_certificate.signature,
            user_certificate.tbs_certificate_bytes,
            padding.PKCS1v15(),
            user_certificate.signature_hash_algorithm
        )
        
        print("✓ Signature verification SUCCESSFUL")
        print("  - Certificate was definitely signed by this CA")
        print("  - Certificate has not been tampered with")
        
        # Step 3: Check validity period
        print("\n[Step 3] Checking certificate validity period...")
        from datetime import datetime
        now = datetime.utcnow()
        
        if user_certificate.not_valid_before <= now <= user_certificate.not_valid_after:
            print("✓ Certificate is currently valid")
            print(f"  Valid from: {user_certificate.not_valid_before}")
            print(f"  Valid until: {user_certificate.not_valid_after}")
        else:
            print("⚠️  Certificate is EXPIRED or not yet valid")
            print(f"  Valid from: {user_certificate.not_valid_before}")
            print(f"  Valid until: {user_certificate.not_valid_after}")
            print(f"  Current time: {now}")
        
        print(f"\n{'='*70}")
        print("VERIFICATION RESULT: ✓ VALID")
        print(f"{'='*70}\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Signature verification FAILED")
        print(f"  Error: {e}")
        print(f"\n{'='*70}")
        print("VERIFICATION RESULT: ✗ INVALID")
        print(f"{'='*70}\n")
        return False


def create_self_signed_certificate():
    """
    Create a self-signed certificate (NOT signed by our CA)
    
    Returns:
        x509.Certificate: Self-signed certificate
    """
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend
    import datetime
    
    print("\n[Creating Self-Signed Certificate]")
    print("This simulates a certificate NOT signed by our trusted CA...")
    
    # Generate key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Create self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Untrusted Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, "Fake Certificate"),
    ])
    
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .sign(private_key, hashes.SHA256(), default_backend())
    )
    
    print("✓ Self-signed certificate created")
    print(f"  Subject: Fake Certificate")
    print(f"  Issuer: Fake Certificate (self-signed)")
    
    return cert


def main():
    """Main demonstration"""
    
    print("="*70)
    print("CERTIFICATE VERIFICATION DEMONSTRATION")
    print("="*70)
    print("\nThis example shows how to verify if a certificate was signed by a CA")
    print("and demonstrates the difference between valid and invalid certificates.\n")
    
    input("Press Enter to begin...")
    
    # ========================================================================
    # SETUP: Create CA and issue certificates
    # ========================================================================
    print(f"\n{'#'*70}")
    print("# SETUP: Creating Certificate Authority")
    print(f"{'#'*70}\n")
    
    # Create Certificate Authority
    ca = CertificateAuthority(
        name="Trusted CA",
        country="IN",
        organization="PKI Authority"
    )
    
    ca_private_key, ca_certificate = ca.generate_root_certificate(
        key_size=2048,
        validity_days=3650
    )
    
    # Generate user key pair
    print("\n[Generating User Key Pair]")
    user_private_key, user_public_key = DigitalSignature.generate_key_pair(key_size=2048)
    
    # Issue legitimate certificate
    print("\n[Issuing Legitimate Certificate from CA]")
    legitimate_cert = ca.issue_certificate(
        subject_name="John Doe",
        subject_org="Legitimate Company",
        subject_email="john@legitimate.in",
        public_key=user_public_key,
        cert_class=2,
        validity_days=365
    )
    
    input("\nPress Enter to verify legitimate certificate...")
    
    # ========================================================================
    # TEST 1: Verify legitimate certificate
    # ========================================================================
    print(f"\n{'#'*70}")
    print("# TEST 1: Verifying Legitimate Certificate")
    print(f"{'#'*70}\n")
    
    print("This certificate was issued by our trusted CA.")
    print("Expected result: VALID\n")
    
    # Display certificate info
    DigitalCertificate.display_certificate_info(legitimate_cert, "Certificate to Verify")
    
    # Verify certificate
    is_valid = verify_certificate_manually(ca_certificate, legitimate_cert)
    
    input("\nPress Enter to test with self-signed certificate...")
    
    # ========================================================================
    # TEST 2: Verify self-signed certificate (should fail)
    # ========================================================================
    print(f"\n{'#'*70}")
    print("# TEST 2: Verifying Self-Signed Certificate (NOT from our CA)")
    print(f"{'#'*70}\n")
    
    print("This certificate was NOT signed by our trusted CA.")
    print("Expected result: INVALID\n")
    
    # Create self-signed certificate
    fake_cert = create_self_signed_certificate()
    
    # Display certificate info
    DigitalCertificate.display_certificate_info(fake_cert, "Self-Signed Certificate")
    
    # Try to verify (should fail)
    is_valid = verify_certificate_manually(ca_certificate, fake_cert)
    
    input("\nPress Enter to see comparison...")
    
    # ========================================================================
    # COMPARISON
    # ========================================================================
    print(f"\n{'#'*70}")
    print("# COMPARISON: Valid vs Invalid Certificates")
    print(f"{'#'*70}\n")
    
    print("LEGITIMATE CERTIFICATE (CA-Signed):")
    print("-" * 70)
    print(f"  Subject: {legitimate_cert.subject.rfc4514_string()}")
    print(f"  Issuer: {legitimate_cert.issuer.rfc4514_string()}")
    print(f"  Serial: {legitimate_cert.serial_number}")
    print(f"  Issuer matches CA: ✓ YES")
    print(f"  Signature valid: ✓ YES")
    print(f"  Trust: ✓ TRUSTED")
    
    print("\nSELF-SIGNED CERTIFICATE (NOT CA-Signed):")
    print("-" * 70)
    print(f"  Subject: {fake_cert.subject.rfc4514_string()}")
    print(f"  Issuer: {fake_cert.issuer.rfc4514_string()}")
    print(f"  Serial: {fake_cert.serial_number}")
    print(f"  Issuer matches CA: ✗ NO")
    print(f"  Signature valid: ✗ NO")
    print(f"  Trust: ✗ UNTRUSTED")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}\n")
    
    print("✓ Certificate Verification Process:")
    print("  1. Check if certificate issuer matches CA subject")
    print("  2. Verify cryptographic signature using CA's public key")
    print("  3. Check certificate validity period")
    print("  4. Verify certificate hasn't been tampered with")
    
    print("\n✓ Why This Matters:")
    print("  • Only certificates signed by trusted CAs are accepted")
    print("  • Prevents use of fake or self-signed certificates")
    print("  • Ensures identity verification through CA")
    print("  • Critical for secure communication and transactions")
    
    print("\n✓ Real-World Applications:")
    print("  • Web browsers verify SSL/TLS certificates")
    print("  • Email clients verify S/MIME certificates")
    print("  • Operating systems verify code signing certificates")
    print("  • Government portals verify digital signature certificates")
    
    print("\n🔐 Security Principle:")
    print("  Trust is established through the Certificate Authority.")
    print("  If you trust the CA, you can trust certificates signed by it.")
    print("  This is the foundation of Public Key Infrastructure (PKI).")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
