"""
Digital Signature Module

This module implements digital signature operations as per Indian IT Act, 2000.
Digital signatures provide:
- Authentication: Verifies the identity of the signer
- Integrity: Ensures the document hasn't been tampered with
- Non-repudiation: Signer cannot deny signing the document
"""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import hashlib
import os


class DigitalSignature:
    """
    Handles digital signature creation and verification
    """
    
    def __init__(self, private_key=None, public_key=None):
        """
        Initialize Digital Signature handler
        
        Args:
            private_key: RSA private key for signing
            public_key: RSA public key for verification
        """
        self.private_key = private_key
        self.public_key = public_key
    
    @staticmethod
    def generate_key_pair(key_size=2048):
        """
        Generate RSA key pair for digital signatures
        
        Args:
            key_size: RSA key size in bits (2048 or 4096 recommended)
            
        Returns:
            tuple: (private_key, public_key)
        """
        print(f"\n{'='*60}")
        print(f"Generating RSA Key Pair for Digital Signatures")
        print(f"{'='*60}")
        print(f"Key Size: {key_size} bits")
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        
        public_key = private_key.public_key()
        
        print("✓ Key pair generated successfully")
        print(f"  - Private key: {key_size}-bit RSA")
        print(f"  - Public key: {key_size}-bit RSA")
        print(f"  - Algorithm: RSA with SHA-256")
        
        return private_key, public_key
    
    def sign_document(self, document, document_name="document.txt"):
        """
        Create a digital signature for a document
        
        Args:
            document: Document content (bytes or string)
            document_name: Name of the document being signed
            
        Returns:
            bytes: Digital signature
        """
        if not self.private_key:
            raise ValueError("Private key is required for signing")
        
        print(f"\n{'='*60}")
        print(f"Creating Digital Signature")
        print(f"{'='*60}")
        
        # Convert to bytes if string
        if isinstance(document, str):
            document = document.encode('utf-8')
        
        print(f"Document: {document_name}")
        print(f"Document size: {len(document)} bytes")
        
        # Calculate document hash
        print("[1/3] Calculating document hash (SHA-256)...")
        doc_hash = hashlib.sha256(document).hexdigest()
        print(f"✓ Document hash: {doc_hash[:32]}...")
        
        # Sign the document
        print("[2/3] Signing document with private key...")
        signature = self.private_key.sign(
            document,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(f"✓ Signature created: {len(signature)} bytes")
        
        print("[3/3] Digital signature complete!")
        print(f"\nSignature Details:")
        print(f"  - Algorithm: RSA-PSS with SHA-256")
        print(f"  - Padding: PSS (Probabilistic Signature Scheme)")
        print(f"  - Hash: SHA-256")
        print(f"  - Signature size: {len(signature)} bytes")
        print(f"  - Legal validity: As per IT Act, 2000, Section 3")
        
        return signature
    
    def verify_signature(self, document, signature, document_name="document.txt"):
        """
        Verify a digital signature
        
        Args:
            document: Original document content (bytes or string)
            signature: Digital signature to verify
            document_name: Name of the document
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not self.public_key:
            raise ValueError("Public key is required for verification")
        
        print(f"\n{'='*60}")
        print(f"Verifying Digital Signature")
        print(f"{'='*60}")
        
        # Convert to bytes if string
        if isinstance(document, str):
            document = document.encode('utf-8')
        
        print(f"Document: {document_name}")
        print(f"Signature size: {len(signature)} bytes")
        
        try:
            print("[1/2] Verifying signature with public key...")
            self.public_key.verify(
                signature,
                document,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            print("✓ Signature verification SUCCESSFUL")
            print("[2/2] Calculating document integrity...")
            
            doc_hash = hashlib.sha256(document).hexdigest()
            print(f"✓ Document hash: {doc_hash[:32]}...")
            
            print(f"\n{'='*60}")
            print("VERIFICATION RESULT: ✓ VALID")
            print(f"{'='*60}")
            print("\nSignature Properties:")
            print("  ✓ Authentication: Verified - Signed by legitimate key holder")
            print("  ✓ Integrity: Verified - Document has not been modified")
            print("  ✓ Non-repudiation: Ensured - Signer cannot deny signing")
            print("\nLegal Status (India):")
            print("  - This signature is legally valid under IT Act, 2000")
            print("  - Equivalent to handwritten signature (Section 3A)")
            print("  - Admissible as evidence in court (Section 5)")
            
            return True
            
        except Exception as e:
            print(f"✗ Signature verification FAILED")
            print(f"✗ Error: {str(e)}")
            
            print(f"\n{'='*60}")
            print("VERIFICATION RESULT: ✗ INVALID")
            print(f"{'='*60}")
            print("\nPossible Reasons:")
            print("  - Document has been modified after signing")
            print("  - Signature was created with a different key")
            print("  - Signature has been tampered with")
            print("  - Wrong public key used for verification")
            
            return False
    
    def save_signature(self, signature, filepath):
        """
        Save a digital signature to a file
        
        Args:
            signature: Signature bytes
            filepath: Output file path
        """
        with open(filepath, 'wb') as f:
            f.write(signature)
        print(f"✓ Signature saved to: {filepath}")
    
    @staticmethod
    def load_signature(filepath):
        """
        Load a digital signature from a file
        
        Args:
            filepath: Path to signature file
            
        Returns:
            bytes: Signature data
        """
        with open(filepath, 'rb') as f:
            signature = f.read()
        print(f"✓ Signature loaded from: {filepath}")
        return signature
    
    @staticmethod
    def demonstrate_hash_function(data):
        """
        Demonstrate cryptographic hash functions used in digital signatures
        
        Args:
            data: Data to hash (string or bytes)
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        print(f"\n{'='*60}")
        print("Cryptographic Hash Demonstration")
        print(f"{'='*60}")
        print(f"Input data: {data.decode('utf-8')[:50]}...")
        print(f"Data size: {len(data)} bytes\n")
        
        # SHA-256 (most commonly used in India PKI)
        sha256_hash = hashlib.sha256(data).hexdigest()
        print(f"SHA-256 Hash:")
        print(f"  {sha256_hash}")
        print(f"  Length: 64 characters (256 bits)")
        print(f"  Use: Digital signatures, certificate fingerprints\n")
        
        # SHA-1 (legacy, still used in some cases)
        sha1_hash = hashlib.sha1(data).hexdigest()
        print(f"SHA-1 Hash:")
        print(f"  {sha1_hash}")
        print(f"  Length: 40 characters (160 bits)")
        print(f"  Status: Deprecated, use SHA-256 instead\n")
        
        # MD5 (for demonstration only, not secure)
        md5_hash = hashlib.md5(data).hexdigest()
        print(f"MD5 Hash:")
        print(f"  {md5_hash}")
        print(f"  Length: 32 characters (128 bits)")
        print(f"  Status: Insecure, for checksums only\n")
        
        print("Hash Properties:")
        print("  ✓ Deterministic: Same input always produces same hash")
        print("  ✓ One-way: Cannot reverse hash to get original data")
        print("  ✓ Collision-resistant: Hard to find two inputs with same hash")
        print("  ✓ Avalanche effect: Small change in input drastically changes hash")
        
        return sha256_hash


class TimestampAuthority:
    """
    Simulates a Timestamp Authority for timestamping digital signatures
    (As required under IT Act for certain legal documents)
    """
    
    @staticmethod
    def create_timestamp(document_hash):
        """
        Create a trusted timestamp for a document
        
        Args:
            document_hash: Hash of the document
            
        Returns:
            dict: Timestamp information
        """
        from datetime import datetime
        
        timestamp_info = {
            'document_hash': document_hash,
            'timestamp': datetime.utcnow().isoformat(),
            'tsa': 'India Timestamp Authority (Demo)',
            'algorithm': 'SHA-256'
        }
        
        print(f"\n{'='*60}")
        print("Trusted Timestamp Created")
        print(f"{'='*60}")
        print(f"Document Hash: {document_hash[:32]}...")
        print(f"Timestamp: {timestamp_info['timestamp']}")
        print(f"TSA: {timestamp_info['tsa']}")
        print(f"\nLegal Significance:")
        print("  - Proves document existed at specific time")
        print("  - Required for certain legal documents in India")
        print("  - Strengthens non-repudiation")
        
        return timestamp_info
