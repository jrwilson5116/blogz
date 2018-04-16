
def valid_length(input):
    for i in input:
        if i == " ":
            return 'error: cannot contain spaces'

    if  len(input) < 3 or len(input) > 20:
        return 'error: must be between 3 and 20 characters'

    return ''

def match(password_1,password_2):
    if password_1 != password_2:
        return 'error: passwords do not match'
    return ''