import random
otp=random.randrange(0,99999)
print("Your OTP is:", otp)
length=4
user=input("enter the otp:")
if otp==user:
    print("Otp is in477correct")
else:
    print("Otp is correct")