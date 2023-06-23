import random
import math

class Affine:

    # This is the encrypt method where the encryption of the message takes place
    # The formula f( p) = (ap + b) mod 128 will be used where a is the primary key and b is the secondary key
    def getKey(self): #return a randomly generated keys
        primary = random.randint(1,100)
        secondary = random.randint(1,100)
        if self.gcd(primary) == 1:
            return  (primary,secondary)
        else:
            return self.getKey()
    
    def choose_key(self): # write key to a file
        try:
            primary,secondary = self.getKey()
            with open('affine_key.txt' , 'w') as file:
                file.write(str(primary) + '\n')
                file.write(str(secondary))
            file.close()
        except:
            print("error occured while writing to file")
            return None



    def encrypt(self, message_path , key_file = 'affine_key.txt'):
        
        
        try:
            with open(key_file , 'r') as file:
                primary = int(file.readline())
                secondary = int(file.readline())
            file.close()
        except FileNotFoundError:
            print("key file not found")
            return None
                

        cipher_text_path = message_path.split('.')[0] + '_affine_cipher.txt'   

        try:
            with open(message_path , 'r') as file:
                message = file.read()
            file.close()
        except FileNotFoundError:
            print("message file not found")
            return None

        cipher_text = ""
        for x in message:
                
            value1 = primary * ord(x) + secondary

            value2 = value1 % 128
            cipher_text = cipher_text + chr(value2)
       
        with open(cipher_text_path , 'w') as file:
            file.write(cipher_text)
        file.close()
        
        

    # This is the decrypt method where a cipher_text is decrypted
    def decrypt(self, cipher_text_path, key_file = 'affine_key.txt'):

        with open(key_file , 'r') as file:
            primary = int(file.readline())
            secondary = int(file.readline())
        
        message = ""
        try:
            with open(cipher_text_path , 'r') as file:
                cipher_text = file.read()
            file.close()
        except FileNotFoundError:
            print("cipher text file not found")
            return None
        
        message_path = cipher_text_path.split('_')[0] + '_affine_message.txt'

        for x in cipher_text:

            value1 = self.inverse_mode(primary) * (ord(x) - secondary)

            value2 = value1 % 128
            message = message + chr(value2)

        try:
            with open(message_path , 'w') as file:
                file.write(message)
            file.close()
        except:
            print("error occured while writing to file")
            return None

    def gcd(self, y, x = 128):  # This method is used to calculate the gcd of 128 and the primary key

        if x == 0:
            return y

        else:
            return self.gcd(x, y % x)

    def inverse_mode(self, primary):  # This method is used to find the inverse of the primary key
        for x in range(128):
            if ((x * primary) % 128) == 1:
                return x

# ***************************************************************************************************************************


