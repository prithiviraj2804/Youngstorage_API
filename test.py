mail = input("Enter Mail Address: ")
ver = mail.split("@",-1)
allowed = ["gmail.com",'email.com']
if ver[1] in allowed:
    print("You are valid")
else:
    print("You are not valid")