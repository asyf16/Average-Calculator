import csv

marks = open('mark.csv', 'r')

reader = csv.reader(marks)
data = list(reader)
headers = ['Student Number', 'Course Number', 'Grade', 'Credit hours', 'Lastfirst']
hlocations = []  # columns with the headers

for i in range(0, len(headers)):
    for j in range(0, len(data[0])):
        if data[0][j].strip().lower() == headers[i].strip().lower():
            hlocations.append(j)  # finds the locations
marks.close()

marks = open('mark.csv', 'r')

reader = csv.reader(marks)
mark = []  # main array with all the data
for row in reader:  # appends the necessary columns
    mark.append([row[hlocations[0]], row[hlocations[1]], row[hlocations[2]], row[hlocations[3]], row[hlocations[4]]])

code = open('codes.csv', 'r')

reader = csv.reader(code)

codes = []  # list with course codes
for row in reader:
    codes.append([row[0], row[1], row[2]])  # appends the important rows

A = []
one = []
three = []
five = []
M = []
print(mark)

for i in range(0, len(codes)):  # sorts the exported courses
    if codes[i][1] == 'A':
        A.append(codes[i][0])
    if codes[i][1] == 'M':
        M.append(codes[i][0])
    if codes[i][1] == 'B':
        if codes[i][2].strip() == '3' or codes[i][2].strip() == '3,5':
            three.append(codes[i][0])
        if codes[i][2].strip() == '5' or codes[i][2].strip() == '3,5':
            five.append(codes[i][0])
        if codes[i][2] == '1':
            one.append(codes[i][0])


studentlocation = []  # array with the location of each new student

for i in range(1, len(mark)):  # finds the location of each new student, skips first row
    if mark[i][0] != mark[i - 1][0]: # search
        studentlocation.append(i)  # adds the location into the array

averages = []  # final array with all the averages


def calculate(a_list, y):  # finds the location of english
    acourses = []
    threecredits = []
    fivecredits = []
    onecredits = []
    base = 0
    t = len(a_list)  # the range will be the length of the array for the last student
    if y + 1 < len(studentlocation):  # checks if the student is the last one
        t = studentlocation[y + 1]

    for i in range(studentlocation[y], t):
        # checks for english
        for j in range(0, len(M)):  # finds english
            if M[j].strip() in a_list[i][1].strip():
                base = base + int(float(a_list[i][2]))

        for j in range(0, len(A)):  # appends the A courses into a list
            if A[j].strip().lower() in a_list[i][1].strip().lower():
                acourses.append(int(float(a_list[i][2])))

        for j in range(0, len(three)):  # appends the all three credit courses into a list
            if three[j].strip().lower() in a_list[i][1].strip().lower() and a_list[i][3].strip() == '3':
                threecredits.append(int(float(a_list[i][2])))

        for j in range(0, len(one)):  # appends the all one credit courses into a list
            if one[j].strip().lower() in a_list[i][1].strip().lower() and a_list[i][3].strip() == '1':
                onecredits.append(int(float(a_list[i][2])))

        for j in range(0, len(five)):  # appends the all five credit courses into a list
            if five[j].strip().lower() in a_list[i][1].strip().lower() and a_list[i][3].strip() == '5':
                fivecredits.append(int(float(a_list[i][2])))

    for i in range(len(acourses)):
        for j in range(0, len(acourses) - 1):
            if acourses[j] < acourses[j + 1]:  # if value is smaller than other one
                acourses[j], acourses[j + 1] = acourses[j + 1], acourses[j]
    for i in range(len(onecredits)):
        for j in range(0, len(onecredits) - 1):
            if onecredits[j] < onecredits[j + 1]:  # if value is smaller than other one
                onecredits[j], onecredits[j + 1] = onecredits[j + 1], onecredits[j]
    for i in range(len(threecredits)):
        for j in range(0, len(threecredits) - 1):
            if threecredits[j] < threecredits[j + 1]:  # if value is smaller than other one
                threecredits[j], threecredits[j + 1] = threecredits[j + 1], threecredits[j]
    for i in range(len(fivecredits)):
        for j in range(0, len(fivecredits) - 1):
            if fivecredits[j] < fivecredits[j + 1]:  # if value is smaller than other one
                fivecredits[j], fivecredits[j + 1] = fivecredits[j + 1], fivecredits[j]

    base = base + (acourses[0] + acourses[1] + acourses[2])  # mandatory courses
    base = base * 5
    choices = []
    if len(onecredits) >= 5:  # five one credits
        choices.append(round((base + onecredits[0] + onecredits[1] + onecredits[2] + onecredits[3] +
                              onecredits[4]) / 25, 2))
    if len(acourses) >= 4:  # all five are group A
        choices.append(round((base + (acourses[3] * 5)) / 25, 2))
    if len(fivecredits) >= 1:  # one five credits
        choices.append(round((base + (fivecredits[0] * 5)) / 25, 2))
    if len(threecredits) >= 2:  # two three credits
        choices.append(round((base + ((threecredits[0] + threecredits[1]) * 3)) / 26, 2))
    if len(threecredits) >= 1 and len(onecredits) >= 2:  # one three two ones
        choices.append(round((base + ((threecredits[0] * 3) + onecredits[0] + onecredits[1])) / 25, 2))
    for i in range(len(choices)): # sort
        for j in range(0, len(choices) - 1):
            if choices[j] < choices[j + 1]:  # if value is smaller than other one
                choices[j], choices[j + 1] = choices[j + 1], choices[j]
    averages.append(choices[0])


