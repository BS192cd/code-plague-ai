#!/usr/bin/env python3
"""
Test JWT configuration for Anti-Plagiarism AI
"""

import sys
import os
sys.path.append('backend')

def test_jwt_setup():
    """Test JWT configuration and token generation"""
    print("🔑 Testing JWT Setup...")
    
    try:
        # Test configuration loading
        from app.core.config import settings, validate_settings
        print(f"✅ Configuration loaded successfully")
        print(f"   JWT_SECRET: {settings.JWT_SECRET[:10]}... (truncated)")
        print(f"   JWT_ALGORITHM: {settings.JWT_ALGORITHM}")
        print(f"   ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
        
        # Validate configuration
        validate_settings()
        print("✅ Configuration validation passed")
        
        # Test JWT token creation
        from app.auth import create_access_token
        from datetime import timedelta
        
        test_data = {
            "sub": "test_user",
            "user_id": "test_id_123",
            "role": "student"
        }
        
        token = create_access_token(
            data=test_data,
            expires_delta=timedelta(minutes=30)
        )
        
        print("✅ JWT token created successfully")
        print(f"   Token: {token[:20]}... (truncated)")
        
        # Test JWT token verification
        from app.auth import verify_token
        
        token_data = verify_token(token)
        print("✅ JWT token verified successfully")
        print(f"   Username: {token_data.username}")
        print(f"   User ID: {token_data.user_id}")
        print(f"   Role: {token_data.role}")
        
        # Test password hashing
        from app.auth import get_password_hash, verify_password
        
        test_password = "test_password_123"
        hashed = get_password_hash(test_password)
        
        print("✅ Password hashing works")
        print(f"   Original: {test_password}")
        print(f"   Hashed: {hashed[:20]}... (truncated)")
        
        # Test password verification
        is_valid = verify_password(test_password, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        print("\n🎉 All JWT tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ JWT test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_jwt_setup()
    sys.exit(0 if success else 1)