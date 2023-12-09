import json
from z3 import *
import math
from collections import defaultdict

# subtract the start time from the end time to get the class time.
def timeToMint(time):
    hour = math.floor(time)
    mint = int((time - hour)*100)
    return int(hour*60+mint)
            
# EITHER WE CAN TAKE INPUT HERE FOR THE STUDENTS OR FROM JSON FILE. 
# (we only want to know no. of student enrolled in each course)

import csv
import random

# Number of students includieng all batches.
num_students = 1200

# List of courses
cid = ["HS201", 'MA201', 'MA202', 'ME301', 'CS101', 'CS102', 'CS202', 'CS341','CS389', 'HS301', 'EE201',
       'EE102', 'EE104', 'EE105', 'ME101', 'ME104', 'ME633', 'EE570', 'EE572', 'ME572', 'CS101', 'ME102', 'CS386', 'EE633', 'CS633', 'CS359', 'CS102', 'CS387', 'ME401', 'EE103', 'EE101', 'MA401']

# Generate random student data
students = []
for i in range(1, num_students + 1):
    roll_no = f'STUDENT{i:03d}'
    chosen_courses = random.sample(cid, min(5, len(cid)))
    students.append({'Roll No': roll_no, 'Courses': ', '.join(chosen_courses)})

# Write data to CSV file
csv_file_path = 'enrollment_data.csv'
columns = ['Roll No', 'Courses']

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(students)

print(f"CSV file '{csv_file_path}' generated successfully.") 

# Dictionary to store the count of students per course
course_count = {}

# Open and read the CSV file
with open(csv_file_path, mode='r') as file:
    # Create a CSV reader
    reader = csv.DictReader(file)
    
   # Iterate through each row in the CSV file
    for row in reader:
        # Assuming the column names are 'Roll No' and 'Course'
        courses = row['Courses'].split(', ')
        
        # Count the number of students per course
        for course in courses:
            course_count[course] = course_count.get(course, 0) + 1

# Print the results
for course, count in course_count.items():
    print(f"Course: {course}, Number of Students: {count}")


print("The algorithm is under process, currently this is the data availabe \n" )
#Read JSON data into the data variable
with open('ip.json') as f:
    data = json.load(f)    
instTimes = data["Time"]
classrooms = data["Rooms"]   #available classrooms.
courses = data["Courses"]  #course_info

# for width
def function(classes):
    coursename = classes[0]
    for course in courses:
        if course[0] == coursename:
            if course[2][0] == 180:
                return 100
            if course[2][0] == 60:
                return 30
            
coursename = [] # List storing the Name/id of the courses
duration = []   ## List storing the Duration of the courses
Rooms=[]
    
for course in courses:
        if(course[2][2] == 3):  
            course[2]=[180]
        else:
            sum= course[2][0]+course[2][1]
            course[2]=[]
            for k in range(sum):
                course[2].append(60)


for classroom in classrooms:
    Rooms.append(classroom[0])

for course in courses:
    coursename.append(course[0])       # insert course id.
    duration.append(course[2])         # insert l-t-p of course.

for i in range(len(courses)-5):
    cid= courses[i][0]
    if(course_count[cid]<=100):
        courses[i][4]="mini"
    elif(course_count[cid]<=150):
        courses[i][4]="small"
    elif(course_count[cid]<=250):
        courses[i][4]="medium"
    elif(course_count[cid]<=350):
        courses[i][4]="big"
    elif(course_count[cid]<=500):
        courses[i][4]="Large"

# for classname in classrooms:
#     Rooms.append(classname[0])  #actual room nos. in Rooms.

# Loop to convert Institute times to minutes using 'timeToMint()' function.
for i in range(len(instTimes)):
    for j in range(len(instTimes[i])):              
        instTimes[i][j] = timeToMint(instTimes[i][j])
        
# print(type(instTimes[i][j]))
# printing the contents of class&capacity.

classAndCapacity = defaultdict(list)  # Dictionary to map class type to classroom names

