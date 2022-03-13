class Cleaner_Login:
    def __init__(self):
        self.staff_name = input(f'')
        self.staff_id = input(f'')
        self.password = input('')

    def create_account(self):
        if self.existing():
            return self.existing()
        file=open("Cleaning_System.Txt")
        file.write(self.staff_name+""+self.staff_id+""+self.password)
        file.close()
        return(f"Staff Account Created Successfully")

    def existing(self):     
        for line in open('Cleaning_System.txt', 'r'):
            check = line.split()
        if self.staff_name == check[0] and self.staff_id == check[1]:
            opt = input(f"Wrong UserName or Password You want to Try again or Change Password (1/2) ??")
            if opt == 1:
                self.login()
            if opt == 2:
                newpass = input(f'Enter new password : ')
                check[2] = newpass
                with open("Cleaning_System.txt", "w") as file:
                    return(f'Password Updated Successfully {self.login()}')     
        
    def login(self):
        def authorized_login():
            check = line.split()
            if self.staff_name == check[0] and self.staff_id == check[1] and self.password == check[2]:
                return(f'Login Successful')
            if self.staff_name != check[0] and self.staff_id != check[1]:
                return(f'You dont hava an existing Staff Account in Cleaning account. Please let Billy know to create a account for you !!!')
            return(f'{self.existing()}')
        key = int(input("Login as a Admin(Billy) or Cleaning staff or Management Team (1/2/3)?? :"))
        if key == 1:
            file = open("Admin.txt")
            for line in open("Admin.txt", 'r'):
                authorized_login()

        if key == 2:
            file=open("Cleaning_System.txt")
            for line in open('Cleaning_System.txt', 'r'):
                authorized_login()
