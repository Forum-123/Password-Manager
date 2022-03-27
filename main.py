import string
import os.path

alphabets = string.ascii_lowercase
numbers = "0123456789"
symbols = '''`¬¦!£$€%^&*()_-+={}[]~#:;@'"<,>.?/\|'''

directory = "C:\\tmp\\"
filename = "passwords.txt"
filepath = os.path.join(directory, filename)

# Directory is created if it doesn't exist already
if not os.path.isdir(directory):
    os.mkdir(directory)

# File is created if it doesn't exist already
if not os.path.isfile(filepath):
    with open(filepath, 'w') as file:
        pass

class BasePasswordManager:
    # List of user's passwords, where last item is their current password
    old_passwords = []

    with open(filepath, 'r') as file:
        for line in file:
            if line.strip():  # Checks file is not empty
                old_passwords.append(line)

    def get_password(self):
        """Returns the current password as a string"""
        return self.old_passwords[-1]

    def is_correct(self, input_string):
        """Takes a string and returns a boolean depending on if the string is equal to the current password or not """
        if input_string == self.old_passwords[-1]:
            return True
        else:
            return False


class PasswordManager(BasePasswordManager):
    def set_password(self):
        """Sets the user's password"""
        current_password = self.old_passwords[-1]
        password_input = input("Enter new password: ")

        input_security_level = self.get_level(password_input)

        # Minimum length of new password is 6 characters
        while len(password_input) < 6 or input_security_level <= self.get_level(current_password):
            if len(password_input) < 6:
                password_input = input("Password must have minimum 6 characters. Try again: ")

            # If old password has highest security level, new password must be of the same security level
            elif self.get_level(current_password) == 2:
                if input_security_level == self.get_level(current_password):
                    continue

            elif input_security_level <= self.get_level(current_password):
                # Security level of new password must be greater than that of current password
                password_input = input(f"Not secure enough. Enter an alphanumeric password with special characters: ")
                input_security_level = self.get_level(password_input)
                continue

        with open(filepath, 'a') as password_file:
            password_file.write("\n" + password_input)

            # Confirmation message is written to console
            print("New password has successfully been saved to Password Manager")

        return self.old_passwords.append(password_input)

    @staticmethod
    def get_level(password):
        alphabet_count = 0
        num_count = 0
        symbol_count = 0

        for character in password:
            if character in alphabets:
                alphabet_count += 1
            elif character in numbers:
                num_count += 1
            elif character in symbols:
                symbol_count += 1

        if symbol_count == 0:
            if (alphabet_count == 0 and num_count >= 1) or (alphabet_count >= 1 and num_count == 0):
                # Level 0: Password consists of alphabets or numbers only.
                level = 0
                return level
            elif alphabet_count >= 1 and num_count >= 1:
                # Level 1: Alphanumeric passwords.
                level = 1
                return level
        else:
            if alphabet_count >= 1 and num_count >= 1:
                # Level 2: Alphanumeric passwords with special characters.
                level = 2
                return level


user_passwords = PasswordManager()

while True:
    # Checks current password list has some content
    if user_passwords.old_passwords:
        yes_or_no = input("You already have a password. Would you like to add a new password (y/n)? ").lower()
        while yes_or_no not in ['y', 'n']:
            yes_or_no = input("Cannot understand. Do you want to add a new password (y for yes/ n for no)? ").lower()
        if yes_or_no == "y":
            user_passwords.set_password()
            yes_or_no = input("Are you happy with the password you have set (y/n)? ").lower()
            if yes_or_no == "y":
                break
            else:
                continue
        else:
            break
    # If no passwords are already stored, program will not go further
    else:
        print(f"You have no current passwords stored in the file {filepath}")
        break
