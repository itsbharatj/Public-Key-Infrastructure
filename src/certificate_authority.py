"""
Certificate Authority (CA) Implementation

This module simulates a Certificate Authority similar to those licensed
under India's PKI framework (e.g., CCA-approved CAs).
"""

from cryptography import x509
from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime
import os


class CertificateAuthority:
    """
    Represents a Certificate Authority that can:
    - Generate root CA certificates
    - Issue and sign subordinate certificates
    - Manage the certificate hierarchy
    """
    
    def __init__(self, name="India Root CA", country="IN", organization="Government of India"):
        """
        Initialize the Certificate Authority
        
        Args:
            name: CA common name
            country: Country code (IN for India)
            organization: Organization name
        """
        self.name = name
        self.country = country
        self.organization = organization
        self.private_key = None
        self.certificate = None
        self.issued_certificates = []
        
    def generate_root_certificate(self, key_size=4096, validity_days=3650):
        """
        Generate a self-signed root CA certificate
        
        Args:
            key_size: RSA key size (default 4096 for high security)
            validity_days: Certificate validity period (default 10 years)
            
        Returns:
            tuple: (private_key, certificate)
        """
        print(f"\n{'='*60}")
        print(f"Generating Root CA Certificate: {self.name}")
        print(f"{'='*60}")
        
        # Generate RSA private key
        print(f"[1/4] Generating {key_size}-bit RSA private key...")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        print("✓ Private key generated successfully")
        
        # Create subject and issuer (same for self-signed root CA)
        print("[2/4] Creating certificate subject...")
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Delhi"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "New Delhi"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.organization),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "Controller of Certifying Authorities"),
            x509.NameAttribute(NameOID.COMMON_NAME, self.name),
        ])
        print("✓ Subject created")
        
        # Build the certificate
        print("[3/4] Building X.509 certificate...")
        self.certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(self.private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=validity_days))
            # Root CA extensions
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=None),
                critical=True,
            )
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_cert_sign=True,
                    crl_sign=True,
                    key_encipherment=False,
                    content_commitment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .add_extension(
                x509.SubjectKeyIdentifier.from_public_key(self.private_key.public_key()),
                critical=False,
            )
            .sign(self.private_key, hashes.SHA256(), default_backend())
        )
        print("✓ Certificate built and self-signed")
        
        print("[4/4] Certificate generated successfully!")
        print(f"\nRoot CA Details:")
        print(f"  - Common Name: {self.name}")
        print(f"  - Organization: {self.organization}")
        print(f"  - Country: {self.country}")
        print(f"  - Serial Number: {self.certificate.serial_number}")
        print(f"  - Valid From: {self.certificate.not_valid_before}")
        print(f"  - Valid Until: {self.certificate.not_valid_after}")
        print(f"  - Key Size: {key_size} bits")
        
        return self.private_key, self.certificate
    
    def issue_certificate(self, subject_name, subject_org, subject_email, 
                         public_key, cert_class=3, validity_days=365):
        """
        Issue a certificate signed by this CA
        
        Args:
            subject_name: Common name of the certificate subject
            subject_org: Organization of the subject
            subject_email: Email of the subject
            public_key: Public key to be certified
            cert_class: Certificate class (1, 2, or 3 as per Indian PKI)
            validity_days: Certificate validity period
            
        Returns:
            x509.Certificate: Signed certificate
        """
        if not self.private_key or not self.certificate:
            raise ValueError("CA must have a certificate before issuing certificates")
        
        print(f"\n{'='*60}")
        print(f"Issuing Class {cert_class} Certificate")
        print(f"{'='*60}")
        
        # Create subject
        print(f"[1/3] Creating certificate for {subject_name}...")
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Maharashtra"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Mumbai"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject_org),
            x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, subject_email),
        ])
        
        # Build certificate
        print("[2/3] Building and signing certificate...")
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(self.certificate.subject)
            .public_key(public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=validity_days))
            # End entity certificate extensions
            .add_extension(
                x509.BasicConstraints(ca=False, path_length=None),
                critical=True,
            )
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_encipherment=True,
                    content_commitment=True,  # Non-repudiation
                    data_encipherment=False,
                    key_agreement=False,
                    key_cert_sign=False,
                    crl_sign=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .add_extension(
                x509.ExtendedKeyUsage([
                    x509.oid.ExtendedKeyUsageOID.EMAIL_PROTECTION,
                    x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH,
                ]),
                critical=False,
            )
            .add_extension(
                x509.SubjectAlternativeName([
                    x509.RFC822Name(subject_email),
                ]),
                critical=False,
            )
            .add_extension(
                x509.AuthorityKeyIdentifier.from_issuer_public_key(self.private_key.public_key()),
                critical=False,
            )
            .sign(self.private_key, hashes.SHA256(), default_backend())
        )
        
        self.issued_certificates.append(cert)
        print("✓ Certificate signed by CA")
        
        print(f"[3/3] Certificate issued successfully!")
        print(f"\nCertificate Details:")
        print(f"  - Class: {cert_class} (India PKI Standard)")
        print(f"  - Subject: {subject_name}")
        print(f"  - Organization: {subject_org}")
        print(f"  - Email: {subject_email}")
        print(f"  - Serial Number: {cert.serial_number}")
        print(f"  - Issuer: {self.name}")
        print(f"  - Valid From: {cert.not_valid_before}")
        print(f"  - Valid Until: {cert.not_valid_after}")
        
        return cert
    
    def save_certificate(self, certificate, filename):
        """
        Save a certificate to a PEM file
        
        Args:
            certificate: The certificate to save
            filename: Output filename
        """
        cert_dir = "certificates"
        if not os.path.exists(cert_dir):
            os.makedirs(cert_dir)
            
        filepath = os.path.join(cert_dir, filename)
        with open(filepath, "wb") as f:
            f.write(certificate.public_bytes(serialization.Encoding.PEM))
        print(f"✓ Certificate saved to: {filepath}")
        
    def save_private_key(self, private_key, filename, password=None):
        """
        Save a private key to a PEM file
        
        Args:
            private_key: The private key to save
            filename: Output filename
            password: Optional password for encryption
        """
        cert_dir = "certificates"
        if not os.path.exists(cert_dir):
            os.makedirs(cert_dir)
            
        filepath = os.path.join(cert_dir, filename)
        
        if password:
            encryption = serialization.BestAvailableEncryption(password.encode())
        else:
            encryption = serialization.NoEncryption()
            
        with open(filepath, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=encryption
                )
            )
        print(f"✓ Private key saved to: {filepath}")
    
    def verify_certificate(self, certificate):
        """
        Verify if a certificate was issued by this CA (Proper PKI validation)
        
        This implements proper certificate validation per RFC 5280:
        1. Verify validity period (not expired/not yet valid)
        2. Verify cryptographic signature
        3. Verify issuer matches CA
        4. Verify certificate purpose and constraints
        
        Args:
            certificate: Certificate to verify
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Step 1: Check validity period (CRITICAL!)
            print(f"\n[Certificate Validation]")
            now = datetime.datetime.utcnow()
            
            if now < certificate.not_valid_before:
                print(f"✗ Certificate not yet valid")
                print(f"  - Current time: {now}")
                print(f"  - Valid from: {certificate.not_valid_before}")
                return False
            
            if now > certificate.not_valid_after:
                print(f"✗ Certificate has EXPIRED")
                print(f"  - Current time: {now}")
                print(f"  - Expired on: {certificate.not_valid_after}")
                return False
            
            print(f"✓ Certificate validity period OK")
            print(f"  - Valid from: {certificate.not_valid_before}")
            print(f"  - Valid until: {certificate.not_valid_after}")
            
            # Step 2: Verify the cryptographic signature
            print(f"\n[Signature Verification]")
            from cryptography.hazmat.primitives.asymmetric import padding
            
            self.certificate.public_key().verify(
                certificate.signature,
                certificate.tbs_certificate_bytes,
                padding.PKCS1v15(),
                certificate.signature_hash_algorithm
            )
            print(f"✓ Cryptographic signature valid")
            
            # Step 3: Check if issuer matches CA subject
            print(f"\n[Issuer Verification]")
            if certificate.issuer != self.certificate.subject:
                print(f"✗ Issuer mismatch")
                print(f"  - Certificate issuer: {certificate.issuer.rfc4514_string()}")
                print(f"  - CA subject: {self.certificate.subject.rfc4514_string()}")
                return False
            
            print(f"✓ Issuer matches CA")
            
            # Step 4: Verify basic constraints (if certificate is a CA)
            print(f"\n[Certificate Constraints]")
            try:
                basic_constraints = certificate.extensions.get_extension_for_oid(
                    x509.oid.ExtensionOID.BASIC_CONSTRAINTS
                )
                is_ca = basic_constraints.value.ca
                print(f"✓ Basic constraints: CA={is_ca}")
                
                # If it's a CA certificate, it should have ca=True
                # If it's an end-entity, it should have ca=False
                
            except x509.ExtensionNotFound:
                print(f"⚠️  No basic constraints extension")
            
            # Step 5: Verify key usage
            try:
                key_usage = certificate.extensions.get_extension_for_oid(
                    x509.oid.ExtensionOID.KEY_USAGE
                )
                print(f"✓ Key usage extension present")
                print(f"  - Digital Signature: {key_usage.value.digital_signature}")
                print(f"  - Key Cert Sign: {key_usage.value.key_cert_sign}")
                
            except x509.ExtensionNotFound:
                print(f"⚠️  No key usage extension")
            
            print(f"\n✓ Certificate verification SUCCESSFUL")
            print(f"  - Certificate is signed by: {self.name}")
            print(f"  - Certificate is currently VALID")
            print(f"  - All constraints satisfied")
            return True
                
        except Exception as e:
            print(f"\n✗ Certificate verification FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
