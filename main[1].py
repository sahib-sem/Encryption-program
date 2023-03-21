import random
import math

class Affine:

    # This is the encrypt method where the encryption of the message takes place
    # The formula f( p) = (ap + b) mod 255 will be used where a is the primary key and b is the secondary key
    def getKey(self): #return a randomly generated keys
        primary=random.randint(1,100)
        secondary=random.randint(1,100)
        if self.gcd(primary)==1:
            return  (primary,secondary)
        else:
            return self.getKey()


    def encrypt(self, message):
        primary,secondary=self.getKey()

        cipher_text = ""
        for x in message:
            value1 = primary * ord(x) + secondary # value1 stores the multiplication of the primary key and the unicode value of a character plus the secondary key
            value2 = value1 %255
            cipher_text += chr(value2)
        return cipher_text,primary,secondary

    # This is the decrypt method where a cipher_text is decrypted
    def decrypt(self, cipher_text, keys):
        primary, secondary = keys
        message = ""
        for x in cipher_text:

            value1 = self.inverse_mode(primary) * (ord(x) - secondary)

            value2 = value1%255
            message = message + chr(value2)

        return message

    def gcd(self, y, x=255):  # This method is used to calculate the gcd of 255 and the primary key

        if x == 0:
            return y

        else:
            return self.gcd(x, y % x)

    def inverse_mode(self, primary):  # This method is used to find the inverse of the primary key
        for x in range(255):
            if ((x * primary) % 255) == 1:
                return x

# ***************************************************************************************************************************


class Transposition:
    #given the value for m, it find the mapping function from {1,2,3,...,m} to itself
    def sigma_function(self,m):
        _set= list(range(1,m+1)) #generate list of numbers from 1 to m....{1,2,3....m}
        permutation=random.sample(_set,m) #permutuate the elements of the list , _set
        i,j=0,0
        mapping={}  #we used dictionary(hash map) to  store the mapping which gives sigma function required
        #loops through the elements of _set and assign a value from the permutuation
        #store the result in the hash map
        while i<len(_set):
            key=_set[i]
            mapping[key]=permutation[j]
            i+=1
            j+=1
        return mapping
    #find the inverse function or mapping given the function(dictionary)
    def inverse_sigma(self,mapping):
        inverse={} #stores the inverse mapping
        #loop through the key of the mapping.....the x value of the function
        #find the value corresponding to the keys....find y value of the function
        #swap the two,key and value, and store the result in the inverse mapping
        for key in mapping.keys():
            value=mapping[key]
            inverse[value]=key
        return inverse
    #take a message and m value(block_size) as input
    #find the mapping function which is random
    #returns the encrypted message and the mapping function used
    def encrypt(self,message):
        m=1
        while True:
            m=random.randint(4,10)
            if m<len(message):
                break
        if m<len(message):
            mapping = self.sigma_function(m) #find the mapping function
            #chunck the message into blocks of text based on the value of m
            message_block=[message[i:i+m] for i in range(0,len(message),m)]
            #check whether the last block is the same size as other blocks
            #make it equal size if it is not
            last=message_block[-1]
            while len(last)<len(message_block[0]):
                last+="x"
            message_block[-1]=last
            cipher_lst=[] #store the encrypted message
            #loop through the message block and use the mapping function
            #to find the corresponding cipher_block(encrypted block)
            for block in message_block:
                block_lst=list(block) #gives the list of characters in a block
                cipher_block=[0]*len(block_lst) #store the result,after applying the mapping function on the block_lst
                for key in mapping.keys():
                    value=mapping[key]
                    #store the character at key-1 on block_lst at the position of value-1 on the cipher_block
                    # key:value are pairs on the mapping function
                    #key-1 and value-1 because indexing start at 0
                    cipher_block[value-1]=block_lst[key-1]
                cipher_lst+=cipher_block
            cipher_text="" # store the encrpted message
            for char in cipher_lst:
                cipher_text+=char
            return cipher_text, mapping
        else:
            print("m value sould not be less than the message length")

    #given cipher_text and and a mapping function used to encrypt the message
    #return the original value
    def decrypt(self,cipher_text,mapping):
        m=len(mapping)
        inverse=self.inverse_sigma(mapping) #finds the inverse mapping function
        cipher_block=[cipher_text[i:i+m] for i in range(0,len(cipher_text),m)] #chunck the cipher_Text into blocks
        message_lst=[] #stores the decrypted message_block
        #loops through the cipher_block and use the inverse mapping to find the corresponding message_block
        for block in cipher_block:
            block_lst=list(block)
            message_block=[0]*len(block_lst) #store the result
            for key in inverse.keys():
                value=inverse[key]
                #reverse what is done in encrption process
                message_block[value-1]=block_lst[key-1]
            message_lst+=message_block
        message="" #store the decrypted message
        for char in message_lst:
            message+=char
        return message


#******************************************************************************************************************************************************