class Transposition:

    #given the value for m, it find the mapping function from {1,2,3,...,m} to itself
    def choose_key(self, message_length):
        m = self.choose_m(message_length)
        mapping = self.sigma_function(m)
        try:
            with open('transposition_key.txt' , 'w') as file:
                for key, value in mapping.items():
                    file.write(str(key) + ' ' + str(value) + '\n')
            file.close()
        except:
            print("error occured while writing to file")
            return None

    def choose_m(self, message_length):
        if message_length > 100:
            min_m = 5
            max_m = message_length // 5
        elif message_length < 10:
            min_m = 2
            max_m = 5
        else:
            min_m = 4
            max_m = message_length // 3

        random_m = random.randint(min_m, max_m)

        return random_m

    def sigma_function(self,m):
        _set= list(range(1,m+1)) #generate list of numbers from 1 to m....{1,2,3....m}
        permutation=random.sample(_set,m) #permutuate the elements of the list , _set
   
        mapping={}  #we used dictionary(hash map) to  store the mapping which gives sigma function required
        #loops through the elements of _set and assign a value from the permutuation
        #store the result in the hash map
        for key , value in zip(_set,permutation):
            mapping[key]=value

        return mapping
    #find the inverse function or mapping given the function(dictionary)
    def inverse_sigma(self,mapping):
        inverse = {} #stores the inverse mapping
        #loop through the key of the mapping.....the x value of the function
        #find the value corresponding to the keys....find y value of the function
        #swap the two,key and value, and store the result in the inverse mapping
        for key, value in mapping.items():

            inverse[value] = key
            
        return inverse
    #take a message and m value(block_size) as input
    #find the mapping function which is random
    #returns the encrypted message and the mapping function used

    def transform(self , text , mapping):

        new_text = [0 for i in range(len(text))]

        for key, value in mapping.items():
            new_text[value - 1] = text[key - 1]
        
        return new_text
    
    def make_divisible_by_m(self,message,m):

        
        while len(message) % m != 0: #check whether the message length is divisible by m

            message += "#" #if not add x to the message

     
        i = 0
        block = ''
        message_block = []

        while i < len(message):
            
            block += message[i]

            if len(block) == m:
                message_block.append(block)
                block = ''

            i += 1
        
        return message_block

    
    def encrypt(self , message_path , key_file = 'transposition_key.txt'):

        try:
            with open(key_file , 'r') as file:
                mapping = {}
                for line in file:
                    key, value = line.split()
                    mapping[int(key)] = int(value)
            file.close()
        except FileNotFoundError:
            print("key file not found")
            return None

        try:
            with open(message_path , 'r') as file:
                message = file.read()
            file.close()
        except FileNotFoundError:
            print("message file not found")
            return None

        m = len(mapping) #get the m value from the mapping function

        message_block = self.make_divisible_by_m(message , m) #make the message divisible by m
       
        ciphter_text_path = message_path.split('.')[0] + '_transposition_cipher.txt'

        cipher_text = ''

        for block in message_block:
            cipher_text += ''.join(self.transform(list(block), mapping))
        
        try:
            with open(ciphter_text_path , 'w') as file:
                file.write(cipher_text)
            file.close()
        except:
            print("error occured while writing to file")
            return None


        
        
        

    #given cipher_text and and a mapping function used to encrypt the message
    #return the original value
    def decrypt(self , cipher_text_path , key_file = 'transposition_key.txt'):
        try:
            with open(key_file , 'r') as file:
                mapping = {}
                for line in file:
                    key, value = line.split()
                    mapping[int(key)] = int(value)
            file.close()
        except FileNotFoundError:
            print("key file not found")
            return None

        try:
            with open(cipher_text_path , 'r') as file:
                cipher_text = file.read()
            file.close()
        except FileNotFoundError:
            print("cipher text file not found")
            return None
        
        m = len(mapping) #get the m value from the mapping function
        inverse_mapping = self.inverse_sigma(mapping) #find the inverse mapping of the mapping function used to encrypt the message
        
        message = ''

        message_path = cipher_text_path.split('_')[0] + '_transposition_message.txt'
        cipher_text = self.make_divisible_by_m(cipher_text , m) #make the cipher text divisible by m

        for block in cipher_text:
             
            message += ''.join(self.transform(list(block), inverse_mapping))
       

        try:
            with open(message_path , 'w') as file:
                file.write(message)
            file.close()
        except:
            print("error occured while writing to file")
            return None

#******************************************************************************************************************************************************


