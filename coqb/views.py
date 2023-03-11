import io
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from .decorators import *
from .models import *
from .queries import *


@unauthenticated
def home(request):
    return render(request, 'coqb/home.html')


@unauthenticated
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'coqb/signin.html', {
                'failed': True,
            })
    else:
        return render(request, 'coqb/signin.html', {
            'failed': False,
        })


def signout(request):
    logout(request)
    return redirect('signin')

# def faculty_dashboard(request):
#     return render(request, 'coqb/faculty_dashboard.html')


def authorize(request):
    try:
        faculty = Faculty_T.objects.get(emp__user=request.user)
        return 'faculty', faculty

    except Faculty_T.DoesNotExist:
        pass

    try:
        student = Student_T.objects.get(user=request.user)
        return 'student', student

    except Student_T.DoesNotExist:
        return 'none', None


# Pages

@authenticated
def dashboard(request):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        faculty_info = get_faculty_section_info(auth_data.emp_id)
        return render(request, 'coqb/faculty_dashboard.html', {
            'name': name,
            'page': 'dashboard',
            'faculty_info': faculty_info,
        })
    elif auth_type == 'student':
        name = str(auth_data)
        student = Student_T.objects.get(student_id=auth_data.student_id)
        registration = Registration_T.objects.all().filter(student_id=student)
        sections = [Section_T.objects.get(section_pk=item.section_id) for item in registration]
        sections = [[item.course.course_id, item.course.course_name, item.section_no, item.start_time, item.day]for item in sections]
            
        print(sections)
        return render(request, 'coqb/student_dashboard.html', {
            'name': name,
            'page': 'dashboard',
            'student_info': sections,
        })
    else:
        return signout(request)


@authenticated
def course_outline(request):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        course_outline_list = get_course_outline_list(auth_data.emp_id)
        return render(request, 'coqb/faculty_co_list.html', {
            'name': name,
            'page': 'co',
            'course_outline_list': course_outline_list,
        })
    elif auth_type == 'student':
        name = str(auth_data)
        co_info = get_co_info_student(auth_data.student_id)
        year = [i for i in range(int(YEAR)-4, int(YEAR))]
        return render(request, 'coqb/student_co.html', {
            'name': name,
            'page': 'co',
            'co_info': co_info,
            'year': year,
            'latest_year': YEAR,
        })
    else:
        return signout(request)


@authenticated
def add_course_outline(request):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        course_info = get_faculty_section_info(
            auth_data.emp_id, 's.section_pk')
        if request.method == 'POST':
            # print(request.POST)
            set_course_outline(request.POST)
            return render(request, 'coqb/faculty_co.html', {
                'name': name,
                'page': 'co',
                'course_info': course_info,
                'semester': SEMESTER,
                'year': YEAR,
                'is_submitted': 'true',
                'error': 'false',
            })
        else:
            return render(request, 'coqb/faculty_co.html', {
                'name': name,
                'page': 'co',
                'course_info': course_info,
                'semester': SEMESTER,
                'year': YEAR,
                'is_submitted': 'false',
                'error': 'false',
            })
    else:
        return signout(request)


@authenticated
def edit_course_outline(request, co_id):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        co_info = get_course_outline_info(co_id)
        # if request.method == 'POST':
        #     set_course_outline(request.POST)
        #     return render(request, 'coqb/faculty_co_edit.html', {
        #         'name': name,
        #         'page': 'co',
        #         'course_info': 'course_info',
        #         'semester': SEMESTER,
        #         'year': YEAR,
        #         'is_submitted': 'true',
        #         'error': 'false',
        #     })
        # else:
        return render(request, 'coqb/faculty_co_edit.html', {
            'name': name,
            'page': 'co',
            'co_info': co_info,
            'semester': SEMESTER,
            'year': YEAR,
            'is_submitted': 'false',
            'error': 'false',
        })
    else:
        return signout(request)


@authenticated
def question_bank(request):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        qb_list = get_qb_list(auth_data.emp_id)
        return render(request, 'coqb/faculty_qb_list.html', {
            'name': name,
            'page': 'qb',
            'qb_list': qb_list,
        })
    elif auth_type == 'student':
        name = str(auth_data)
        qb_info = get_co_info_student(auth_data.student_id)
        year = [i for i in range(int(YEAR)-4, int(YEAR))]
        return render(request, 'coqb/student_qb.html', {
            'name': name,
            'page': 'qb',
            'qb_info': qb_info,
            'year': year,
            'latest_year': YEAR,
        })
    else:
        return signout(request)


