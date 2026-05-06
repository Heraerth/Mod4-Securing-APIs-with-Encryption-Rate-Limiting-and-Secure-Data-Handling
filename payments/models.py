from django.db import models
from cryptography.fernet import Fernet

ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

class SecurePayment(models.Model):
    user_id = models.IntegerField()
    encrypted_card_data = models.BinaryField()

    def set_card_data(self, raw_card_number):
        """Encrypts the card number before saving"""
        self.encrypted_card_data = cipher.encrypt(raw_card_number.encode('utf-8'))

    def get_card_data(self):
        """Decrypts the card number when retrieved"""
        return cipher.decrypt(self.encrypted_card_data).decode('utf-8')