# Storing the classrooms of each type.
for classroom in classrooms:
    class_type = classroom[2]
    class_name = classroom[0]
    
    if class_type not in classAndCapacity:
        classAndCapacity[class_type] = [class_name] 
    else:
        classAndCapacity[class_type].append(class_name)

# Print the contents of the classAndCapacity dictionary
for class_type, classroom_names in classAndCapacity.items():
    print(f"Class Type: {class_type}")
    print(f"Classrooms: {', '.join(classroom_names)}")
    print()

class Room:
    def __init__(self,course,count,batch,capacity,faculty):
        self.course = course                                  ## name of the course runnning.
        self.day = String('{}_{}_day'.format(course,count))   ## day of class
        self.room = String('{}_{}_room'.format(course,count)) ## name of room
        self.Batch= batch                                     ## batch attending the class.
        self.startTime = Real('{}_{}_start_Time'.format(course,count))
        self.EndTime = Real('{}_{}_end_Time'.format(course,count))
        self.Capacity = capacity                                    
        self.Faculty = faculty

## Creating the objects of Room class, here-   
# courses[j][3] = faculty
# courses[j][4] = capacity
# courses[j][5] = batch
var = [] 
for j in range(len(courses)):
    temp = []  
    for i in range (len(courses[i])):
        temp.append(Room(coursename[j], i, courses[j][5], courses[j][4], courses[j][3]))
    var.append(temp)

# printing the duration list.
for i in range(len(duration)):
    print(f"{courses[i][0]}", " structure")
    for j in range(len(duration[i])):
        print(f" {duration[i][j]}", end=" ")
    print()

days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
## Constraint which fix the domain of day variable to Monday, Tuesday ,....,Friday.
val_for_days = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        exp = [var[i][j].day == String(Day) for Day in days]
        val_for_days.append(Or(*exp))

# (day==mon \/ day==tue \/ ..  .. \/ day==friday).
 
## Constraint which specifies that a particular course can't have more than 1 class a particular day.
prop1 = [] 
for i in range(len(duration)):
    exp1 = Distinct([var[i][j].day for j in range(len(duration[i]))])
    prop1.append(exp1)
    # lectures of the particular course will be on distinct days.
constraint1 = [And(*prop1)]

# print(str(duration[0][0]))

## Constraint for which the course time must be within the institute timings.
val_for_st_and_end_times = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        exp = [And(Or(And(var[i][j].EndTime <= instTimes[1][1],var[i][j].startTime >= instTimes[1][0]),
                  And(var[i][j].startTime >= instTimes[0][0], var[i][j].EndTime <= instTimes[0][1])),var[i][j].startTime < var[i][j].EndTime)]
        val_for_st_and_end_times.append(*exp)

## Constraint which states that (EndTime-StartTime == Duration) for the particular course.
constraint2 = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        exp = (var[i][j].EndTime - var[i][j].startTime) == (duration[i][j])
        constraint2.append(exp)

# next constraint to avoid clashes.
# converting 2-D list to a 1-D
list_of_var = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        list_of_var.append(var[i][j])

# for i in range (len(list_of_var)):
#     print(list_of_var[i].Batch[0])
#     print()
## Constraint which specifies that if the 2 courses are different and running on same day and 
# (Having the same batch OR
# Having the same faculty teaching OR
# Running in the same room) Then
# they must run at differnt timings.
constr_for_clashes = []
for i in range(len(list_of_var)):
    for j in range(len(list_of_var)):
        exp1 = False
        if i != j:
            for m in range(len(list_of_var[i].Batch)):
                for n in range(len(list_of_var[j].Batch)):
                    if list_of_var[i].Batch[m] == list_of_var[j].Batch[n]:
                        exp1 = True
                        break
                if exp1 == True:
                    break

        exp = If(Or(And(list_of_var[i] != list_of_var[j], list_of_var[i].day == list_of_var[j].day, exp1),
                    And(list_of_var[i] != list_of_var[j], list_of_var[i].day == list_of_var[j].day, list_of_var[i].Faculty == list_of_var[j].Faculty),
                    And(list_of_var[i] != list_of_var[j], list_of_var[i].day == list_of_var[j].day, list_of_var[i].room == list_of_var[j].room)),
                 Or(list_of_var[i].startTime >= list_of_var[j].EndTime, list_of_var[j].startTime >= list_of_var[i].EndTime),
                 True)
        constr_for_clashes.append(exp)

