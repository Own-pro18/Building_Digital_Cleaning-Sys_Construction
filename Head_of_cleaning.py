from re import A
import pymysql,logging
from C_Sys_Login import Cleaner_Login
logger = logging.getLogger(__name__)
db = pymysql.connect(host='localhost', user='root', password='', database="cleaning_system")
exc = db.cursor()
exc.execute("USE cleaning_system") 
db.commit()
import os
# from twilio.rest import Client
import smtplib
from email.message import EmailMessage

class Facility_Management_Sys:
    def __init__(self):
        self.staff_name = input(f"Enter Employee Name : ")
        self.staff_id = input(f"Enter Employee ID : ") 
        self.staff_role = input(f"Enter Employee Role : ")
        self.comments = input(f"Give your comments to Billy : ")
    
    def submit_cleaner_reports(self):
        try:
            print("Report File")
            file = open("Report.txt","a")
            file.write(self.staff_name+""+self.staff_id+""+self.staff_role+""+self.comments)
            file.close
            return(f"reported updated succesfully")
        except Exception as e:
            logger.error(f'Reporting Error')
            
    def auto_report_to_Billy_email(self):
        try:
            Email_address = os.environ.get("Email_id")
            Email_password = os.environ.get("Email_pass")

            with smtplib.SMTP_SSL('smtp.gmail.com', 334) as smtp:
                smtp.login(Email_address, Email_password)
                subject = 'Head of cleaning Report'
                body = 'Plumbing work done in the site(Room23) Need to replace the Boiler'
                msg = f'Subject : {subject} \n {body}'
                smtp.sendmail(Email_address, 'Myemil@gmail.com', msg)
        except Exception as e:
            logger.error(f'Problem in email reporting : {e} ')
            
    def auto_SMS_to_Billy_phone(self):
        account_sid = os.environ[""]
        auth_tocken = os.environ[""]
        client = Client(account_sid, auth_tocken)
        body = self.comments
        message = client.message.create(body , from_ = "", to_ = "" )
        return(message.sid)
        
# class Staff_records:

#     def view_my_record(self):
#     def view_my_task(self):
# class Building_records:
# class Inventory_Records:

class Admin_Access:
    def view_reports(self):
        reports = open("Report.txt","r").readlines()
        for report in reports:
            return report
        reports.close()

    def view_individual_staff_record(self):
        i = input(f'What is your Employee-ID ?? ')
        if self.userid == i:
            exc.execute("SELECT * FROM emp_personal_record WHERE userid= %s",i)
            record = exc.fetchall()
            return(record)
        else:
            return(f'Sorry you are trying to get WRONG USER Record')


    def individual_personal_task(self):
        i = input(f'What is your Employee-ID ?? ')
        if self.userid == i:
            exc.execute(' SELECT assign_tasks.Employee_ID, '
                        ' assign_tasks.Task_ID, emp_table.name,'
                        ' emp_table.occupation FROM assign_tasks'
                        ' RIGHT JOIN emp_table ON(emp_table.id = assign_tasks.Employee_ID)'
                        ' WHERE assign_tasks.Employee_ID = %s', i)
            record = exc.fetchall()
            print(record)
        else:
            print('Sorry you are trying to get WRONG USER Record')


    def add_new_staff(self):
        obj = Cleaner_Login()
        obj.create_account()
           