class RSA:
    def __init__(self):
        self.p=self.Prime_generator()
        self.q=self.Prime_generator()
    def gcd(self, y, x):  # This method is used to calculate the gcd of 255 and the primary key
        if x == 0:
            return y
        else:
            return self.gcd(x, y % x)

    def Prime_generator(self): #generate a random prime from range 100-999
        prime = random.randint(10,99)
        while True:
            isprime = True

            for x in range(2, int(math.sqrt(prime) + 1)):
                if prime % x == 0:
                    isprime = False
                    break

            if isprime:
                return prime

            prime += 1
    def get_public_Keys(self):

        N=self.p*self.q
        phi=(self.p-1)*(self.q-1)
        e=2
        for i in range(2,phi):
            if self.gcd(i,phi)==1:
                e=i
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
    def encrypt(self, message):

        m, n = self.get_public_Keys()  # N=m and e=n
        chunk = self.chunks(message)
        print(chunk)
        cipher_text = ""  # stores the encrypted message

        for block in chunk:

            b = int(block)
            res = self.modular_exponentiation(b, n, m)
            cipher_text+=str(res)+" "
        return cipher_text

    def inverse_mode(self, e, product):  # This method is used to find the inverse of e mod (p-1)*(q-1)
        for x in range(product):
            if (x * e % product) == 1:
                return x

    # receives a cipher_text in the form of chunks produced by encrpt method
    # two prime numbers must be provided
    # receive key as the tuple(N,e)
    # returns the decrypted message as a string

    def decrypt(self, cipher_text):
        cipher_text=cipher_text.split(" ")
        print(cipher_text)
        N, e = self.get_public_Keys()
        product = (self.p - 1) * (self.q - 1)  # calculates phi value used to find inverse of e mod phi
        message = []  # stores the decrypted message
        d = self.inverse_mode(e, product)  # d is the inverse of e mod product
        for i in cipher_text:
            if i!="":
                b = int(i)
                # res stores the decrypted message block
                res = str(self.modular_exponentiation(b, d, N))# d is the decryption key
                message.append(res)
        return self.Tostring(message)
    #return original message from the decrypted cipher
    def Tostring(self, sequence):
        res=""
        for m in sequence:
            val = int(m)
            res += chr(val)
        return res









def main():
    if __name__== "__main__":

        while True:
            print("This programm has 3 cryptosystems \n 1. Affine \n 2. Transposition \n 3. RSA \n 4. Exit")
            try:
                cryptosystem = int(input("Enter the number of the cryptosystem you wish to use: "))
            except:
                print("invalid input, input should be 1,2,3 and 4")

            if cryptosystem == 1:
                print("list of operations that can be performed\n 1. Encryption \n 2.Decryption \n 3.Back")
                while True:
                    try:
                        option = int(input("Enter your option: "))
                    except:
                        print("invalid input, input should be 1,2 or 3")
                    try:
                        if option == 1:
                            print("Enter your message in the form of text")
                            message = input("message: ")

                            affine = Affine()
                            cipher_text,primary,secondary =affine.encrypt(message)
                            print(f"you encrypted message is ,{cipher_text} and with primary key: {primary} and secondary key {secondary}")
                        elif option == 2:
                            affine = Affine()
                            print("Enter the message you want to decrypt")
                            cipher_text = input("cipher_text: ")
                            print("Enter primary and secondary keys")
                            primary = int(input("primary: "))
                            secondary = int(input("secondary: "))
                            key = (primary,secondary)
                            print(f"your decrypted message is, {affine.decrypt(cipher_text,key)}")
                        elif option==3:
                            break
                        else:
                            print("option not available")
                    except:
                        print("key should be integers")
            elif cryptosystem ==2:
                print("list of operations that can be performed\n 1. Encryption \n 2.Decryption \n 3.Back")
                while True:
                    try:
                        option = int(input("Enter your option: "))
                    except:
                        print("invalid input, input shoud be 1,2 or 3")
                    if option == 1:
                        try:
                            print("Enter your message in the form of text")
                            message = input("message: ")
                            transpose = Transposition()
                            cipher_text,map = transpose.encrypt(message)
                            print(f"The encrypted message is, {cipher_text} and the mapping function used is:{map}")
                        except:
                            pass

                    elif option == 2:
                        print("Enter your cipher_text in the form of text")
                        message = input("cipher_text: ")
                        m=input("enter your m value: ")

                          # n is the number of items you want to enter
                        try:
                            map = {}
                            for i in range(m):
                                text = input("enter key value pair separeted by a space: ").split()  # split the input text based on space & store in the list 'text'
                                map[int(text[0])] = int(text[1])
                            transpose = Transposition()
                            message = transpose.decrypt(cipher_text,map)
                            print(f"The decrypted message is,{message}")
                        except:
                            print("you should enter your number pair separeted by a spaced e.g: 2 3")
                    elif option==3:
                        break
                    else:
                        print("option not avialable")



            elif cryptosystem == 3:
                rsa = RSA()
                while True:
                    print("list of opperations that can be perfomed\n 1. Encryption \n 2.Decryption \n 3.Back")
                    try:
                        option = int(input("Enter your option: "))
                    except:
                        print("invalid input, input shoud be 1,2 or 3")
                    if option == 1:
                        print("Enter your message in the form of text")
                        message = input("message: ")

                        cipher_text = rsa.encrypt(message)
                        print(f"The  encrypted message is,{cipher_text}")
                    elif option == 2:
                        print("Enter the message you want to decrypt, your text may contain white space to demarket the blocks of the cipher text")
                        cipher_text = input("cipher_text: ")
                        message = rsa.decrypt(cipher_text)
                        print(f"The decrypted message is, {message}")
                    elif option==3:
                        break
                    else:
                        print("option not avialable")
            elif cryptosystem==4:
                print("exiting....")
                break
            else:
                print("cryptosystem not avialable")
main()
