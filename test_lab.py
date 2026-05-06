import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secure_project.settings")
django.setup()

from payments.models import SecurePayment
from django.contrib.auth.models import User

def test_encryption():
    print("--- Testing Data Encryption ---")
    payment = SecurePayment(user_id=1)
    payment.set_card_data("4111-1111-1111-1111")
    payment.save()
    
    # Retrieve from DB
    saved_payment = SecurePayment.objects.get(user_id=1)
    print(f"Encrypted Data stored in DB: {saved_payment.encrypted_card_data}")
    
    # Decrypt
    decrypted_card = saved_payment.get_card_data()
    print(f"Decrypted Data: {decrypted_card}")

    # Test Invalid Encrypted Payload
    print("\n--- Testing Invalid Encrypted Payloads ---")
    try:
        saved_payment.encrypted_card_data = b"invalid_data_here"
        saved_payment.get_card_data()
    except Exception as e:
        print(f"Caught expected error when decrypting invalid payload: {e}")

def test_password_hashing():
    print("\n--- Testing Password Hashing ---")
    # Create user with password to test Argon2 hashing
    if not User.objects.filter(username="testuser").exists():
        user = User.objects.create_user(username="testuser", password="mysecretpassword")
    else:
        user = User.objects.get(username="testuser")
        
    print(f"Password hash stored in DB: {user.password}")
    print(f"Is hash Argon2? {'Yes' if user.password.startswith('argon2') else 'No'}")

if __name__ == "__main__":
    test_encryption()
    test_password_hashing()