class Storage:

    def add_account(self):
        try:
            exc.execute(
                'CREATE TABLE Emp_Records '
                '(id INT(10) PRIMARY KEY AUTO_INCREMENT,'
                'name VARCHAR(20), '  
                'occupation VARCHAR(20))'
            )
        except Exception as e:
            logger.error(f'Table already exist : {e}')
        db.commit()

        try:
            exc.execute(
                'CREATE TABLE Emp_Tasks'
                '(task_id INT(10) PRIMARY KEY AUTO_INCREMENT,'
                'daily_task  VARCHAR(55),'
                'weekly_task VARCHAR(20),'
                'sprint_review_date VARCHAR(50))'
            )
            db.commit()

        except Exception as e:
            logger.error(f'Table already exist : {e}')

        try:
            exc.execute(
                'CREATE TABLE Assign_Tasks '
                '(Employee_ID INT(10),'
                'Task_ID INT(10) PRIMARY KEY,'
                'FOREIGN KEY(Employee_ID) REFERENCES Emp_Records(id) ON DELETE CASCADE,'
                'FOREIGN KEY(Task_ID) REFERENCES Emp_Tasks(task_id) ON DELETE CASCADE)'
            )
            db.commit()

        except Exception as e:
            logger.error(f'Assign_Tasks Table alreeady exist: {e}: ')

    def insert(self):
        n = int(input(f'How many records would you like to Insert in EMPLOYEE Records TABLE:   '))
        print(f"Insert the feilds in Employee Table")
        try:
            for i in range(n):
                En = input("Enter Employee Name: ")
                Eo = input("Enter Employee occupation: ")
                field = ("INSERT INTO Emp_Records"
                         "(name, occupation) "
                         "VALUES('{}','{}')".format(En, Eo))
                exc.execute(field)
                x=exc.rowcount
            print(f'{n} Records Inserted Successfully')
            db.commit()
        except Exception as e:
            print(f'{e}')
        db.commit()

        i = input(f'would you like to add Tasks in the Tasks list??(Yes/No)')
        if i == 'yes':
            print(f'Enter Task values :')
            daily_tasks= input(f'assign Daily Task: ')
            weekly_tasks= input(f'assign weekly Task: ')
            review_date= input(f' backlog Review : ')
            exc.execute(
                ' INSERT INTO Emp_Tasks('
                ' daily_task,'
                ' weekly_task,'
                ' review_date)'
                ' VALUES("{}","{}","{}"'
                ')'.format(daily_tasks,weekly_tasks,review_date)
            )
            db.commit()
            print(f'Task Added in Task-Table list')

        i = input(f'would you like to Assign Tasks to employees?? (yes/no)')
        if i == 'yes':
            print(f'set the Task id to the correspoding Employee-id  : ')
            emp = input(f'select the Employee whome do you like to assign the Task ::')
            task = input(f'what Task do you like to assign to this Employee ::')
            exc.execute('INSERT INTO Assign_Tasks'
                        '(Employee_ID,Task_ID) VALUES("{}","{}")'.format(emp, task)
                        )
            db.commit()
            print(f'Task assigned successfully: ')

    def showtable(self):
        print(f'1: Employee Table')
        print(f'2: Employee Tasks')
        print(f'3: Employee Assigned Tasks')
        i = int(input(f'To view data from the Tables hit 1/2/3/4 '))
        if i==1:
            exc.execute("SELECT * FROM Emp_Records")
            records = exc.fetchall()
            for record in records:
                return(f'{record}')

        if i==2:
            exc.execute("SELECT * FROM Emp_Tasks")
            records = exc.fetchall()
            for record in records:
                return(f'{record}')

        if i==3:
            exc.execute('SELECT Assign_Tasks.Employee_ID, '
                        'Assign_Tasks.Task_ID, Emp_Records.name,'
                        ' Emp_Records.occupation FROM Assign_Tasks'
                        ' RIGHT JOIN Emp_Records ON(emp_table.id = Assign_Tasks.Employee_ID)')
            records = exc.fetchall()
            for record in records:
                print(f'{record}')

        else:
            print(f'Please enter correct choice to show the table')

obj = Facility_Management_Sys()
print(obj.submit_cleaner_reports(), obj.auto_SMS_to_Billy_phone(), obj.auto_report_to_Billy_email())

obj = Storage()
print(obj.add_account(), obj.insert(), obj.showtable())
obj = Admin_Access()
print(obj.add_new_staff(),obj.individual_personal_task,obj.view_reports,obj.view_individual_staff_record)

