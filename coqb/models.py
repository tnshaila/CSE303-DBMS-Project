from django.db import models
from django.contrib.auth.models import User


class School_T(models.Model):
    school_id = models.CharField(max_length=5, primary_key=True)
    school_name = models.CharField(max_length=100)


class Department_T(models.Model):
    dept_id = models.CharField(max_length=5, primary_key=True)
    school = models.ForeignKey(School_T, on_delete=models.CASCADE)
    dept_name = models.CharField(max_length=100, null=True)


class Program_T(models.Model):
    program_id = models.CharField(max_length=5, primary_key=True)
    program_name = models.CharField(max_length=30)
    department = models.ForeignKey(
        Department_T, on_delete=models.CASCADE, default='N/A')


class Course_T(models.Model):
    course_id = models.CharField(max_length=7, primary_key=True)
    course_name = models.CharField(max_length=30, null=True)
    no_of_credits = models.IntegerField()
    # program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    co_offered_courses = models.CharField(max_length=50, null=True)
    program = models.ForeignKey(
        Program_T, on_delete=models.CASCADE, default='N/A')

    def __str__(self):
        return self.course_id


class Employee_T(models.Model):
    emp_id = models.CharField(max_length=7, primary_key=True)
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, null=True)
    dept = models.ForeignKey(Department_T, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.f_name} {self.l_name}'


class Dean_T(models.Model):
    emp_pk = models.AutoField(primary_key=True)  # not in ERD

    emp = models.ForeignKey(
        Employee_T, on_delete=models.CASCADE)  # primary key
    school = models.ForeignKey(School_T, on_delete=models.CASCADE)
    # email = models.CharField(max_length=30, null=True)
    # dept = models.ForeignKey(Department_T, on_delete=models.CASCADE)


class Department_Head(models.Model):
    emp_pk = models.AutoField(primary_key=True)  # not in ERD

    emp = models.ForeignKey(
        Employee_T, on_delete=models.CASCADE)  # primary key
    # email = models.CharField(max_length=30, null=True)
    # dept = models.ForeignKey(Department_T, on_delete=models.CASCADE)


class Faculty_T(models.Model):
    faculty_pk = models.AutoField(primary_key=True)  # not in ERD

    emp = models.ForeignKey(
        Employee_T, on_delete=models.CASCADE)  # primary key
    RANK = (
        ('L', 'Lecturer'),
        ('S', 'Senior Lecturer'),
        ('AstP', 'Assistant Professor'),
        ('AscP', 'Associate Professor'),
        ('P', 'Professor'),
    )
    rank = models.CharField(max_length=5, choices=RANK)  # primary key?
    # email = models.CharField(max_length=30, null=True)
    # dept = models.ForeignKey(Department_T, on_delete=models.CASCADE)


class PLO_T(models.Model):
    plo_pk = models.AutoField(primary_key=True)  # not in ERD

    plo_no = models.CharField(max_length=5)  # primary key
    description = models.CharField(max_length=200, null=True)
    # course = models.ForeignKey(
    #     Course_T, on_delete=models.CASCADE)  # primary key
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    # details = models.CharField(max_length=5)


class CLO_T(models.Model):
    clo_pk = models.AutoField(primary_key=True)  # not in ERD

    clo_no = models.CharField(max_length=5)  # primary key
    course = models.ForeignKey(
        Course_T, on_delete=models.CASCADE)  # primary key
    description = models.CharField(max_length=200, null=True)
    plo = models.ForeignKey(PLO_T, on_delete=models.CASCADE)