@authenticated
def add_question_bank(request):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        course_info = get_faculty_section_info(
            auth_data.emp_id, 's.section_pk')

        if request.method == 'POST':
            set_question(request.POST)
            return render(request, 'coqb/faculty_qb.html', {
                'name': name,
                'page': 'qb',
                'course_info': course_info,
                'semester': SEMESTER,
                'year': YEAR,
                'is_submitted': 'true',
                'error': 'false',
            })
        else:
            return render(request, 'coqb/faculty_qb.html', {
                'name': name,
                'page': 'qb',
                'course_info': course_info,
                'semester': SEMESTER,
                'year': YEAR,
                'is_submitted': 'false',
                'error': 'false',
            })
    elif auth_type == 'student':
        name = str(auth_data)
        return render(request, 'coqb/student_qb.html', {
            'name': name,
            'page': 'qb',
        })
    else:
        return signout(request)


@authenticated
def question_bank_qlist(request, section_id):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        qb_info = get_qb_list_info(section_id)
        return render(request, 'coqb/faculty_qb_list_q.html', {
            'name': name,
            'page': 'co',
            'qb_info': qb_info,
            'semester': SEMESTER,
            'year': YEAR,
            'is_submitted': 'false',
            'error': 'false',
        })
    elif auth_type == 'student':
        redirect('qb')
    else:
        return signout(request)


@authenticated
def edit_qb_view(request, qb_id):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        qb_info = edit_qb(qb_id)
        return render(request, 'coqb/faculty_qb_edit.html', {
            'name': name,
            'page': 'qb',
            'qb_info': qb_info,
            'semester': SEMESTER,
            'year': YEAR,
            'is_submitted': 'false',
            'error': 'false',
        })
    elif auth_type == 'student':
        redirect('qb')
    else:
        return signout(request)


@authenticated
def edit_qb_action(request):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        if request.method == 'POST':
            name = str(auth_data.emp)
            edit_qb_sql(request.POST)
            return render(request, 'coqb/faculty_qb_edit.html', {
                'name': name,
                'page': 'qb',
                'qb_info': '',
                'semester': SEMESTER,
                'year': YEAR,
                'is_submitted': 'true',
                'error': 'false',
            })
        else:
            redirect('qb')
    elif auth_type == 'student':
        redirect('qb')
    else:
        return signout(request)


@authenticated
def generate_co_pdf(request):
    if request.method == 'POST':
        data = get_all_co_data(request.POST.get('section'))
        format_data = [
            ['Course ID:', data[0]],
            ['Course Name:', data[1]],
            ['Section Number:', data[2]],
            ['Number of credits:', data[3]],
            ['Co-offered Courses:', data[4]],
            ['Semester:', request.POST.get('semester')],
            ['Year:', request.POST.get('year')],
            ['Course Type', 'Undergraduate' if data[5] == 'U' else 'Graduate'],
            ['Course Description', data[6]],
            ['Course Objective', data[7]],
            ['Course Policy', data[8]],
            ['Academic Dishonesty', data[9]],
            ['Non-Discrimination', data[10]],
            ['Student With Disability And Stress', data[11]],
            ['Course Requirement', data[12]],
            ['Course Content', data[13]],
            ['Assessment and Evaluation', data[14]],
            ['Reference', data[15]],
        ]

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
        p.setFont('Helvetica', 25)
        text = p.beginText()
        text.setTextOrigin(inch, inch)
        text.textLine('Course Outline')
        p.drawText(text)
        f = Table(format_data[::-1])
        f.wrapOn(p, 1, 1)
        f.drawOn(p, inch, inch + 50)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='course_outline.pdf')
    else:
        return redirect('co')


@authenticated
def generate_qb_pdf(request):
    if request.method == 'POST':
        section_id = request.POST.get('section')
        section = Section_T.objects.get(section_pk=section_id)
        format_data = [
            ['Course ID:', section.course.course_id],
            ['Course Name:', section.course.course_name],
            ['Section Number:', section.section_no],
        ]
        data = [['No.', 'Marks', 'Question']]
        data = data + get_all_qb_data(section_id)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
        p.setFont('Helvetica', 25)
        text = p.beginText()
        text.setTextOrigin(inch, inch)
        text.textLine('Question Bank')
        p.drawText(text)
        f = Table(format_data[::-1])
        f.wrapOn(p, 1, 1)
        f.drawOn(p, inch, inch + 50)
        f2 = Table(data[::-1])
        f2.wrapOn(p, 1, 1)
        f2.drawOn(p, inch, inch + 120)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='question_bank.pdf')
    else:
        return redirect('qb')


@authenticated
def profile(request):
    auth_type, auth_data = authorize(request)

    if auth_type == 'faculty':
        name = str(auth_data.emp)
        dept = auth_data.emp.dept.dept_name
    elif auth_type == 'student':
        name = str(auth_data)
        dept = auth_data.department.dept_name
    else:
        name = ''

    return render(request, 'coqb/profile.html', {
        'name': name,
        'dept': dept,
    })
