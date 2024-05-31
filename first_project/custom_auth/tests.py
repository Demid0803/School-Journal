from django.test import TestCase

import hashlib
from datetime import datetime


hash_str = hashlib.sha256(b"qwerty123")
print(hash_str.hexdigest())
token_str = f"khvostov.demid@mail.ru.{hash_str.hexdigest()}.{str(datetime.now())}"
print(token_str)
token = hashlib.sha512(token_str.encode())
print(token.hexdigest())