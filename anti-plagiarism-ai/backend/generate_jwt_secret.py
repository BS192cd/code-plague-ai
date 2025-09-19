#!/usr/bin/env python3
"""
Generate a secure JWT secret for the Anti-Plagiarism AI system.
Run this script once to generate a secure secret key.
"""

import secrets

def generate_jwt_secret():
    """Generate a secure JWT secret"""
    secret = secrets.token_urlsafe(32)
    print("Generated JWT Secret:")
    print(f"JWT_SECRET={secret}")
    print()
    print("Copy this line into your backend/.env file")
    print("Replace 'your_generated_secret_here' with the generated secret above")
    return secret

if __name__ == "__main__":
    generate_jwt_secret()