
class InputValidation():
    def password_validation(password, verify_password):
        if (len(password) < 4 and len(verify_password) < 4): 
            return False
        elif (password != verify_password):
            return False
        else:
             return True
    def email_validation(email):
        if '@' not in email:
            return False
        else: 
            return True