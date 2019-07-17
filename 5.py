from Cryptodome.Cipher import AES
from Cryptodome import Random
from binascii import b2a_hex

data = '鹿死谁手'
key = b'this is a 16 key'
iv = Random.new().read(AES.block_size)
mycipher = AES.new(key, AES.MODE_CFB,iv)
ciphertext = iv + mycipher.encrypt(data.encode())
mydecrypt = AES.new(key,AES.MODE_CFB,ciphertext[:16])
decrypttext = mydecrypt.decrypt(ciphertext[16:])

print('秘钥：',key)
print('iv:',b2a_hex(ciphertext)[:16])
print('加密',b2a_hex(ciphertext)[16:])
print('解密',decrypttext.decode())