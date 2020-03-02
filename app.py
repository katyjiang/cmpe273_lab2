from flask import Flask, escape, request

app = Flask(__name__)

DB = {
    "students":[],
    "classes":[]
}

student_id = 0

class_id = 0

@app.route('/')
def hello():
    name = request.args.get("name", "Katy")
    return f'Hello, {escape(name)}!'

# create a new student
@app.route('/students',methods=['POST'])
def create_student():
    global DB, student_id, class_id
    name = (request.json)["name"]

    for student in DB["students"]:
        if name == student["name"]:   #check if student existed
            return student
    DB["students"].append({
        "name": name, 
        "id": student_id
    })
    student_id = student_id + 1
    return DB["students"][-1]

# retrieve an existing student
@app.route('/students/<stu_id>',methods=['GET'])
def search_student(stu_id):
    global DB, student_id, class_id
    for student in DB["students"]:
        if int(stu_id) == student["id"]:
            return student
    return f"This student is not existed."

# create a new class
@app.route('/classes',methods=['POST'])
def create_class():
    global DB, student_id, class_id
    name = (request.json)["name"]
    for course in DB["classes"]:
        if name == course["name"]:   #check if class existed
            return course
    DB["classes"].append({
        "id": class_id,
        "name": name, 
        "students":[]
    })
    class_id = class_id + 1
    return DB["classes"][-1]

# retrieve an existing class
@app.route('/classes/<cour_id>',methods=['GET'])
def search_class(cour_id):
    global DB, student_id, class_id
    for course in DB["classes"]:
        if int(cour_id) == course["id"]:
            return course
    return f"This class is not existed."

# add students to a class
@app.route('/classes/<cour_id>',methods=['PATCH'])
def add_student(cour_id):
    global DB, student_id, class_id
    stu_id = (request.json)["student_id"]
    course_existed = False
    for course in DB["classes"]:
        if int(cour_id) == course["id"]:     #check existed
            course_existed = True
            break 
    if not course_existed:
        return f"This course is not existed."

    student_existed =False
    found_student = None
    for student in DB["students"]:
        if int(stu_id) ==student["id"]:      #check existed
            student_existed = True
            found_student = student
            break
    if not student_existed:
        return f"This student is not existed."

    student_added = False
    for course in DB["classes"]:
        if course["id"] == int(cour_id):
            for student in course["students"]:
                if student["id"] == int(stu_id):
                    student_added = True
                    break
            if not student_added:
                course["students"].append(found_student)
            return course       
