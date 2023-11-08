import random
import sqlite3
import csv

conn = sqlite3.connect('StudentDB.sqlite') #establishes connection to database
mycursor = conn.cursor() #the cursor allows python to execute SQL statements

advisorList = ["Antonee Robinson", "John Stones", "Oscar Bobb", "Zach Steffen", "Rico Lewis"]

state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
def importDatabase():
    with open('students.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mycursor.execute(
                "INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted')  "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['FirstName'], row['LastName'], row['GPA'], row['Major'], random.choice(advisorList),
                 row['Address'], row['City'], row['State'], row['ZipCode'], row['MobilePhoneNumber'], 0))

def checkTable(input_val, colNum):
    exists = False
    mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0")
    myresult = mycursor.fetchall()
    for x in myresult:
        if (x[colNum] == input_val):
            exists = True
    return exists


exit = False
justStarted = True

while (exit != True):

    if (justStarted == True):
        importDatabase()
        justStarted = False

    user = input('\nType "Display" to display all students\nType "Add" to add a new student\nType "Update" to update a student\nType "Delete" to delete a student\nType "Search" to search for a student\nElse type "Exit" to exit the program\n')

    if (user == 'Display'):
        mycursor.execute("SELECT * FROM Student Where isDeleted = 0")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

    elif (user == 'Add'):
        firstName = input("What is the first name of the student?\n")
        while (firstName.isalpha() != True):
            firstName = input("Please enter an alphabetical value\n")
        lastName = input("What is the last name of the student?\n")
        while (lastName.isalpha() != True):
            lastName = input("Please enter an alphabetical value\n")
        gpa = input("What is the GPA of the student?\n")
        gpaCheck = False
        while (gpaCheck == False):
            if (gpa.replace(".", "").isnumeric() == False):
                gpa = input("Please enter a numerical value\n")
                continue
            if (round(float(gpa)) < 5.0):
                break
            else:
                gpa = input("GPA does not match requirements, enter a different value\n")

        major = input("What is the major of the student?\n")
        while (major.isalpha() != True):
            major = input("Please enter an alphabetical value\n")

        advisor = input("Who is the faculty advisor for the student?\n")
        advisorCheck = False
        while (advisorCheck == False):
            if (advisor.isnumeric() == True):
                advisor = input("Please enter an alphabetical value\n")
                continue
            if (advisor in advisorList):
                break
            else:
                advisor = input("Advisor does not exist, enter a different value\n")

        address = input("What is the address for the student?\n")

        city = input("What city is the student from?\n")
        while (city.isnumeric() == True):
            city = input("Please enter an alphabetical value\n")

        state = input("What state is the student from?\n")
        stateCheck = False
        while (stateCheck == False):
            if (state.isnumeric() == True):
                state = input("Please enter an alphabetical value\n")
                continue
            if (state in state_names):
                break
            else:
                state = input("State does not exist, enter a different value\n")

        zip = input("What is the zipcode for the student?\n")
        zipCheck = False
        while (zipCheck == False):
            if (zip.isnumeric() == False):
                zip = input("Please enter a numerical value\n")
                continue
            if (len(zip) == 5):
                break
            else:
                zip = input("Zipcode does not match requirements, enter a different value\n")

        phone = input("What is the student's phone number?\n")
        phoneCheck = False
        while (phoneCheck == False):
            if (phone.isnumeric() == False):
                phone = input('Invalid phone number, enter a different ten digits of the the new phone number\n')
                continue
            if (len(phone) == 10):
                break
            else:
                phone = input("Phone number does not match requirements, enter a different ten digit number")


        mycursor.execute("INSERT INTO Student('StudentId','FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted')  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, firstName, lastName, gpa, major, advisor, address, city, state, zip, phone, 0))

        print("Student added.")

    elif (user == 'Update'):
        contain = False
        id = input("What is the ID of the student you would like to update?\n")
        mycursor.execute("SELECT * FROM Student Where isDeleted = 0")
        myresult = mycursor.fetchall()

        done = False
        while (contain == False):
            if (id.isnumeric() == False):
                id = input("Enter a numeric value\n")
                continue
            else:
                done = True
            if (done == True):
                for x in myresult:
                    if (x[0] == int(id)):
                        contain = True
                        break
                if (contain == False):
                    id = input("ID does not exist, enter a different value\n")


        type = input('What field would you like to update?\nType "Major" to update Major field\nType "Advisor" to update Advisor field\nType "Phone" to update MobilePhoneNumber field\n')
        if (type == 'Major'):
            major = input('What is the new major for the student?\n')
            majorCheck = False
            while (majorCheck == False):
                if (major.isnumeric() == True):
                    major = input("Please enter an alphabetical value\n")
                    continue
                majorCheck = checkTable(major, 4)
                if (majorCheck):
                    mycursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?", (major,id,))
                    print("Field successfully updated")
                    break
                else:
                    major = input("Major does not exist, enter a different value\n")
        if (type == 'Advisor'):
            advisor = input('Who is the new advisor for the student?\n')
            advisorCheck = False
            while (advisorCheck == False):
                if (advisor.isnumeric() == True):
                    advisor = input("Please enter an alphabetical value\n")
                    continue
                if (advisor in advisorList):
                    mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?", (advisor,id,))
                    print("Field successfully updated")
                    break
                else:
                    advisor = input("Advisor does not exist, enter a different value\n")
        if (type == 'Phone'):
            phone = input('Enter ten digits of the the new mobile phone number for the student?\n')
            phoneCheck = False
            while (phoneCheck == False):
                if (phone.isnumeric() == False):
                    phone = input('Invalid phone number, enter a different ten digits of the the new phone number\n')
                    continue
                if (len(phone) == 10):
                    mycursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?", (phone,id,))
                    print("Field successfully updated")
                    break
                else:
                    phone = input("Phone number does not exist, enter a different ten digit number")

    elif (user == 'Delete'):
        contain = False
        id = input("What is the ID of the student you would like to delete?\n")
        mycursor.execute("SELECT * FROM Student Where isDeleted = 0")
        myresult = mycursor.fetchall()

        done = False
        while (contain == False):
            if (id.isnumeric() == False):
                id = input("Enter a numeric value\n")
                continue
            else:
                done = True
            if (done == True):
                for x in myresult:
                    if (x[0] == int(id)):
                        contain = True
                        mycursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?", (id,))
                        print("Succesfully deleted")
                        break
                if (contain == False):
                    id = input("ID does not exist\n")

    elif (user == 'Search'):
        type = input('Would field would you like to search by?\nType "Major" to search for Major field\nType "GPA" to search by GPA field\nType "City" to search by City field\nType "State" to search by State field\nType "Advisor" to search by FacultyAdvisor" field\n')

        if (type == "Major"):
            major = input('What is the major of the student?\n')
            majorCheck = False
            while (majorCheck == False):
                if (major.isnumeric() == True):
                    major = input("Please enter an alphabetical value\n")
                    continue
                majorCheck = checkTable(major, 4)
                if (majorCheck):
                    mycursor.execute("SELECT * FROM Student WHERE Major = ? and isDeleted = 0", (major,))
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        print(x)
                    break
                else:
                    major = input("Major does not exist, enter a different value\n")
        if (type == "GPA"):
            gpa = input("What is the GPA of the student?\n")
            gpaCheck = False
            while (gpaCheck == False):
                if (gpa.isalpha() == True):
                    gpa = input("Please enter a numerical value\n")
                    continue

                exists = False
                mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0")
                myresult = mycursor.fetchall()
                for x in myresult:
                    if (float(x[3]) == float(gpa)):
                        exists = True

                if (exists):
                    mycursor.execute("SELECT * FROM Student WHERE GPA = ? and isDeleted = 0", (gpa,))
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        print(x)
                    break
                else:
                    gpa = input("GPA does not exist, enter a different value\n")


        if (type == "City"):
            city = input("What city is the student from?\n")
            cityCheck = False
            while (cityCheck == False):
                if (city.isnumeric() == True):
                    city = input("Please enter an alphabetical value\n")
                    continue
                cityCheck = checkTable(city, 7)
                if (cityCheck):
                    mycursor.execute("SELECT * FROM Student WHERE City = ? and isDeleted = 0", (city,))
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        print(x)
                    break
                else:
                    city = input("City does not exist, enter a different value\n")
        if (type == "State"):
            state = input("What state is the student from?\n")
            stateCheck = False
            while (stateCheck == False):
                if (state.isnumeric() == True):
                    state = input("Please enter an alphabetical value\n")
                    continue
                stateCheck = checkTable(state, 8)
                if (stateCheck):
                    mycursor.execute("SELECT * FROM Student WHERE State = ? and isDeleted = 0", (state,))
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        print(x)
                    break
                else:
                    state = input("State does not exist, enter a different value\n")
        if (type == "Advisor"):
            advisor = input("Who is the faculty advisor for the student?\n")
            advisorCheck = False
            while (advisorCheck == False):
                if (advisor.isnumeric() == True):
                    advisor = input("Please enter an alphabetical value\n")
                    continue
                if (advisor in advisorList):
                    mycursor.execute("SELECT * FROM Student WHERE FacultyAdvisor = ? and isDeleted = 0", (advisor,))
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        print(x)
                    break
                else:
                    advisor = input("Advisor does not exist, enter a different value\n")

    elif (user == 'Exit'):
        exit = True

    else:
        print("Please enter a valid input from the following options:")


conn.close()


