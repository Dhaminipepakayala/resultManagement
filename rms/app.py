from flask import Flask,render_template,redirect,request,url_for
from mysql.connector import connect

app=Flask(__name__)
con=connect(host='localhost',port=3306,database='resultsmanagement',user='root')
cur=con.cursor()
grade_to_points = {
    'O': 10,
    'A': 9,
    'B': 8,
    'C': 7,
    'D': 6,
    'F': 5
}
def calculate_gpa(results):
    total_points = 0
    total_credits = 0

    for result in results:
        grade = result[3]  
        credits = result[4]  
        total_points += grade_to_points.get(grade, 0) * credits
        total_credits += credits

    if total_credits == 0:
        return 0

    gpa=total_points / total_credits 
    return "{:.2f}".format(gpa)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

    return render_template('admin.html')

@app.route('/admin')
def admin():
    return render_template('login.html')
@app.route('/courses',methods=["GET","POST"])
def courses():
    if request.method=='POST':
        title=request.form['title']
        dept=request.form['dept']
        cur.execute("INSERT INTO courses(course_name,department) VALUES(%s,%s)",(title,dept))
        con.commit()
    cur.execute("select * from courses")
    obj=cur.fetchall()

    return render_template('/courses.html',obj=obj)
@app.route('/editcourse/<int:id>',methods=["GET","POST"])
def editcourse(id):
    try:
        if request.method=='POST':
            title=request.form['title']
            dept=request.form['dept']
            # cur.execute("SELECT COUNT(*) FROM courses WHERE course_id = %s", (id,))
            # count = cur.fetchone()[0]
            # if count > 0:
            #     return "Cannot edit subject: Related course exist."

            cur.execute("UPDATE courses SET  course_name=%s,department = %s WHERE course_id = %s",(title,dept,id))
            con.commit()
        cur.execute("select * from courses")
        obj=cur.fetchall()
        return render_template('/courses.html',obj=obj)
    except Exception as e:
        return "An error occurred: " + str(e)
@app.route('/delcourse/<int:id>')
def delcourse(id):
    try:
        cur.execute("SELECT COUNT(*) FROM subjects WHERE course_id = %s", (id,))
        count = cur.fetchone()[0]
        if count > 0:
            return "Cannot delete course: Related subjects exist."
        cur.execute("DELETE FROM courses WHERE course_id = %s", (id,))
        con.commit()        
        cur.execute("SELECT * FROM courses")
        obj = cur.fetchall()
        return render_template('/courses.html', obj=obj)
    except Exception as e:
        return "An error occurred: " + str(e)

@app.route('/subjects',methods=['POST','GET'])
def subjects():
    if request.method=='POST':
        course_id=request.form['course_id']
        title=request.form['title']
        sem=request.form['sem']
        credits=request.form['credits']
        cur.execute("INSERT INTO subjects(course_id,sub_name,semester,credits) VALUES(%s,%s,%s,%s)",(course_id,title,sem,credits))
        con.commit()
    cur.execute("select * from subjects")
    obj=cur.fetchall()
    return render_template('/subjects.html',obj=obj)
@app.route('/editsubject/<int:id>',methods=["GET","POST"])
def editsub(id):
    try:
        if request.method=='POST':
            course_id=request.form['course_id']
            title=request.form['title']
            sem=request.form['sem']
            credits=request.form['credits']
            cur.execute("SELECT COUNT(*) FROM courses WHERE course_id = %s", (id,))
            count = cur.fetchone()[0]
            if count > 0:
                return "Cannot edit subject: Related course exist."

            cur.execute("UPDATE subjects SET  course_id=%s,sub_name = %s, semester = %s, credits = %s WHERE sub_id = %s",(course_id,title,sem,credits,id))
            con.commit()
        cur.execute("select * from subjects")
        obj=cur.fetchall()
        return render_template('/subjects.html',obj=obj)
    except Exception as e:
        return "An error occurred: " + str(e)
@app.route('/delsub/<int:id>')
def delsub(id):
    try:
        cur.execute("SELECT COUNT(*) FROM exams WHERE sub_id = %s", (id,))
        count = cur.fetchone()[0]
        if count > 0:
            return "Cannot delete subject: Related exams exist."
        cur.execute("DELETE FROM subjects WHERE sub_id = %s", (id,))
        con.commit()        
        cur.execute("SELECT * FROM subjects")
        obj = cur.fetchall()
        return render_template('/subjects.html', obj=obj)
    except Exception as e:
        return "An error occurred: " + str(e)
@app.route('/students',methods=['POST','GET'])
def students():
    if request.method=='POST':
        sid=request.form['sid']
        name=request.form['name']
        email=request.form['email']
        batch=request.form['batch']
        department=request.form['department']
        cur.execute("INSERT INTO students(sid,name,email,batch,department) VALUES(%s,%s,%s,%s,%s)",(sid,name,email,batch,department))
        con.commit()
    cur.execute("select * from students")
    obj=cur.fetchall()
    return render_template('/students.html',obj=obj)
