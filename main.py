#pip install pycryptodome
#pip install matplotlib
#pip install pybase64

from hashlib import md5
import matplotlib.pyplot as plt
import base64
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
import cv2 #για να τυπώσουμε την εικόνα με το matplotlib


BLOCK_SIZE = 16  # Bytes


def pad(s): #με την συνα΄ρτηση αυτή συμπληρώνουμε το μέγεθος (16bytes) των blocks με όσα 0 σε byte μορφή χρειάζεται.
    while len(s) % 16 != 0:
        s=s+b'0'
    return s

# unpad = lambda s: s[:-ord(s[len(s) - 1:])] Αν θέλαμε να κρυπτογραφήσουμε κείμενο, θα μπορούσαμε να κάνουμε unpadding με αυτό τον τρόπο


class AESc:


    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, data):
        data = pad(data)
        
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)
        
        
        return b64encode(cipher.encrypt(data))
    
    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)
        return (cipher.decrypt(enc)).rstrip(b'0') #αφαιρούμε τα μηδενικά που προσθέσαμε εξαρχής

    
    

img_path = input(r'Enter path of Image: ') #Εισαγάγω το αρχείο


with open(img_path, "rb") as image:
    msg = base64.b64encode(image.read())   #κάνουμε Base64 encoding, μετατρέπω την εικόνα σε bytes                        
                                           #It accepts a bytes-like object and returns the Base64 encoded bytes 
#print(msg)
  

pwd = input('Password..: ')


encr=AESc(pwd).encrypt(msg) #Αυτό μου δίνει το περιεχόμενο της κρυπτογραφησης του περιεχομένου της εικόνας

#------------------------------------------------------------------------------------
with open(img_path, "wb") as image:
    
    image.write(encr) #αλλάζω το περιεχόμενο αντικαθιστώντας το με το encrypted κείμενο
#------------------------------------------------------------------------------------

print("Encryption done!\n")

while True:
    dresponse=input("Do you want to decrypt it? (answer: YES or NO) \n \n")
    
    if dresponse !="YES" and dresponse != "NO": 
    
        print("Invalid option \n \n")
    
        continue
    
    elif dresponse =="NO":
        break
        
    else:
        decr=AESc(pwd).decrypt(encr)
        
        fh = open("random.jpg", "wb")
        
        #print(type(decr),decr)
        
        fh.write(base64.decodebytes(decr))  #https://www.programcreek.com/2013/09/convert-image-to-string-in-python/
        
        fh.close()
        
        print("\n Decryption done!\n \n")

        
        break
        
print("\n Your image has been decrypted! \n")       
my_img = cv2.imread("random.jpg")
plt.imshow(my_img)
plt.show()
