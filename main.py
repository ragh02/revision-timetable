import yaml
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from random import shuffle

def rewriteFile(header,subjects,table):
    data_1 = yaml.dump(header)
    data_2 = yaml.dump(subjects)
    data_3 = yaml.dump(table)
    string = "# 'days' is the number of days you want to revise for\n# 'tests' is the number of papers you want to do per day\n"
    string += str(data_1)
    string += "\n# Enter your subjects here. Enter the subject name, then their 'weight''\n# The 'weight' is the ratio of that subject to other subjects.\n"
    string += "# For example, a ratio of 2 for one subject and 4 for another subject makes the 2nd subject show up twice as often.\n"
    string += str(data_2)
    string += "\n# DO NOT EDIT BEYOND THIS LINE!\n"
    string += str(data_3)
    return string
def loadFile(filepath):

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            config_dict = yaml.safe_load(f)
            return config_dict
    else:
        return("That file doesn't exist!")

def createFile(filepath):
    if os.path.exists(filepath):
        return("File already exists!")
    else:
        with open(filepath, "w") as file:
            data_1 = {
                "days":0,
                "tests":0
            }
            data_2 = {
                "subjects": {
                    "Maths": 3,
                    "Computer Science": 3
                }
            }
            data_3 = {
                "table":{},
                "completed":0
            }

            file.write(rewriteFile(data_1,data_2,data_3))


def constructSubjectList(subjectDict,total_tests):
    # calculate sum of weights
    totalweight = 0
    for s in subjectDict:
        totalweight += subjectDict[s]

    # calculate number of subjects to add
    s_counts = []
    # number of subjects = (weight / total weight) * total tests
    for s in subjectDict:
        s_counts.append({s:round((subjectDict[s]/totalweight)*total_tests)})

    # create a list of tests
    tests = []
    for i in range(len(s_counts)):
        for j in s_counts[i]:
            for k in range(s_counts[i][j]):
                tests.append(j)

    # shuffle list of tests
    shuffle(tests)
    return tests

# internal function for the one below
def formatSubjectListInner(test_list: list, tests_per_day: int, days: int, start_date: int):
    timetable = []
    row1 = []
    timetable = []
    # create header (day numbers)
    # maybe if I stop being lazy I'll add proper date formatting
    for i in range(days):
        row1.append(f"Day {i+start_date}")
    # create the nested lists depending on how many tests there are
    for i in range(tests_per_day):
        timetable.append([])
    # fill each row
    for i in range(len(test_list)):
        # calculate row to put things in
        row = i % tests_per_day

        # add subject
        timetable[row].append(test_list[i])

    # merge lists
    timetable.insert(0,row1)
    return timetable

# regular function that splits test list into groups of 5
def formatSubjectList(test_list: list, tests_per_day: int, days: int, batch_size: int):
    final_list = []
    start_list = test_list
    c = batch_size
    d = 0
    e = 0
    while len(start_list) > c:
        final_list.append(formatSubjectListInner(start_list[d:(batch_size + c)], tests_per_day, batch_size, e+1))
        c += batch_size*tests_per_day
        d += batch_size*tests_per_day
        e += batch_size

    # handle unfinished days
    print(f"{c} {d} {e} {len(test_list)} {len(start_list)}")
    remainder = (((len(start_list)-(c-batch_size))//batch_size)+1)
    final_list.append(formatSubjectListInner(start_list[d:len(test_list)], tests_per_day, remainder, e+1))
    return final_list


# PDF creating function
def createPdf(filepath, raw_data):
    document = SimpleDocTemplate(filepath,pagesize=A4)
    styles = getSampleStyleSheet()
    content = []
    content.append(Paragraph("<b>Revision Timetable</b>", styles["Title"]))
    content.append(Spacer(1, 12))
    # create table style
    css = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),  # header background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])

    # create table (list containing every 2D list)
    for item in raw_data:
        table = Table(item,colWidths=[150,150,150,150,150])
        table.setStyle(css)
        content.append(table)

    # build document
    document.build(content)
    print("Built successfully!")

# test code
subjects = constructSubjectList({"maths":2,"computer science":3},50)
# subjects = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
list = formatSubjectList(subjects,2,10,3)
createPdf("dirt.pdf",list)

# simple CLI to start
if __name__ == "__main__":
    print("Work in progress")