#!/usr/bin/env python3
"""
Certificate Viewer Utility

This script allows you to view details of generated certificates
using OpenSSL commands.
"""

import subprocess
import os


def view_certificate(cert_path):
    """View certificate details using OpenSSL"""
    if not os.path.exists(cert_path):
        print(f"❌ Certificate not found: {cert_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"Certificate: {cert_path}")
    print(f"{'='*70}\n")
    
    # View certificate in text format
    cmd = f"openssl x509 -in {cert_path} -text -noout"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
    except Exception as e:
        print(f"❌ Error viewing certificate: {e}")
        print("\n💡 Alternative: Using Python to read certificate")
        
        # Fallback to Python
        import sys
        sys.path.insert(0, 'src')
        from digital_certificate import DigitalCertificate
        cert = DigitalCertificate.load_certificate_from_file(cert_path)
        DigitalCertificate.display_certificate_info(cert)


def view_certificate_fingerprint(cert_path):
    """View certificate fingerprint"""
    if not os.path.exists(cert_path):
        return
    
    print(f"\nFingerprints for: {cert_path}")
    print("-" * 70)
    
    # SHA-256 fingerprint
    cmd = f"openssl x509 -in {cert_path} -fingerprint -sha256 -noout"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"SHA-256: {result.stdout.strip()}")
    except:
        pass
    
    # SHA-1 fingerprint
    cmd = f"openssl x509 -in {cert_path} -fingerprint -sha1 -noout"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"SHA-1:   {result.stdout.strip()}")
    except:
        pass


def main():
    print("="*70)
    print("PKI Certificate Viewer")
    print("="*70)
    
    cert_dir = "certificates"
    
    # List available certificates
    print("\nAvailable Certificates:")
    certs = []
    if os.path.exists(cert_dir):
        for f in os.listdir(cert_dir):
            if f.endswith('.pem') and 'key' not in f.lower():
                certs.append(os.path.join(cert_dir, f))
                print(f"  • {f}")
    
    if not certs:
        print("  No certificates found. Run main.py first!")
        return
    
    print("\n" + "="*70)
    
    # View each certificate
    for cert in certs:
        view_certificate(cert)
        view_certificate_fingerprint(cert)
        print("\n" + "="*70)
    
    print("\n✅ Certificate viewing complete!")


if __name__ == "__main__":
    main()
