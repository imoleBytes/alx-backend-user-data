userpass = "imole:umegain"

splitted_str = userpass.split(':')
email = splitted_str[0]
passwd = userpass[len(email):]
# print(passwd)
# passwd = passwd[1:]

print(f"email: {email}")
print(f"passwd: {passwd}")