@app.route('/editstudent/<string:id>',methods=["GET","POST"])
def editstudent(id):
    try:
        if request.method=='POST':
            name=request.form['name']
            email=request.form['email']
            batch=request.form['batch']
            department=request.form['department']
            
            cur.execute("UPDATE students SET name = %s, email = %s, batch = %s,department=%s WHERE sid = %s",(name,email,batch,department,id))
            con.commit()
        cur.execute("select * from students")
        obj=cur.fetchall()
        return render_template('/students.html',obj=obj)
    except Exception as e:
        return "An error occurred: " + str(e)
@app.route('/delstudent/<string:id>')
def delstudent(id):
    try:
        cur.execute("SELECT COUNT(*) FROM results WHERE stud_id = %s", (id,))
        count = cur.fetchone()[0]
        if count > 0:
            return "Cannot delete student: Related result exist."
        cur.execute("DELETE FROM students WHERE sid = %s", (id,))
        con.commit()        
        cur.execute("SELECT * FROM students")
        obj = cur.fetchall()
        return render_template('/students.html', obj=obj)
    except Exception as e:
        return "An error occurred: " + str(e)
@app.route('/exams',methods=["GET","POST"])
def exams():
    if request.method == "POST":
        sub_id=request.form['subcode']
        title=request.form['title']
        date=request.form['date']
        print(date)
        cur.execute("INSERT INTO exams(sub_id,exam_name,exam_date) values(%s,%s,%s)",(sub_id,title,date))
        con.commit()
    cur.execute("SELECT * from exams")
    obj=cur.fetchall()
    return render_template('/exams.html',obj=obj)   
@app.route('/editexam/<int:id>',methods=["GET","POST"]) 
def editexam(id):
    try:
        if request.method=='POST':
            sub_id=request.form['subcode']
            title=request.form['title']
            date=request.form['date']
            cur.execute("SELECT COUNT(*) FROM subjects WHERE sub_id = %s", (sub_id,))
            count = cur.fetchone()[0]
            if count > 0:
                 return "Cannot edit exam: Related subject exist."

            cur.execute("UPDATE exams SET  sub_id=%s,exam_name = %s, exam_date = %s WHERE exam_id = %s",(sub_id,title,date,id))
            con.commit()
        cur.execute("select * from exams")
        obj=cur.fetchall()
        return render_template('/exams.html',obj=obj)
    except Exception as e:
        return "An error occurred: " + str(e)
@app.route('/delexam/<int:id>')
def delexam(id):
    try:
        cur.execute("SELECT COUNT(*) FROM results WHERE exam_id = %s", (id,))
        count = cur.fetchone()[0]
        if count > 0:
          return "Cannot delete exam: Related results exist."
        cur.execute("DELETE FROM exams WHERE exam_id = %s", (id,))
        con.commit()        
        cur.execute("SELECT * FROM exams")
        obj = cur.fetchall()
        return render_template('/exams.html', obj=obj)
    except Exception as e:
        return "An error occurred: " + str(e)

@app.route('/results',methods=["POST","GET"])
def results():
    obj1 = []
    exam_id = None
    if request.method=="POST":
        batch=request.form['batch']
        dept=request.form['dept']
        exam_id=request.form['exam_id']
        cur.execute("select sid from students where batch=%s and department=%s",(batch,dept))
        obj=cur.fetchall()
        for i in obj:
            cur.execute("SELECT count(stud_id) from results where stud_id=%s and exam_id=%s",(i[0],exam_id))
            ob=cur.fetchone()[0]
            if ob <= 0:
                cur.execute("INSERT INTO results(stud_id,exam_id) values(%s,%s)",(i[0],exam_id))
                con.commit()
        cur.execute("select s.sid,s.name,r.marks,r.grade from students s join results r on s.sid=r.stud_id where r.exam_id=%s",(exam_id,))
        obj1=cur.fetchall()
    elif request.method == "GET":
        exam_id = request.args.get('exam_id')
        if exam_id:
            cur.execute("SELECT s.sid, s.name, r.marks, r.grade FROM students s JOIN results r ON s.sid = r.stud_id WHERE r.exam_id = %s", (exam_id,))
            obj1 = cur.fetchall()
    
    return render_template('/results.html',obj1=obj1,exam_id=exam_id)
   

@app.route('/results/<string:id>',methods=["GET","POST"])
def editmarks(id):
    
    if request.method=="POST":
        marks=request.form['marks']
        grade=request.form['grade']
        exam_id=request.form['exam_id']
        cur.execute("update results set marks=%s,grade=%s where stud_id=%s and exam_id=%s",(marks,grade,id,exam_id))
        con.commit()
    return redirect(url_for('results',exam_id=exam_id))
@app.route('/search',methods=['GET','POST'])
def search():
    if(request.method=='POST'):
        regd=request.form['regd_no']
        sem=request.form['sem']
        cur.execute("select sid,name,department from students  where sid=%s",(regd,))
        obj1=cur.fetchall()
        cur.execute("SELECT e.exam_name,sub.sub_name,r.marks,r.grade,sub.credits FROM subjects sub join exams e on sub.sub_id = e.sub_id join results r on r.exam_id = e.exam_id where r.stud_id=%s and sub.semester=%s",(regd,sem))
        obj=cur.fetchall()   
        gpa=calculate_gpa(obj)
    return render_template('index.html',obj=obj,obj1=obj1,gpa=gpa)
if __name__ == "__main__":
    app.run()
