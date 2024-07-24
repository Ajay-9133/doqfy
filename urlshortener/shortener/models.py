from django.db import models
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from cryptography.fernet import Fernet

class URL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)

class Snippet(models.Model):
    text = models.TextField()
    key = models.CharField(max_length=44, blank=True)

    def encrypt_text(self, text, key):
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(text.encode()).decode()

    def decrypt_text(self, text, key):
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(text.encode()).decode()

    def save(self, *args, **kwargs):
        if self.key:
            self.text = self.encrypt_text(self.text, self.key)
        super().save(*args, **kwargs)
