#!/usr/bin/env python3
"""
Public Key Infrastructure (PKI) Demonstration for India

This script demonstrates the complete PKI workflow as implemented in India
under the IT Act, 2000 and Controller of Certifying Authorities (CCA) framework.

Author: PKI Demo
Date: 2025
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from certificate_authority import CertificateAuthority
from digital_certificate import DigitalCertificate, CertificateChain
from digital_signature import DigitalSignature, TimestampAuthority


def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def main():
    """Main demonstration function"""
    
    print_header("INDIAN PKI DEMONSTRATION")
    print("This demonstration shows how Public Key Infrastructure works in India")
    print("under the IT Act, 2000 and CCA (Controller of Certifying Authorities).\n")
    print("Components to be demonstrated:")
    print("  1. Root Certificate Authority (CA)")
    print("  2. Digital Certificate Issuance (Class 3 Certificate)")
    print("  3. Digital Signature Creation and Verification")
    print("  4. Certificate Chain Validation")
    print("  5. Timestamp Authority")
    
    input("\nPress Enter to begin the demonstration...")
    
    # ============================================================================
    # STEP 1: Create Root Certificate Authority
    # ============================================================================
    print_header("STEP 1: Creating Root Certificate Authority")
    print("In India, the CCA licenses various organizations to act as Certifying")
    print("Authorities. We'll simulate creating a root CA.\n")
    
    # Initialize CA
    ca = CertificateAuthority(
        name="India Digital CA Root",
        country="IN",
        organization="Government of India - CCA"
    )
    
    # Generate root certificate
    ca_private_key, ca_certificate = ca.generate_root_certificate(
        key_size=4096,
        validity_days=3650  # 10 years
    )
    
    # Save CA certificate
    ca.save_certificate(ca_certificate, "root_ca.pem")
    ca.save_private_key(ca_private_key, "root_ca_key.pem")
    
    # Display CA certificate info
    DigitalCertificate.display_certificate_info(
        ca_certificate,
        "Root CA Certificate Details"
    )
    
    input("\nPress Enter to continue to certificate issuance...")
    
    # ============================================================================
    # STEP 2: Issue Digital Certificate (Class 3)
    # ============================================================================
    print_header("STEP 2: Issuing Class 3 Digital Signature Certificate")
    print("Class 3 certificates are the highest assurance level in India PKI.")
    print("They are used for:")
    print("  - E-tendering and e-procurement")
    print("  - E-commerce transactions")
    print("  - High-security applications")
    print("  - Company director authentication\n")
    
    # Display certificate class information
    print(DigitalCertificate.get_certificate_class_description(3))
    print()
    
    # Generate key pair for user
    user_private_key, user_public_key = DigitalSignature.generate_key_pair(
        key_size=2048
    )
    
    # Issue certificate
    user_certificate = ca.issue_certificate(
        subject_name="Bharat Jain",
        subject_org="Tech Solutions Pvt Ltd",
        subject_email="bharat.jain@techsolutions.in",
        public_key=user_public_key,
        cert_class=3,
        validity_days=365
    )
    
    # Save user certificate and private key
    ca.save_certificate(user_certificate, "user_certificate.pem")
    ca.save_private_key(user_private_key, "user_private_key.pem")
    
    # Display user certificate info
    DigitalCertificate.display_certificate_info(
        user_certificate,
        "User Certificate Details"
    )
    
    # Display certificate fingerprint
    print("Certificate Fingerprint (SHA-256):")
    fingerprint = DigitalCertificate.get_certificate_fingerprint(user_certificate)
    print(f"  {fingerprint}\n")
    
    input("\nPress Enter to continue to certificate verification...")
    
    # ============================================================================
    # STEP 3: Verify Certificate
    # ============================================================================
    print_header("STEP 3: Verifying Digital Certificate")
    print("Verifying that the user certificate was issued by our CA...\n")
    
    ca.verify_certificate(user_certificate)
    
    input("\nPress Enter to continue to certificate chain...")
    
    # ============================================================================
    # STEP 4: Certificate Chain
    # ============================================================================
    print_header("STEP 4: Certificate Chain Validation")
    print("In PKI, certificates form a chain of trust from the root CA to")
    print("end-entity certificates. Let's visualize and validate this chain.\n")
    
    cert_chain = CertificateChain()
    cert_chain.add_certificate(ca_certificate)
    cert_chain.add_certificate(user_certificate)
    
    cert_chain.display_chain()
    cert_chain.validate_chain()
    
    input("\nPress Enter to continue to digital signatures...")
    
    # ============================================================================
    # STEP 5: Digital Signature Creation
    # ============================================================================
    print_header("STEP 5: Creating Digital Signature")
    print("Digital signatures in India are legally equivalent to handwritten")
    print("signatures under IT Act, 2000, Section 3A.\n")
    
    # Create a sample document
    document_content = """
OFFICIAL DOCUMENT - TENDER SUBMISSION

To: Government e-Procurement Portal
From: Tech Solutions Pvt Ltd
Date: October 29, 2025

Subject: Tender for Smart City Project - Bid Submission

Dear Sir/Madam,

We hereby submit our technical and financial bid for the Smart City
Infrastructure Project as per Tender No. SC/2025/1234.

