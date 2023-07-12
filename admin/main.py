from password_generator import PasswordGenerator


pwo = PasswordGenerator()
pwo.minlen = 8
pwo.maxlen = 16
pwo.minuchars = 3
pwo.minnumbers = 2
pwo.minschars = 1


def generate_key():
    token = pwo.generate()
    return token