## Constraint which specifies that name of the room object will be the one in the JSON file according to the students enrolled in course & capacity of the room. 
val_for_room = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        exp = Or(*[var[i][j].room == String(rooom) for rooom in classAndCapacity[courses[i][4]]])
        val_for_room.append(exp)

S = Solver()
S.add(val_for_days)
S.add(constraint1)   #only 1 class of each course per day.
S.add(val_for_st_and_end_times)
S.add(constraint2)    #duration should be = (end-t-strt-t).
S.add(val_for_room)
S.add(constr_for_clashes)

print(S.check())
m= S.model()

printingTT = {}
mappingOfRoom = {}  ## Dictionary which maps the room variable to names of the room available in JSON file
mappingOfDay = {}   ## Dictionary which maps the day variable to days available.

mappingofBatch={}
mappingofBatch = {
    1: "Mnc btech 22",
    2: "Mnc btech 21",
    3: "All btech 22",
    4: "cs btech 22",
    5: "cs btech 21",
    6: "ee btech 21",
    7: "ee btech 20",
    8: "ce btech 21",
    9: "me btech 20",
    10: "me btech 23",
    11: "me btech 19",
    12: "cs btech 20",
    13: "ee btech 19",
    14: "cs btech 19",
}
while(1):
    print("Choose your batch option from below(1 or 2 or 3.. ..15)\n")
    print("(1) Mnc btech 22\n")
    print("(2) Mnc btech 21\n")
    print("(3) All btech 22\n")
    print("(4) cs btech 22\n")
    print("(5) cs btech 21\n")
    print("(6) ee btech 21\n")
    print("(7) ee btech 20\n")
    print("(8) ce btech 21\n")
    print("(9) me btech 20\n")
    print("(10) me btech 23\n")
    print("(11) me btech 19\n")
    print("(12) cs btech 20\n")
    print("(13) ee btech 19\n")
    print("(14) cs btech 19\n")
    print("(15) Whole Batch \n")
    batch_no= int(input("Your Batch- "))
    chosen_batch_description = mappingofBatch.get(batch_no)
    if(chosen_batch_description==""):
        print("Invalid batch number. Please choose a valid option.\n\n")
    else:
        print("Time Table generated successfully!")
        break
# fill all the dictionary.
## This loop just fills the 'mappingOfRoom' dictionary

if(batch_no<15):
    print(mappingofBatch[batch_no])
    print() 
else:
    print("Whole Batch\n")
filtered_classes = [list_of_var[i] for i in range(len(list_of_var)) if (str(list_of_var[i].Batch[0]) == chosen_batch_description or list_of_var[i].Batch == "Elective btech 22" or list_of_var[i].Batch == "Elective btech 21")]
# print(f"{list_of_var[i].Batch}")

for i in range(len(list_of_var)):
    temp = m.evaluate(list_of_var[i].room)
    for roomcap in classrooms:
        if temp == m.evaluate(String(roomcap[0])):
            mappingOfRoom[temp] = roomcap[0]

## This loop just fills the 'mappingOfDay' dictionary
for i in range(len(list_of_var)):
    temp = m.evaluate(list_of_var[i].day)
    for day in days:
        if temp == m.evaluate(String(day)):
            mappingOfDay[temp] = day 

