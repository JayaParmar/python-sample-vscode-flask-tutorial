from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

public_key = private_key.public_key()

subject = x509.Name([
    x509.NameAttribute(x509.NameOID.COMMON_NAME, u"new_orion"),
])

certificate = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    subject
).public_key(
    public_key
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).sign(private_key, hashes.SHA256(), default_backend())

with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("certificate.pem", "wb") as f:
    f.write(certificate.public_bytes(serialization.Encoding.PEM))
