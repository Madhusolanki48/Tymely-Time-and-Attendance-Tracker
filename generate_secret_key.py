#!/usr/bin/env python
"""
Script to generate a new Django secret key
"""
from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("="*50)
    print("NEW DJANGO SECRET KEY:")
    print("="*50)
    print(secret_key)
    print("="*50)
    print("Copy this key to your .env file as SECRET_KEY=...")
    print("="*50)