if(batch_no==15):
# This loop just fills the 'printingTT' dictionary 
    for i in range(len(list_of_var)):
        if mappingOfDay[m.evaluate(list_of_var[i].day)] not in printingTT:
            printingTT[mappingOfDay[m.evaluate(list_of_var[i].day)]] = [[list_of_var[i].course,simplify(m.evaluate(list_of_var[i].startTime)/60),simplify(m.evaluate(list_of_var[i].EndTime)/60),mappingOfRoom[m.evaluate(list_of_var[i].room)],list_of_var[i].Faculty,list_of_var[i].Batch]]
            print()
        else:
            printingTT[mappingOfDay[m.evaluate(list_of_var[i].day)]] += [[list_of_var[i].course,simplify(m.evaluate(list_of_var[i].startTime)/60),simplify(m.evaluate(list_of_var[i].EndTime)/60),mappingOfRoom[m.evaluate(list_of_var[i].room)],list_of_var[i].Faculty,list_of_var[i].Batch]]
else:
    # Fill the 'printingTT' dictionary for the filtered classes
    # Inside the loop that filters classes
    # print("Filtered classes:", filtered_classes)

    for i in range(len(filtered_classes)):
        day_key = mappingOfDay[m.evaluate(filtered_classes[i].day)]

        if day_key not in printingTT:
            printingTT[day_key] = [[filtered_classes[i].course, simplify(m.evaluate(filtered_classes[i].startTime)/60), simplify(m.evaluate(filtered_classes[i].EndTime)/60), mappingOfRoom[m.evaluate(filtered_classes[i].room)], filtered_classes[i].Faculty, filtered_classes[i].Batch]]
        else:
            printingTT[day_key].append([filtered_classes[i].course, simplify(m.evaluate(filtered_classes[i].startTime)/60), simplify(m.evaluate(filtered_classes[i].EndTime)/60), mappingOfRoom[m.evaluate(filtered_classes[i].room)], filtered_classes[i].Faculty, filtered_classes[i].Batch])

# After initializing printingTT
# print("printingTT after initialization:", printingTT)

## Now this part is just to print the time table in csv format.
columns = ["Day", "class", "9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"]
mapTime = {
    '9': '9:00-10:00',
    '10': '10:00-11:00',
    '11': '11:00-12:00',
    '12': '12:00-13:00',
    '14': '14:00-15:00',
    '15': '15:00-16:00',
    '16': '16:00-17:00',
    '17': '17:00-18:00'
}

with open('TimeTable.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=columns)
    writer.writeheader()
    for day in days:
        listOfDictionaries = []
        count = 0

        for classn in Rooms:
            if classn == 'CCLAB1' or classn == 'CCLAB2' or classn == 'AILAB' or classn == 'Mechlab' or classn == 'EElab1' or classn == 'EElab2':
                if count == 0:
                    temp = {'Day':day,'class':'LAB'}
                    listOfDictionaries.append(temp)
                    count += 1
            else:
                temp = {'Day':day,'class':classn}
                listOfDictionaries.append(temp)

        for classes in printingTT.get(day, []):
            # if(printingTT.get(day, []) == []):
            #     continue
            # for class,cac in rooms:
            time = mapTime[classes[1].as_decimal(1)]
            merge = function(classes)
            cellvalue = classes[0]+" ("+classes[4]+")"
            # value = '{0: < merge}'.format(cellvalue)
            for diction in listOfDictionaries:
                if classes[3] == 'CCLAB1' or classes[3] == 'CCLAB2' or classes[3] == 'AILAB' or classes[3] == 'Mechlab' or classes[3] == 'EElab1' or classes[3] == 'EElab2':
                    if diction['class'] == 'LAB':
                        if time not in diction:
                            diction[time] = [[classes[0],classes[4], classes[3]]]
                        else:
                            diction[time] = [[classes[0],classes[4], classes[3]]]
                        break

                elif classes[3] == diction['class']:
                    if merge == 30:
                        diction[time] = '{0: <80}'.format(cellvalue)
                    elif merge == 50:
                        diction[time] = '{0: <50}'.format(cellvalue)
                    break
        writer.writerows(listOfDictionaries)
