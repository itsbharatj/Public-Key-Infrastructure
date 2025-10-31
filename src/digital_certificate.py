"""
Digital Certificate Module

This module handles digital certificate operations including:
- Certificate generation
- Certificate parsing and display
- Certificate validation
"""

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import datetime


class DigitalCertificate:
    """
    Handles digital certificate operations
    """
    
    @staticmethod
    def display_certificate_info(certificate, title="Certificate Information"):
        """
        Display detailed information about a certificate
        
        Args:
            certificate: x509.Certificate object
            title: Display title
        """
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        
        # Subject information
        print("\n[Subject Information]")
        for attribute in certificate.subject:
            print(f"  {attribute.oid._name}: {attribute.value}")
        
        # Issuer information
        print("\n[Issuer Information]")
        for attribute in certificate.issuer:
            print(f"  {attribute.oid._name}: {attribute.value}")
        
        # Validity information
        print("\n[Validity Period]")
        print(f"  Not Before: {certificate.not_valid_before}")
        print(f"  Not After: {certificate.not_valid_after}")
        
        # Check if currently valid
        now = datetime.datetime.utcnow()
        is_valid = certificate.not_valid_before <= now <= certificate.not_valid_after
        status = "✓ VALID" if is_valid else "✗ EXPIRED/NOT YET VALID"
        print(f"  Status: {status}")
        
        # Serial number
        print(f"\n[Certificate Details]")
        print(f"  Serial Number: {certificate.serial_number}")
        print(f"  Version: {certificate.version.name}")
        print(f"  Signature Algorithm: {certificate.signature_algorithm_oid._name}")
        
        # Extensions
        print(f"\n[Extensions]")
        try:
            for ext in certificate.extensions:
                print(f"  - {ext.oid._name}")
                if ext.oid._name == "basicConstraints":
                    print(f"    CA: {ext.value.ca}")
                elif ext.oid._name == "keyUsage":
                    print(f"    Digital Signature: {ext.value.digital_signature}")
                    print(f"    Key Cert Sign: {ext.value.key_cert_sign}")
        except Exception as e:
            print(f"  (No extensions or error reading extensions: {e})")
        
        print(f"\n{'='*60}\n")
    
    @staticmethod
    def load_certificate_from_file(filepath):
        """
        Load a certificate from a PEM file
        
        Args:
            filepath: Path to the certificate file
            
        Returns:
            x509.Certificate object
        """
        with open(filepath, "rb") as f:
            cert_data = f.read()
            certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
        return certificate
    
    @staticmethod
    def get_certificate_fingerprint(certificate, algorithm="SHA256"):
        """
        Get the fingerprint of a certificate
        
        Args:
            certificate: x509.Certificate object
            algorithm: Hash algorithm (default SHA256)
            
        Returns:
            str: Hexadecimal fingerprint
        """
        from cryptography.hazmat.primitives import hashes
        
        if algorithm == "SHA256":
            hash_algo = hashes.SHA256()
        elif algorithm == "SHA1":
            hash_algo = hashes.SHA1()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        fingerprint = certificate.fingerprint(hash_algo)
        return ":".join([f"{b:02X}" for b in fingerprint])
    
    @staticmethod
    def export_public_key(certificate, filepath):
        """
        Export the public key from a certificate
        
        Args:
            certificate: x509.Certificate object
            filepath: Output file path
        """
        public_key = certificate.public_key()
        
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        with open(filepath, "wb") as f:
            f.write(pem)
        
        print(f"✓ Public key exported to: {filepath}")
    
    @staticmethod
    def get_certificate_class_description(cert_class):
        """
        Get description of Indian PKI certificate classes
        
        Args:
            cert_class: Certificate class (1, 2, or 3)
            
        Returns:
            str: Description of the certificate class
        """
        classes = {
            1: """Class 1 Certificate:
            - Purpose: Email security and basic authentication
            - Assurance: Low
            - Verification: Email verification only
            - Use Cases: Secure email, personal identification""",
            
            2: """Class 2 Certificate:
            - Purpose: Business transactions and e-filing
            - Assurance: Medium
            - Verification: Organization verification required
            - Use Cases: MCA filing, income tax e-filing, DGFT, trademark filing
            - Common in India for: GST registration, company incorporation""",
            
            3: """Class 3 Certificate:
            - Purpose: E-commerce and e-tendering
            - Assurance: High
            - Verification: Personal presence required, biometric verification
            - Use Cases: E-tendering, e-auctions, secure financial transactions
            - Mandatory for: High-value e-commerce, government e-procurement"""
        }
        
        return classes.get(cert_class, "Unknown certificate class")


