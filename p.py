import sqlite3,csv
from datetime import datetime
from cs50 import SQL
db = SQL("sqlite:///school.db")
 
def login():
        print()
        name=input("Username: ")
        pwd=input("password: ")
        if pwd=='admin'==name:
            print("\nLoged in as admin.\n")
            admin_view()
        elif db.execute("SELECT * FROM people WHERE name=? AND pwd=?;",name,pwd)!=None:
            print(f"Loged in as {name}(STUDENT).")
            student_view(name)
        else:
            print("username not exits")
            login()
def admin_view():
    cmd=input('''\nPress 1 to view current students.
Press 2 to add new student.
Press 3 to logout as admin.
Press 4 to remove a student.
Press 4 to remove a student.
Press 5 to add marksheet.
Press 6 to add todays attendence.
Press 7 to check class average.
Press 8 to Fee status of students.
Press 9 to change Fee status of any student.
Press 10 to send a message to students.
press 11 to see messages from students. 
''')
    if cmd=='1':
        for student in db.execute("SELECT name FROM people;"):
            print(student['name'] )
    elif cmd=="2":
        name=input("Student name: ")
        pwd=input("Create a pwd: ")
        try: 
            db.execute("INSERT INTO peopleee(name, pwd) VALUES(?,?);",name,pwd)
        except RuntimeError:
            db.execute("CREATE TABLE people(id INTEGER PRIMARY KEY AUTOINCREMENT,name, pwd, percentage FLOAT DEFAULT 0);")
            db.execute("INSERT INTO people(name, pwd) VALUES(?,?);",name,pwd)
        print("\nStudent added.")
    elif cmd=='3':
        print("\nLogged out from admin view.")
        login()

    elif cmd=='4':
        name=input("Username to delete: ")
        try:
            db.execute("DELETE FROM people WHERE name=?;",name)
            print(f"Sucessfuly deleted {name} from student")
        except:
            print(f"{name} is not a student")
    elif cmd=='5':
        names=db.execute("SELECT name FROM people;")
        for name in names:
            name=name["name"]
            percentage=-1
            while not 0<=int(percentage)<=100:
                percentage=input(f"{name}: ")
            db.execute("UPDATE people SET percentage=? WHERE name=?;",percentage,name)
        print("\n\nUpdated percentages.")
    elif cmd=='6':
        names=db.execute("SELECT name FROM people;")
        for student in names:
            name=student['name']
            attendence='w'
            while attendence.lower() not in ['a','p']:
                attendence=input(f"{name}: ")
            if attendence.lower()=='p':
                date=datetime.now().strftime("%d/%m/%Y")
                try:
                    if date not in[item['date'] for item in db.execute("SELECT date FROM Attandence WHERE attendees=?;",name)]:
                        db.execute("INSERT OR IGNORE INTO Attandence(date, attendees) VALUES(?, ?);",date,name)
                except:
                    db.execute("CREATE TABLE Attandence(date TEXT NOT NULL,attendees TEXT NOT NULL);")
                    db.execute("INSERT OR IGNORE INTO Attandence(date, attendees) VALUES(?, ?);",date,name)
            
        print("\n\nUpdated todays attendence.")
    elif cmd=='7':
        print(db.execute("SELECT avg(percentage) FROM people;"))
    elif cmd=="8":
        for student in db.execute("SELECT * FROM people;"):
            print(student['name'] ,':', student['fee_status'])
    elif cmd=="9":
        name=input("Student name: ")
        status=input("Fee status update: ")
        db.execute("UPDATE people set fee_status=? where name=?;",status,name)
        print("Upadat sucessfull!")
    elif cmd=='10':
        msg=input("Enter a message: ")
        for student in db.execute("SELECT * FROM people where name!='admin';"):
            db.execute("insert into messages(sender,reciever,msg,time) values('admin',?,?,?);",student['name'],msg,datetime.now())
    elif cmd=='11':
        print(db.execute("SELECT sender,msg from messages where reciever='admin';"))       

    print(db.execute("SELECT * FROM people;" ))
        
#recursive call to admin view
    admin_view()

def student_view(name):
    cmd=input('''\nPress 1 to Overall percentage.
Press 2 to view your attendence.\nPress 3 to logout.
Press 4 to view fee status. 
Press 5 to check class average.
Press 6 to view messages.
Press 7 to send a message
''')
    if cmd=='1':
        print(db.execute("select percentage from people where name=?",name))
    elif cmd=="2":
        dates=db.execute("select date from Attandence where attendees=?;",name)    
        print("You were marked present on:")
        presents=0
        for date in dates:
            print(date['date']);presents+=1
            attend_percent=(presents*100)/(list(db.execute("select count(distinct(date)) from Attandence where attendees!=?;",name)[0].values())[0])        
            print("Your overall atandence percentage is:",attend_percent)
    elif cmd=="3":
        return login()
    elif cmd=="4":
        print("Fee status: ",db.execute("SELECT fee_status FROM people where name=?;",name)[0]['fee_status'])
    elif cmd=="5":
        print("Class average: ",db.execute("SELECT avg(percentage) FROM people;"))
    elif cmd=='6':
        print(db.execute("SELECT sender,msg from messages where reciever=?",name))       
    elif cmd=='7':
        reciever=input("reciever: ")
        for student in db.execute("SELECT name from people;"):
            if reciever==student["name"]:
                msg=input("Enter your message: ")
                db.execute("insert into messages(sender,reciever,msg,time) values(?,?,?,?);",name,reciever,msg,datetime.now())

    
    return student_view(name)
login()