error_five = []
error_english = []
english_check = False
course_check = False
heading_check = False
course_amounts = 0


def error_check(a_list, y):
    global course_amounts
    t = len(a_list)  # the range will be the length of the array for the last student
    if y + 1 < len(studentlocation):  # checks if the student is the last one
        t = studentlocation[y + 1]

    for i in range(studentlocation[y], t):
        for j in range(0, len(M)):  # finds english
            if M[j].strip() in a_list[i][1].strip():
                course_amounts = course_amounts + 1
        for j in range(0, len(A)):  # appends the A courses into a list
            if A[j].strip().lower() in a_list[i][1].strip().lower():
                course_amounts = course_amounts + 1
        for j in range(0, len(three)):  # appends the all three credit courses into a list
            if three[j].strip().lower() in a_list[i][1].strip().lower() and a_list[i][3].strip() == '3':
                course_amounts = course_amounts + 1
        for j in range(0, len(one)):  # appends the all one credit courses into a list
            if one[j].strip().lower() in a_list[i][1].strip().lower() and a_list[i][3].strip() == '1':
                course_amounts = course_amounts + 1
        for j in range(0, len(five)):  # appends the all five credit courses into a list
            if five[j].strip().lower() in a_list[i][1].strip().lower() and a_list[i][3].strip() == '5':
                course_amounts = course_amounts + 1


for i in range(0, len(studentlocation)):
    error_check(mark,i)
    calculate(mark, i)


print(averages)

student_numbers = []
for i in range(0, len(studentlocation)):
    student_numbers.append(mark[studentlocation[i]][0])

names = []
for i in range(0, len(studentlocation)):
    names.append(mark[studentlocation[i]][4])

f = open('export.csv', 'wt', newline='')  # opens a csv file named 'export'
f.truncate() # deletes any previous data on the csv file
writer = csv.writer(f) # opens the file in writing mode
writer.writerow(["Student Name", "Student Number", "Average"])  # writes the headings to the spreadsheet
for i in range(0, len(averages)):
    writer.writerow([names[i], student_numbers[i], str(averages[i])])  # append the calculated scores and student names

choice = int(input('Search for a student number: '))
for i in range(0, len(student_numbers)):
    if int(student_numbers[i]) == choice:
        print("The student has an average of", averages[i])

f.close()
marks.close()
code.close()