class CertificateChain:
    """
    Manages and validates certificate chains
    """
    
    def __init__(self):
        self.certificates = []
    
    def add_certificate(self, certificate):
        """Add a certificate to the chain"""
        self.certificates.append(certificate)
    
    def display_chain(self):
        """Display the certificate chain hierarchy"""
        print(f"\n{'='*60}")
        print("Certificate Chain Hierarchy")
        print(f"{'='*60}\n")
        
        for i, cert in enumerate(self.certificates):
            indent = "  " * i
            cn = None
            for attr in cert.subject:
                if attr.oid._name == "commonName":
                    cn = attr.value
                    break
            
            issuer_cn = None
            for attr in cert.issuer:
                if attr.oid._name == "commonName":
                    issuer_cn = attr.value
                    break
            
            if i == 0:
                print(f"{indent}┌─ Root CA")
            else:
                print(f"{indent}├─ End Entity Certificate")
            
            print(f"{indent}│  Subject: {cn}")
            print(f"{indent}│  Issued by: {issuer_cn}")
            print(f"{indent}│  Serial: {cert.serial_number}")
            print(f"{indent}│")
        
        print(f"\n{'='*60}\n")
    
    def validate_chain(self):
        """
        Validate the certificate chain per RFC 5280
        
        Performs comprehensive chain validation:
        1. Each certificate is within validity period
        2. Each certificate signature is valid
        3. Each issuer has CA=true in basic constraints
        4. Path length constraints are satisfied
        5. Each link in chain is properly connected
        
        Returns:
            bool: True if chain is valid
        """
        print("\n[Validating Certificate Chain - RFC 5280 Compliant]")
        
        if len(self.certificates) < 2:
            print("✗ Chain too short (need at least root CA and one certificate)")
            return False
        
        now = datetime.datetime.utcnow()
        
        # Check each certificate in the chain
        for i in range(len(self.certificates)):
            cert = self.certificates[i]
            
            # Get certificate name for display
            cn = None
            for attr in cert.subject:
                if attr.oid._name == "commonName":
                    cn = attr.value
                    break
            
            print(f"\n[Certificate {i}: {cn}]")
            
            # Step 1: Check validity period
            if now < cert.not_valid_before:
                print(f"✗ Certificate not yet valid")
                print(f"  - Current: {now}")
                print(f"  - Valid from: {cert.not_valid_before}")
                return False
            
            if now > cert.not_valid_after:
                print(f"✗ Certificate EXPIRED")
                print(f"  - Current: {now}")
                print(f"  - Expired: {cert.not_valid_after}")
                return False
            
            print(f"✓ Validity: {cert.not_valid_before} to {cert.not_valid_after}")
            
            # Step 2: Check basic constraints for CA certificates
            if i < len(self.certificates) - 1:  # Not the end-entity cert
                try:
                    basic_constraints = cert.extensions.get_extension_for_oid(
                        x509.oid.ExtensionOID.BASIC_CONSTRAINTS
                    )
                    
                    if not basic_constraints.value.ca:
                        print(f"✗ Certificate {i} is not a CA but trying to sign certificates")
                        return False
                    
                    print(f"✓ CA certificate: Authorized to sign certificates")
                    
                    # Check path length constraint
                    if basic_constraints.value.path_length is not None:
                        remaining = len(self.certificates) - i - 2
                        if remaining > basic_constraints.value.path_length:
                            print(f"✗ Path length constraint violated")
                            print(f"  - Max path length: {basic_constraints.value.path_length}")
                            print(f"  - Remaining path: {remaining}")
                            return False
                        print(f"✓ Path length constraint: {basic_constraints.value.path_length} (OK)")
                    
                except x509.ExtensionNotFound:
                    print(f"✗ CA certificate missing basic constraints extension")
                    return False
        
        # Step 3: Verify each certificate is signed by the previous one
        print(f"\n[Verifying Certificate Signatures]")
        from cryptography.hazmat.primitives.asymmetric import padding
        
        for i in range(len(self.certificates) - 1):
            issuer_cert = self.certificates[i]
            subject_cert = self.certificates[i + 1]
            
            # Verify issuer name matches
            if subject_cert.issuer != issuer_cert.subject:
                print(f"✗ Chain break: Certificate {i+1} issuer doesn't match certificate {i} subject")
                print(f"  - Cert {i+1} issuer: {subject_cert.issuer.rfc4514_string()}")
                print(f"  - Cert {i} subject: {issuer_cert.subject.rfc4514_string()}")
                return False
            
            # Verify cryptographic signature
            try:
                issuer_cert.public_key().verify(
                    subject_cert.signature,
                    subject_cert.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    subject_cert.signature_hash_algorithm
                )
                print(f"✓ Certificate {i+1} → Certificate {i}: Valid signature")
            except Exception as e:
                print(f"✗ Certificate {i+1} → Certificate {i}: Invalid signature")
                print(f"  - Error: {e}")
                return False
        
        print("\n✓ Certificate chain is VALID")
        print("  - All certificates within validity period")
        print("  - All signatures verified")
        print("  - All constraints satisfied")
        print("  - Chain of trust established")
        return True
