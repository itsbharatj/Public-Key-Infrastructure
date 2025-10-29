#!/usr/bin/env python3
"""
Example: Using PKI Modules Programmatically

This script shows how to use the PKI modules in your own applications.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from certificate_authority import CertificateAuthority
from digital_certificate import DigitalCertificate
from digital_signature import DigitalSignature


def example_1_create_ca():
    """Example 1: Create a Certificate Authority"""
    print("\n=== Example 1: Creating a Certificate Authority ===\n")
    
    # Initialize CA
    ca = CertificateAuthority(
        name="My Organization CA",
        country="IN",
        organization="My Company Ltd"
    )
    
    # Generate root certificate
    private_key, certificate = ca.generate_root_certificate(
        key_size=2048,
        validity_days=1825  # 5 years
    )
    
    # Save to files
    ca.save_certificate(certificate, "my_ca.pem")
    ca.save_private_key(private_key, "my_ca_key.pem")
    
    return ca


def example_2_issue_certificate(ca):
    """Example 2: Issue a digital certificate"""
    print("\n=== Example 2: Issuing a Digital Certificate ===\n")
    
    # Generate user's key pair
    user_private, user_public = DigitalSignature.generate_key_pair(key_size=2048)
    
    # Issue certificate
    cert = ca.issue_certificate(
        subject_name="John Doe",
        subject_org="Tech Corp",
        subject_email="john.doe@techcorp.in",
        public_key=user_public,
        cert_class=2,
        validity_days=365
    )
    
    # Display certificate info
    DigitalCertificate.display_certificate_info(cert)
    
    return user_private, cert


def example_3_sign_and_verify():
    """Example 3: Sign and verify a document"""
    print("\n=== Example 3: Digital Signature ===\n")
    
    # Generate key pair
    private_key, public_key = DigitalSignature.generate_key_pair()
    
    # Create document
    document = "This is a confidential agreement between parties."
    
    # Sign document
    signer = DigitalSignature(private_key=private_key)
    signature = signer.sign_document(document, "agreement.txt")
    
    # Verify signature
    verifier = DigitalSignature(public_key=public_key)
    is_valid = verifier.verify_signature(document, signature, "agreement.txt")
    
    print(f"\nSignature valid: {is_valid}")


def example_4_certificate_fingerprint():
    """Example 4: Get certificate fingerprint"""
    print("\n=== Example 4: Certificate Fingerprint ===\n")
    
    # Load a certificate
    cert = DigitalCertificate.load_certificate_from_file(
        "certificates/user_certificate.pem"
    )
    
    # Get fingerprint
    fingerprint = DigitalCertificate.get_certificate_fingerprint(cert, "SHA256")
    print(f"Certificate Fingerprint (SHA-256):\n{fingerprint}")


def main():
    print("="*70)
    print("PKI Programming Examples")
    print("="*70)
    
    # Example 1: Create CA
    ca = example_1_create_ca()
    
    # Example 2: Issue certificate
    user_private, user_cert = example_2_issue_certificate(ca)
    
    # Example 3: Sign and verify
    example_3_sign_and_verify()
    
    # Example 4: Certificate fingerprint (requires existing certificate)
    if os.path.exists("certificates/user_certificate.pem"):
        example_4_certificate_fingerprint()
    
    print("\n" + "="*70)
    print("All examples completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
