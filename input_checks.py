
#Input checks I grabbed from my "user signup" assignment

def valid_length(input):
    for i in input:
        if i == " ":
            return False
    return (len(input) >= 3 and len(input)<=20)


def match(password_1,password_2):
    return password_1 == password_2