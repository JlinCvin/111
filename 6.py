import rsa
import binascii
def rsa_encrypt(rsa_n,rsa_e, message):
    key = rsa.Publickey(rsa_n,rsa_e)
    message = rsa.encrypt(message.encode(),key)
    message = binascii.b2a_hex(message)
    return message.decode()
pubkey_n = '8d7e6949d411ce14d7d233d7160f5b2cc753930caba4d5ad24f923a505253b9c39b09a059732250e56c594d735077cfcb0c3508e9f544f101bdf7e97fe1b0d97f273468264b8b24caaa2a90cd9708a417c51cf8ba35444d37c514a0490441a773ccb121034f29748763c6c4f76eb0303559c57071fd89234d140c8bb965f9725'
pubkey_e = '10001'
rsa_n = int(pubkey_n,16)
rsa_e = int(pubkey_e,16)
message='鹿死谁手'

print('公钥N长度',len(pubkey_n))
print(rsa_encrypt((rsa_n,rsa_e,message)))