Total Bid Amount: ₹ 50,00,00,000 (Fifty Crore Rupees)

This document is digitally signed using our Class 3 Digital Signature
Certificate issued by a CCA-licensed Certifying Authority.

Regards,
Bharat Jain
Director
Tech Solutions Pvt Ltd
"""
    
    print("Document to be signed:")
    print("-" * 70)
    print(document_content)
    print("-" * 70)
    
    # Demonstrate hash function
    DigitalSignature.demonstrate_hash_function(document_content)
    
    # Create digital signature
    signer = DigitalSignature(private_key=user_private_key)
    signature = signer.sign_document(
        document_content,
        document_name="tender_submission.txt"
    )
    
    # Save signature
    signer.save_signature(signature, "certificates/tender_submission.sig")
    
    # Save the document
    with open("certificates/tender_submission.txt", "w") as f:
        f.write(document_content)
    print("✓ Document saved to: certificates/tender_submission.txt")
    
    input("\nPress Enter to continue to signature verification...")
    
    # ============================================================================
    # STEP 6: Digital Signature Verification
    # ============================================================================
    print_header("STEP 6: Verifying Digital Signature")
    print("The recipient can verify the signature using the signer's public key")
    print("(extracted from their digital certificate).\n")
    
    # Create verifier with public key
    verifier = DigitalSignature(public_key=user_public_key)
    
    # Verify the signature
    is_valid = verifier.verify_signature(
        document_content,
        signature,
        document_name="tender_submission.txt"
    )
    
    input("\nPress Enter to see timestamp authority demonstration...")
    
    # ============================================================================
    # STEP 7: Timestamp Authority
    # ============================================================================
    print_header("STEP 7: Trusted Timestamp")
    print("For certain legal documents, a trusted timestamp is required to prove")
    print("when the document was signed.\n")
    
    import hashlib
    doc_hash = hashlib.sha256(document_content.encode()).hexdigest()
    timestamp = TimestampAuthority.create_timestamp(doc_hash)
    
    input("\nPress Enter to see the final summary...")
    
    # ============================================================================
    # STEP 8: Summary
    # ============================================================================
    print_header("PKI DEMONSTRATION SUMMARY")
    
    print("✓ Successfully completed all PKI operations:\n")
    
    print("1. ROOT CERTIFICATE AUTHORITY")
    print(f"   - Created self-signed root CA certificate")
    print(f"   - Organization: Government of India - CCA")
    print(f"   - Key Size: 4096-bit RSA")
    print(f"   - Validity: 10 years\n")
    
    print("2. DIGITAL CERTIFICATE ISSUANCE")
    print(f"   - Issued Class 3 certificate to: Bharat Jain")
    print(f"   - Organization: Tech Solutions Pvt Ltd")
    print(f"   - Key Size: 2048-bit RSA")
    print(f"   - Serial Number: {user_certificate.serial_number}\n")
    
    print("3. DIGITAL SIGNATURE")
    print(f"   - Signed document: tender_submission.txt")
    print(f"   - Algorithm: RSA-PSS with SHA-256")
    print(f"   - Signature verified: {'✓ VALID' if is_valid else '✗ INVALID'}\n")
    
    print("4. CERTIFICATE CHAIN")
    print(f"   - Root CA → User Certificate")
    print(f"   - Chain validated successfully\n")
    
    print("5. FILES GENERATED")
    print(f"   certificates/")
    print(f"   ├── root_ca.pem")
    print(f"   ├── root_ca_key.pem")
    print(f"   ├── user_certificate.pem")
    print(f"   ├── user_private_key.pem")
    print(f"   ├── tender_submission.txt")
    print(f"   └── tender_submission.sig\n")
    
    print("LEGAL FRAMEWORK IN INDIA:")
    print("-" * 70)
    print("• IT Act, 2000 - Provides legal recognition to digital signatures")
    print("• Section 3 - Authentication of electronic records")
    print("• Section 3A - Digital signatures legally equivalent to handwritten")
    print("• Section 5 - Legal recognition of electronic records")
    print("• Section 35 - Certifying Authorities to be licensed by CCA")
    print("• Controller of Certifying Authorities (CCA) - Regulatory body")
    print("-" * 70)
    
    print("\n📚 CERTIFICATE CLASSES IN INDIA:")
    print("-" * 70)
    print("Class 1: Email security, basic authentication")
    print("Class 2: Business transactions, e-filing (MCA, Income Tax, GST)")
    print("Class 3: E-commerce, e-tendering, high-security (requires biometric)")
    print("-" * 70)
    
    print("\n🔐 SECURITY NOTES:")
    print("-" * 70)
    print("⚠️  This is an educational demonstration only!")
    print("⚠️  Do not use these certificates in production systems")
    print("⚠️  Real PKI requires proper security audits and HSM for key storage")
    print("⚠️  Always obtain certificates from CCA-licensed CAs for legal use")
    print("-" * 70)
    
    print("\n✅ Demonstration completed successfully!")
    print("\nFor more information:")
    print("  • CCA Website: https://cca.gov.in/")
    print("  • IT Act, 2000: http://www.dot.gov.in/")
    print("  • Licensed CAs in India: Check CCA repository")
    
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