class RSA:
    
    def choose_key(self):
        try:
            p = self.Prime_generator()
            q = self.Prime_generator()
            while p == q:
                q = self.Prime_generator()
            N, e = self.get_public_Keys(p, q)
            with open('public_rsa_key.txt', 'w') as file:
                file.write(str(N) + '\n')
                file.write(str(e))
            file.close()
            phi = (p - 1) * (q - 1)
            d = self.inverse_mode(e, phi)
            with open('private_rsa_key.txt', 'w') as file:
                file.write(str(N) + '\n')
                file.write(str(d))
            file.close()
        except:
            print("error occured while writing to file")
            return None
            

    def gcd(self, y, x):  # find the gcd of two numbers
        if x == 0:
            return y
        else:
            return self.gcd(x, y % x)

    def Prime_generator(self): #generate a random prime from range 100-999
        prime = random.randint(100,999)
        while True:
            isprime = True

            for x in range(2, int(math.sqrt(prime) + 1)):
                if prime % x == 0:
                    isprime = False
                    break 

            if isprime:
                return prime

            prime += 1
    def get_public_Keys(self, p , q):

        N = p * q
        phi = (p-1)*(q-1)
        e=2
        for i in range(3,phi):
            if self.gcd(i,phi) == 1:
                e = i
        return N,e


    # convert a given message into blocks of integer
    # based on the given N value which is the product of two large primes
    def chunks(self, message):
        Integer_representation = [] # store the integer representation of the message
        for char in message:
            num_char = ord(char)

            Integer_representation.append(str(num_char))
        return Integer_representation

    # based on the value of given number
    # return the required block size
    def find_block_length(self, number):
        if len(str(number)) <= 2:
            return 2
        smallest_block = "25"
        count = 0
        while int(smallest_block) < number:
            count += 2
            smallest_block += "25"
        return count

    # returns the bit String representation of a given number
    def binary_converter(self, number):
        return bin(number).replace("0b", "")

    # formula: (b^n)mod m
    # returns the the modulus of the above expression using
    # the algorithm of fast modular exponentiation
    def modular_exponentiation(self, b, n, m):
        n = list(self.binary_converter(n))  # we need the bit string representation of the exponent
        x = 1
        power = b % m
        for i in range(len(n) - 1, 0, -1):
            if int(n[i]) == 1:
                x = (x * power) % m
            power = (power ** 2) % m
        return (x * power) % m

    # takes a string message and a public key in the form of a tuple (N,e)
    # where N is the product of two prime numbers: p and q
    # e is relatively prime with the product (p-1)*(q-1)
    def encrypt(self, message_path, key_file = 'public_rsa_key.txt'):

        try:
            with open(key_file , 'r') as file:
                N = int(file.readline())
                e = int(file.readline())
            file.close()
        except FileNotFoundError:
            print("key file not found")
            return None

        try:
            with open(message_path , 'r') as file:
                message = file.read()
            file.close()
        except FileNotFoundError:
            print("message file not found")
            return None
        
        chunk = self.chunks(message)

        cipher_text_path = message_path.split('.')[0] + '_rsa_cipher.txt'
        cipher_text = ""  # stores the encrypted message

        for block in chunk:

            b = int(block)
            res = self.modular_exponentiation(b, e, N)
            cipher_text+=str(res)+" "
        try:
            with open(cipher_text_path , 'w') as file:
                file.write(cipher_text)
            file.close()
        except:
            print("error occured while writing to file")
            return None
        

    def inverse_mode(self, e, product):  # This method is used to find the inverse of e mod (p-1)*(q-1)
        for x in range(product):
            if (x * e % product) == 1:
                return x

    # receives a cipher_text in the form of chunks produced by encrpt method
    # two prime numbers must be provided
    # receive key as the tuple(N,e)
    # returns the decrypted message as a string

    def decrypt(self, cipher_text_path, key_file = 'private_rsa_key.txt'):
        try:
            with open(key_file , 'r') as file:
                N = int(file.readline())
                d = int(file.readline())
            file.close()
        except FileNotFoundError:
            print("key file not found")
            return None

        try:
            with open(cipher_text_path , 'r') as file:
                cipher_text = file.read()
            file.close()
        except FileNotFoundError:
            print("cipher text file not found")
            return None
        
        cipher_text = cipher_text.strip().split(" ")

        
        message = []  # stores the decrypted message
         # d is the inverse of e mod product (our private key) 
        for i in cipher_text:
            if i != "" and i != " ":
                b = int(i)
                # res stores the decrypted message block
                res = str(self.modular_exponentiation(b, d, N))# d is the decryption key
                message.append(res)
        
        message = self.Tostring(message)
        
        message_path = cipher_text_path.split('_')[0] + '_rsa_message.txt'
        try:
            with open(message_path , 'w') as file:
                file.write(message)
            file.close()
        except:
            print("error occured while writing to file")
            return None
    #return original message from the decrypted cipher
    def Tostring(self, sequence):
        res=""
        for m in sequence:
            val = int(m)
            res += chr(val)
        return res
    
    def sign(self,message_path,key_file = 'private_rsa_key.txt'):

        try:
            with open(key_file , 'r') as file:
                N = int(file.readline())
                d = int(file.readline())
            file.close()
        except FileNotFoundError:
            print("key file not found")
            return None
        
        try:
            with open(message_path , 'r') as file:
                message = file.read()
            file.close()
        except FileNotFoundError:
            print("message file not found")
            return None

        
        chunk = self.chunks(message)
        signature = ""

        signature_path = message_path.split('.')[0] + '_rsa_signature.txt'
        for block in chunk:    
            b = int(block)
            res = self.modular_exponentiation(b, d, N)
            signature += str(res) + " "
        
        try:
            with open(signature_path , 'w') as file:
                file.write(signature)
            file.close()
        except:
            print("error occured while writing to file")
            return None
    
    def verify(self,message_path ,signature_path,key_file = 'public_rsa_key.txt'):

        try:
            with open(key_file , 'r') as file:
                N = int(file.readline())
                e = int(file.readline())
            file.close()
        except FileNotFoundError:
            print("key file not found")
            return None

        try:
            with open(message_path , 'r') as file:
                message = file.read()
            file.close()
        except FileNotFoundError:
            print("message file not found")
            return None

        try:
            with open(signature_path , 'r') as file:
                signature = file.read()
            file.close()
        except FileNotFoundError:
            print("signature file not found")
            return None

        
        chunk = self.chunks(message)


        signature = signature.strip().split(" ")
        if len(chunk) != len(signature):
            return False
        
        for i in range(len(chunk)):
            if chunk[i] != "" and signature[i] != "":
                b = int(signature[i])
                res = self.modular_exponentiation(b, e, N)
                if res != int(chunk[i]):
                    return False
        return True
        
    