class Section_T(models.Model):
    section_pk = models.AutoField(primary_key=True)  # not in ERD

    section_no = models.IntegerField()  # primary key
    SEMESTER = (
        ('Sp', 'Spring'),
        ('Su', 'Summer'),
        ('Au', 'Autumn'),
    )
    semester = models.CharField(max_length=10, choices=SEMESTER)  # primary key
    year = models.CharField(max_length=4)  # primary key
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty_T, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=10, null=True)
    end_time = models.CharField(max_length=10, null=True)
    day = models.CharField(max_length=10, null=True)
    room = models.CharField(max_length=15, null=True)
    
    def __str__(self):
        return f'Section {self.section_no} ({self.course.course_name}) {self.get_semester_display()} {self.year}'


class CourseOutline_T(models.Model):
    # co_pk = models.AutoField(primary_key=True)  # not in ERD

    # co_no = models.CharField(max_length=5)  # primary key
    # course = models.ForeignKey(
    #     Course_T, on_delete=models.CASCADE)  # primary key
    section = models.ForeignKey(
        Section_T, on_delete=models.CASCADE, primary_key=True)  # primary key
    # plo_no = models.ForeignKey(PLO_T, on_delete=models.CASCADE)
    # clo_no = models.ForeignKey(CLO_T, on_delete=models.CASCADE)
    COURSETYPE = (
        ('U', 'Undergraduate'),
        ('G', 'Graduate'),
    )
    course_type = models.CharField(
        max_length=30, choices=COURSETYPE, null=True)
    # credit_value = models.IntegerField()
    # course_hour = models.IntegerField()
    course_description = models.CharField(max_length=250, null=True)
    course_obj = models.CharField(max_length=30, null=True)
    course_policy = models.CharField(max_length=30, null=True)
    academic_dishonesty = models.CharField(max_length=250, null=True)
    student_disability = models.CharField(max_length=250, null=True)
    non_discrimination = models.CharField(max_length=250, null=True)
    course_content = models.CharField(max_length=250, null=True)
    # clo_matrix = models.CharField(max_length=250)
    # mapping_clo_with_plo = models.CharField(max_length=30)
    assesment_evaluation_section = models.CharField(max_length=30, null=True)
    # grading_chart = models.CharField(max_length=30)
    course_requrement = models.CharField(max_length=30, null=True)
    reference = models.CharField(max_length=30, null=True)


class QuestionBank_T(models.Model):
    qb_id = models.AutoField(primary_key=True)  # not in ERD

    section = models.ForeignKey(
        Section_T, on_delete=models.CASCADE)  # primary key
    question = models.CharField(max_length=1000)  # primary key
    # blooms_taxonomy_level = models.CharField(max_length=30)
    marks = models.FloatField()
    # clo = models.ForeignKey(CLO_T, on_delete=models.CASCADE)


class Exam_T(models.Model):
    exam_id = models.CharField(max_length=5, primary_key=True)
    question = models.ForeignKey(QuestionBank_T, on_delete=models.CASCADE)
    # time = models.CharField(max_length=30)


##########################


class Assessment_T(models.Model):
    assessment_id = models.AutoField(primary_key=True)
    assessment_name = models.CharField(max_length=30, null=True)
    # marks_obstained = models.FloatField()
    # total_marks = models.CharField(max_length=10)
    co_no = models.ForeignKey(CLO_T, on_delete=models.CASCADE)
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE, default=0)


class Evaluation_T(models.Model):
    evaluation_id = models.AutoField(primary_key=True)
    marks_obtained = models.FloatField()
    assessment = models.ForeignKey(
        Assessment_T, on_delete=models.CASCADE, default='N/A')


class Student_T(models.Model):
    student_id = models.CharField(max_length=7, primary_key=True)
    f_name = models.CharField(max_length=30, null=True)
    l_name = models.CharField(max_length=30, null=True)
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, null=True)
    email = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.f_name} {self.l_name}'


class Registration_T(models.Model):
    registration_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student_T, on_delete=models.CASCADE)
    SEMESTER = (
        ('Sp', 'Spring'),
        ('Su', 'Summer'),
        ('Au', 'Autumn'),
    )
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    semester = models.CharField(max_length=6, choices=SEMESTER)
    year = models.CharField(max_length=4)
