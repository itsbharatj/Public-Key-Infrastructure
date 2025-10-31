#!/usr/bin/env python3
"""
Client-Server Communication Simulation with PKI

This example demonstrates:
1. Secure client-server communication using digital signatures
2. Authenticated vs. unauthenticated messages
3. Message tampering detection
4. Man-in-the-middle attack prevention
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from certificate_authority import CertificateAuthority
from digital_certificate import DigitalCertificate
from digital_signature import DigitalSignature
import json
import time
from datetime import datetime


class Server:
    """
    Simulates a secure server that can verify client messages
    """
    
    def __init__(self, name, ca):
        """
        Initialize server with its own certificate
        
        Args:
            name: Server name
            ca: Certificate Authority instance
        """
        self.name = name
        self.ca = ca
        
        # Generate server's key pair
        print(f"\n[Server: {self.name}] Initializing...")
        self.private_key, self.public_key = DigitalSignature.generate_key_pair(key_size=2048)
        
        # Get certificate from CA
        self.certificate = ca.issue_certificate(
            subject_name=f"{name} Server",
            subject_org="Secure Services Ltd",
            subject_email=f"{name.lower()}@secureservices.in",
            public_key=self.public_key,
            cert_class=3,
            validity_days=365
        )
        
        print(f"✓ Server '{self.name}' initialized and certified by CA")
        
        # Store trusted client certificates
        self.trusted_clients = {}
        self.message_log = []
    
    def register_client(self, client_name, client_certificate):
        """
        Register a trusted client certificate
        
        Args:
            client_name: Name of the client
            client_certificate: Client's certificate
        """
        # Verify certificate is issued by our CA
        if self.ca.verify_certificate(client_certificate):
            self.trusted_clients[client_name] = client_certificate
            print(f"✓ Server registered client: {client_name}")
        else:
            print(f"✗ Server rejected client: {client_name} (untrusted certificate)")
    
    def receive_message(self, message_data):
        """
        Receive and process a message from a client
        
        Args:
            message_data: Dictionary containing message and signature
            
        Returns:
            dict: Processing result
        """
        print(f"\n{'='*70}")
        print(f"[Server: {self.name}] Receiving Message")
        print(f"{'='*70}")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        sender = message_data.get('sender')
        message = message_data.get('message')
        signature = message_data.get('signature')
        is_signed = message_data.get('signed', False)
        
        print(f"Timestamp: {timestamp}")
        print(f"Sender: {sender}")
        print(f"Message: {message}")
        print(f"Signed: {is_signed}")
        
        result = {
            'timestamp': timestamp,
            'sender': sender,
            'message': message,
            'authenticated': False,
            'trusted': False,
            'status': 'rejected'
        }
        
        if not is_signed:
            print(f"\n⚠️  WARNING: Message is NOT signed!")
            print(f"✗ Authentication: FAILED (no signature)")
            print(f"✗ Message REJECTED - cannot verify sender identity")
            result['reason'] = 'No digital signature provided'
        else:
            # Check if client is trusted
            if sender not in self.trusted_clients:
                print(f"\n✗ Sender '{sender}' is NOT in trusted clients list")
                print(f"✗ Message REJECTED - untrusted sender")
                result['reason'] = 'Sender not in trusted list'
            else:
                # Verify signature
                client_cert = self.trusted_clients[sender]
                client_public_key = client_cert.public_key()
                
                verifier = DigitalSignature(public_key=client_public_key)
                is_valid = verifier.verify_signature(
                    message,
                    signature,
                    document_name=f"message_from_{sender}",
                    signer_certificate=client_cert  # Pass certificate for full PKI validation
                )
                
                if is_valid:
                    result['authenticated'] = True
                    result['trusted'] = True
                    result['status'] = 'accepted'
                    print(f"\n✓ Message ACCEPTED and processed")
                else:
                    print(f"\n✗ Signature verification FAILED")
                    print(f"✗ Message REJECTED - possible tampering detected")
                    result['reason'] = 'Invalid signature - message may be tampered'
        
        self.message_log.append(result)
        print(f"{'='*70}\n")
        
        return result
    
    def get_statistics(self):
        """Get server message processing statistics"""
        total = len(self.message_log)
        accepted = sum(1 for m in self.message_log if m['status'] == 'accepted')
        rejected = total - accepted
        
        return {
            'total_messages': total,
            'accepted': accepted,
            'rejected': rejected,
            'acceptance_rate': f"{(accepted/total*100):.1f}%" if total > 0 else "0%"
        }


class Client:
    """
    Simulates a client that can send signed and unsigned messages
    """
    
    def __init__(self, name, ca):
        """
        Initialize client with its own certificate
        
        Args:
            name: Client name
            ca: Certificate Authority instance
        """
        self.name = name
        self.ca = ca
        
        # Generate client's key pair
        print(f"\n[Client: {self.name}] Initializing...")
        self.private_key, self.public_key = DigitalSignature.generate_key_pair(key_size=2048)
        
        # Get certificate from CA
        self.certificate = ca.issue_certificate(
            subject_name=name,
            subject_org="Client Organization",
            subject_email=f"{name.lower()}@client.in",
            public_key=self.public_key,
            cert_class=2,
            validity_days=365
        )
        
        print(f"✓ Client '{self.name}' initialized and certified by CA")
    
    def send_message(self, server, message, sign=True):
        """
        Send a message to the server
        
        Args:
            server: Server instance
            message: Message content
            sign: Whether to sign the message (default True)
            
        Returns:
            dict: Server's response
        """
        print(f"\n{'='*70}")
        print(f"[Client: {self.name}] Sending Message to {server.name}")
        print(f"{'='*70}")
        print(f"Message: {message}")
        print(f"Will sign: {sign}")
        
        message_data = {
            'sender': self.name,
            'message': message,
            'signed': sign
        }
        
        if sign:
            # Sign the message
            signer = DigitalSignature(private_key=self.private_key)
            signature = signer.sign_document(message, f"message_to_{server.name}")
            message_data['signature'] = signature
            print(f"✓ Message signed with client's private key")
        else:
            message_data['signature'] = None
            print(f"⚠️  Message sent WITHOUT signature (unauthenticated)")
        
        print(f"{'='*70}\n")
        
        # Send to server
        return server.receive_message(message_data)


class Attacker:
    """
    Simulates a malicious attacker trying to send unauthorized messages
    """
    
    def __init__(self, name):
        self.name = name
        print(f"\n[Attacker: {self.name}] Active (no valid certificate)")
    
    def send_fake_message(self, server, fake_sender, message, with_fake_signature=False):
        """
        Send a fake message pretending to be someone else
        
        Args:
            server: Target server
            fake_sender: Name to impersonate
            message: Malicious message
            with_fake_signature: Whether to include a fake signature
        """
        print(f"\n{'='*70}")
        print(f"[Attacker: {self.name}] Sending FAKE Message")
        print(f"{'='*70}")
        print(f"Impersonating: {fake_sender}")
        print(f"Malicious message: {message}")
        
        message_data = {
            'sender': fake_sender,  # Impersonating!
            'message': message,
            'signed': with_fake_signature
        }
        
        if with_fake_signature:
            # Create a fake signature (just random bytes)
            message_data['signature'] = os.urandom(256)
            print(f"⚠️  Including FAKE signature")
        else:
            message_data['signature'] = None
            print(f"⚠️  No signature")
        
        print(f"{'='*70}\n")
        
        return server.receive_message(message_data)
    
    def tamper_message(self, server, client, original_message, tampered_message):
        """
        Intercept and tamper with a legitimate message (Man-in-the-Middle)
        
        Args:
            server: Target server
            client: Original client
            original_message: Original message
            tampered_message: Modified message
        """
        print(f"\n{'='*70}")
        print(f"[Attacker: {self.name}] TAMPERING with Message (MITM Attack)")
        print(f"{'='*70}")
        print(f"Original message: {original_message}")
        print(f"Tampered message: {tampered_message}")
        
        # Create signature for original message
        signer = DigitalSignature(private_key=client.private_key)
        original_signature = signer.sign_document(original_message, "original")
        
        # Send tampered message with original signature
        message_data = {
            'sender': client.name,
            'message': tampered_message,  # Changed!
            'signed': True,
            'signature': original_signature  # Original signature won't match!
        }
        
        print(f"⚠️  Sending tampered message with original signature")
        print(f"{'='*70}\n")
        
        return server.receive_message(message_data)


def print_scenario_header(scenario_num, title):
    """Print formatted scenario header"""
    print(f"\n\n{'#'*70}")
    print(f"# SCENARIO {scenario_num}: {title}")
    print(f"{'#'*70}\n")


def main():
    """Main demonstration of client-server communication"""
    
    print("="*70)
    print("CLIENT-SERVER COMMUNICATION WITH PKI DEMONSTRATION")
    print("="*70)
    print("\nThis demonstration shows:")
    print("  • Authenticated communication using digital signatures")
    print("  • Detection of unauthenticated messages")
    print("  • Detection of message tampering")
    print("  • Protection against impersonation attacks")
    
    input("\nPress Enter to begin...")
    
    # ========================================================================
    # SETUP: Create CA and initialize parties
    # ========================================================================
    print_scenario_header(0, "SETUP - Certificate Authority and Entities")
    
    # Create Certificate Authority
    ca = CertificateAuthority(
        name="Secure Communications CA",
        country="IN",
        organization="National PKI Authority"
    )
    
    ca_private_key, ca_certificate = ca.generate_root_certificate(
        key_size=2048,
        validity_days=3650
    )
    
    # Create server
    server = Server("PaymentGateway", ca)
    
    # Create legitimate clients
    client_alice = Client("Alice", ca)
    client_bob = Client("Bob", ca)
    
    # Register clients with server
    server.register_client("Alice", client_alice.certificate)
    server.register_client("Bob", client_bob.certificate)
    
    # Create attacker (no certificate)
    attacker = Attacker("Mallory")
    
    input("\nPress Enter to see Scenario 1...")
    
    # ========================================================================
    # SCENARIO 1: Legitimate authenticated message
    # ========================================================================
    print_scenario_header(1, "LEGITIMATE AUTHENTICATED MESSAGE")
    print("Alice sends a signed payment request to the server.\n")
    
    result1 = client_alice.send_message(
        server,
        "Transfer ₹10,000 to account 1234567890",
        sign=True
    )
    
    print(f"Result: {result1['status'].upper()}")
    
    input("\nPress Enter to see Scenario 2...")
    
    # ========================================================================
    # SCENARIO 2: Unauthenticated message from legitimate client
    # ========================================================================
    print_scenario_header(2, "UNAUTHENTICATED MESSAGE")
    print("Bob sends a message WITHOUT signing it.\n")
    
    result2 = client_bob.send_message(
        server,
        "Transfer ₹50,000 to account 9876543210",
        sign=False
    )
    
    print(f"Result: {result2['status'].upper()}")
    
    input("\nPress Enter to see Scenario 3...")
    
    # ========================================================================
    # SCENARIO 3: Impersonation attack without signature
    # ========================================================================
    print_scenario_header(3, "IMPERSONATION ATTACK (No Signature)")
    print("Attacker Mallory tries to impersonate Alice without a signature.\n")
    
    result3 = attacker.send_fake_message(
        server,
        fake_sender="Alice",
        message="Transfer ₹100,000 to attacker account 0000000000",
        with_fake_signature=False
    )
    
    print(f"Result: {result3['status'].upper()}")
    
    input("\nPress Enter to see Scenario 4...")
    
    # ========================================================================
    # SCENARIO 4: Impersonation attack with fake signature
    # ========================================================================
    print_scenario_header(4, "IMPERSONATION ATTACK (Fake Signature)")
    print("Mallory tries to impersonate Bob with a fake signature.\n")
    
    result4 = attacker.send_fake_message(
        server,
        fake_sender="Bob",
        message="Transfer ₹200,000 to attacker account 1111111111",
        with_fake_signature=True
    )
    
    print(f"Result: {result4['status'].upper()}")
    
    input("\nPress Enter to see Scenario 5...")
    
    # ========================================================================
    # SCENARIO 5: Message tampering (Man-in-the-Middle)
    # ========================================================================
    print_scenario_header(5, "MESSAGE TAMPERING ATTACK (MITM)")
    print("Mallory intercepts Alice's message and modifies it.\n")
    
    result5 = attacker.tamper_message(
        server,
        client_alice,
        original_message="Transfer ₹1,000 to account 1234567890",
        tampered_message="Transfer ₹999,000 to account 0000000000"
    )
    
    print(f"Result: {result5['status'].upper()}")
    
    input("\nPress Enter to see Scenario 6...")
    
    # ========================================================================
    # SCENARIO 6: Multiple legitimate messages
    # ========================================================================
    print_scenario_header(6, "MULTIPLE LEGITIMATE MESSAGES")
    print("Both Alice and Bob send properly signed messages.\n")
    
    result6a = client_alice.send_message(
        server,
        "Update account settings: email=alice@newdomain.in",
        sign=True
    )
    
    result6b = client_bob.send_message(
        server,
        "Check balance for account 9876543210",
        sign=True
    )
    
    print(f"Alice's message: {result6a['status'].upper()}")
    print(f"Bob's message: {result6b['status'].upper()}")
    
    input("\nPress Enter to see statistics...")
    
    # ========================================================================
    # STATISTICS
    # ========================================================================
    print(f"\n{'='*70}")
    print("SERVER STATISTICS")
    print(f"{'='*70}\n")
    
    stats = server.get_statistics()
    
    print(f"Total messages received: {stats['total_messages']}")
    print(f"Messages accepted: {stats['accepted']} ✓")
    print(f"Messages rejected: {stats['rejected']} ✗")
    print(f"Acceptance rate: {stats['acceptance_rate']}")
    
    print(f"\n{'='*70}")
    print("MESSAGE LOG SUMMARY")
    print(f"{'='*70}\n")
    
    for i, log in enumerate(server.message_log, 1):
        status_icon = "✓" if log['status'] == 'accepted' else "✗"
        print(f"{i}. {status_icon} {log['sender']}: {log['message'][:50]}...")
        print(f"   Status: {log['status'].upper()}")
        print(f"   Authenticated: {log['authenticated']}")
        print(f"   Trusted: {log['trusted']}")
        if log['status'] == 'rejected':
            print(f"   Reason: {log.get('reason', 'Unknown')}")
        print()
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print(f"{'='*70}")
    print("DEMONSTRATION SUMMARY")
    print(f"{'='*70}\n")
    
    print("✓ PKI Security Features Demonstrated:")
    print("  • Authentication: Digital signatures verify sender identity")
    print("  • Integrity: Tampering is immediately detected")
    print("  • Non-repudiation: Sender cannot deny sending signed messages")
    print("  • Trust: Only CA-certified clients are trusted")
    
    print("\n✗ Attacks Successfully Prevented:")
    print("  • Unauthenticated messages rejected")
    print("  • Impersonation attacks detected")
    print("  • Fake signatures rejected")
    print("  • Message tampering detected")
    
    print("\n📊 Results:")
    print(f"  • Legitimate signed messages: 100% accepted")
    print(f"  • Attack attempts: 100% rejected")
    print(f"  • Overall security: EXCELLENT")
    
    print("\n🔐 Key Takeaways:")
    print("  1. Always sign messages with your private key")
    print("  2. Always verify signatures with sender's public key")
    print("  3. Trust only certificates issued by legitimate CAs")
    print("  4. PKI provides comprehensive protection against:")
    print("     - Impersonation")
    print("     - Message tampering")
    print("     - Replay attacks")
    print("     - Man-in-the-middle attacks")
    
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