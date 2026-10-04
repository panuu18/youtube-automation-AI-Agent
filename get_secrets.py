import base64
import os

def encode_file(filepath):
    if not os.path.exists(filepath):
        return "FILE NOT FOUND"
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

print("\n" + "="*50)
print("🔐 YOUR SECRETS FOR GITHUB ACTIONS 🔐")
print("="*50 + "\n")

print("1️⃣ SECRET NAME: CLIENT_SECRET_B64")
print("SECRET VALUE:")
print(encode_file("client_secret.json"))
print("\n" + "-"*50 + "\n")

print("2️⃣ SECRET NAME: TOKEN_PICKLE_B64")
print("SECRET VALUE:")
print(encode_file("token.pickle"))
print("\n" + "="*50)