def main():
    if __name__== "__main__":

        while True:
            print("This programm has 3 cryptosystems \n 1. Affine \n 2. Transposition \n 3. RSA \n 4. Exit")
            try:
                cryptosystem = int(input("Enter the number of the cryptosystem you wish to use: "))
            except:
                print("invalid input, input should be 1,2,3 and 4")

            if cryptosystem == 1:
                
                while True:
                    print("list of operations that can be performed\n 1. Encryption \n 2.Decryption \n 3.Back")
                    try:
                        option = int(input("Enter your option: "))
                    except:
                        print("invalid input, input should be 1,2 or 3")
                 
                    if option == 1:
                        print("Enter the path of the message you want to encrypt")
                        message_path = input("message_path: ")
                        affine = Affine()
                        print('Do you want to use a randomly generated key? (y/n)')
                        choice = input('choice: ')
                        if choice == 'y':
                            affine.choose_key()
                        
                            affine.encrypt(message_path)
                            print('your encrypted message is in the file ending with _affine_cipher.txt')
                            
                            
                        elif choice == 'n':
                            print('enter the path of the key file')
                            key_file = input('key_file: ')
                            
                            affine.encrypt(message_path,key_file)
                            print('your encrypted message is in the file ending with _affine_cipher.txt')
                           
                        else:
                            print('invalid input')
                            

                        
                    elif option == 2:
                        affine = Affine()
                        key_file = input('enter the path of the key file: ')
                        print('enter the path of the cipher text file')
                        cipher_text_path = input('cipher_text_path: ')
                        
                       
                        affine.decrypt(cipher_text_path,key_file)
                        print('your decrypted message is in the file ending with _affine_message.txt')
                        
                        
                    elif option==3:
                        break
                    else:
                        print("option not available")
                    
            elif cryptosystem ==2:
                
                while True:
                    print("list of operations that can be performed\n 1. Encryption \n 2.Decryption \n 3.Back")
                    try:
                        option = int(input("Enter your option: "))
                    except:
                        print("invalid input, input shoud be 1,2 or 3")
                    if option == 1:
                        
                        print("Enter the path of the message you want to encrypt")
                        message_path = input("message_path: ")
                        
                        chioce = input("Do you want to use a randomly generated key? (y/n): ")
                        if chioce == 'y':
                            transpose = Transposition()
                            try:
                                with open(message_path , 'r') as file:
                                    message = file.read()
                                file.close()
                            except FileNotFoundError:
                                print("message file not found")
                                return None
                            
                            m = len(message)
                            transpose.choose_key(m)
                    
                            transpose.encrypt(message_path)
                            print('your encrypted message is in the file ending with _transposition_cipher.txt')
                           
                        elif chioce == 'n':

                            print('enter the path of the key file')
                            key_file = input('key_file: ')
                            transpose = Transposition()
                         
                            transpose.encrypt(message_path,key_file)
                            print('your encrypted message is in the file ending with _transposition_cipher.txt')
                            
                        else:
                            print('invalid input')
                        
                       
                    elif option == 2:
                        transpose = Transposition()
                        key_file = input('enter the path of the key file: ')
                        print('enter the path of the cipher text file')
                        cipher_text_path = input('cipher_text_path: ')
                        
                        transpose.decrypt(cipher_text_path,key_file)
                        print('your decrypted message is in the file ending with _transposition_message.txt')
                        
                    elif option==3:
                        break
                    else:
                        print("option not avialable")



            elif cryptosystem == 3:
                
                while True:
                    print("list of opperations that can be perfomed\n 1. Encryption \n 2.Decryption \n 3.Sign \n 4.Verify \n 5.Back")
                    try:
                        option = int(input("Enter your option: "))
                    except:
                        print("invalid input, input shoud be 1,2 or 3")
                    if option == 1:
                        print("Enter the path of the message you want to encrypt")
                        message_path = input("message_path: ")
                        rsa = RSA()
                        print('Do you want to use a randomly generated private and public key? (y/n)')
                        choice = input('choice: ')
                        if choice == 'y':
                            rsa.choose_key()
                        
                            rsa.encrypt(message_path)
                            print('your encrypted message is in the file ending with _rsa_cipher.txt')
                            
                            
                        elif choice == 'n':
                            print('enter the path of your public key file')
                            key_file = input('public key_file path: ')
                            
                            rsa.encrypt(message_path,key_file)
                            print('your encrypted message is in the file ending with _rsa_cipher.txt')
                           
                        else:
                            print('invalid input')
                    elif option == 2:
                        rsa = RSA()
                        print('enter the path of your private key file')
                        key_file = input('private key_file path: ')
                        print('enter the path of the cipher text file')
                        cipher_text_path = input('cipher_text_path: ')
                        
                       
                        rsa.decrypt(cipher_text_path,key_file)
                        print('your decrypted message is in the file ending with _rsa_message.txt')
                       
                    elif option==3:
                        print('enter the path of the message file')
                        message_path = input('message_path: ')
                        rsa = RSA()
                        print('enter the path of your private key file')
                        key_file = input('private key_file path: ')
                        rsa.sign(message_path,key_file)
                        print('your signature is in the file ending with _rsa_signature.txt')
                    
                    elif option==4:
                        print('enter the path of the message file')
                        message_path = input('message_path: ')
                        print('enter the path of the signature file')
                        signature_path = input('signature_path: ')
                        rsa = RSA()
                        print('enter the path of your public key file')
                        key_file = input('public key_file path: ')
                        if rsa.verify(message_path,signature_path,key_file):
                            print('**************signature is valid*************')
                        else:
                            print('**************signature is not valid*************')
                    elif option==5:
                        break
                       
                    else:
                        print("option not avialable")
            elif cryptosystem==4:
                print("exiting....")
                break
            else:
                print("cryptosystem not avialable")
main()


# tr = Transposition(8)
# cipher = tr.encrypt("hello world is going to be the motto of programmers")
# print(cipher, 'cipher text')
# print(tr.decrypt(cipher) , 'decrypted text')


# rsa = RSA()
# cipher = rsa.encrypt("hello world is going to be the motto of programmers")
# print(cipher, 'cipher text')
# print(rsa.decrypt(cipher) , 'decrypted text')

# af = Affine()
# af.choose_key()
# af.encrypt('hello.txt')
# af.decrypt('hello_cipher.txt')

# tr = Transposition()
# tr.choose_key(100)
# tr.encrypt('hello.txt')
# tr.decrypt('hello_transposition_cipher.txt')

# rsa = RSA()
# rsa.choose_key()
# rsa.sign('hello.txt')
