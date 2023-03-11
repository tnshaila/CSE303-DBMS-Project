from django.db import connection
from django.db import IntegrityError

SEMESTER = 'Au'
YEAR = '2022'


def get_faculty_section_info(emp_id, args=''):
    if args:
        args = f', {args}'
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT c.course_id, c.course_name, s.section_no, s.start_time, s.day{}
            FROM coqb_employee_t e, coqb_faculty_t f, coqb_section_t s, coqb_course_t c
            WHERE e.emp_id = '{}'
            AND f.emp_id = e.emp_id
            AND s.faculty_id = f.faculty_pk
            AND c.course_id = s.course_id
            AND s.semester = '{}'
            AND s.year = '{}';
        '''.format(args, emp_id, SEMESTER, YEAR))
        return cursor.fetchall()


def set_course_outline(args):
    section_id = args.get('section')
    reference = args.get('reference')
    academic_dishonesty = args.get('dishonesty')
    assesment_evaluation_section = args.get('assessment')
    course_content = args.get('course_content')
    course_description = args.get('course_description')
    course_obj = args.get('course_objective')
    course_policy = args.get('course_policy')
    course_requrement = args.get('requirement')
    course_type = args.get('course_type')
    non_discrimination = args.get('discrimination')
    student_disability = args.get('disability')
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO coqb_courseoutline_t('section_id',
                                                 'reference',
                                                 'academic_dishonesty',
                                                 'assesment_evaluation_section',
                                                 'course_content',
                                                 'course_description',
                                                 'course_obj',
                                                 'course_policy',
                                                 'course_requrement',
                                                 'course_type',
                                                 'non_discrimination',
                                                 'student_disability')
                VALUES('{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}');
            '''.format(section_id,
                       reference,
                       academic_dishonesty,
                       assesment_evaluation_section,
                       course_content,
                       course_description,
                       course_obj,
                       course_policy,
                       course_requrement,
                       course_type,
                       non_discrimination,
                       student_disability))
    except IntegrityError:
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE coqb_courseoutline_t
                SET reference = '{}',
                    academic_dishonesty = '{}',
                    assesment_evaluation_section = '{}',
                    course_content = '{}',
                    course_description = '{}',
                    course_obj = '{}',
                    course_policy = '{}',
                    course_requrement = '{}',
                    course_type = '{}',
                    non_discrimination = '{}',
                    student_disability = '{}'
                WHERE
                    section_id = '{}';
            '''.format(reference,
                       academic_dishonesty,
                       assesment_evaluation_section,
                       course_content,
                       course_description,
                       course_obj,
                       course_policy,
                       course_requrement,
                       course_type,
                       non_discrimination,
                       student_disability,
                       section_id))


def set_question(args):
    section_id = args.get('course_info')
    question = args.get('question')
    marks = args.get('marks')
    with connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO coqb_questionbank_t('section_id',
                                            'question',
                                            'marks')
            VALUES('{}',
                    '{}',
                    '{}');
        '''.format(section_id, question, marks))


def get_course_outline_list(emp_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT co.section_id, c.course_id, c.course_name, s.section_no, s.semester, s.year
            FROM coqb_course_t c,
                coqb_section_t s,
                coqb_faculty_t f,
                coqb_employee_t e,
                coqb_courseoutline_t co
            WHERE c.course_id = s.course_id
            AND s.faculty_id = f.faculty_pk
            AND f.emp_id = e.emp_id
            AND e.emp_id = '{}'
            AND co.section_id = s.section_pk;
        '''.format(emp_id))

        return cursor.fetchall()


def get_course_outline_info(co_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT co.section_id,
                   c.course_id,
                   c.course_name,
                   s.section_no,
                   s.semester,
                   s.year,
                   co.course_type,
                   co.course_description,
                   co.course_obj,
                   co.course_policy,
                   co.academic_dishonesty,
                   co.non_discrimination,
                   co.student_disability,
                   co.course_requrement,
                   co.course_content,
                   co.assesment_evaluation_section,
                   co.reference
            FROM coqb_course_t c,
                 coqb_section_t s,
                 coqb_courseoutline_t co
            WHERE c.course_id = s.course_id
            AND co.section_id = s.section_pk
            AND co.section_id = '{}';
        '''.format(co_id))
        return cursor.fetchone()


def get_qb_list(emp_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT qb.section_id,
                   c.course_id,
                   c.course_name,
                   s.section_no,
                   s.semester,
                   s.year
            FROM coqb_course_t c,
                 coqb_section_t s,
                 coqb_faculty_t f,
                 coqb_employee_t e,
                 coqb_questionbank_t qb
            WHERE c.course_id = s.course_id
            AND s.faculty_id = f.faculty_pk
            AND f.emp_id = e.emp_id
            AND e.emp_id = '{}'
            AND qb.section_id = s.section_pk
            GROUP BY qb.section_id,
                     c.course_id,
                     c.course_name,
                     s.section_no,
                     s.semester,
                     s.year;
        '''.format(emp_id))
        
        return cursor.fetchall()

def get_qb_list_info(section_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT qb.qb_id,
                   ROW_NUMBER() OVER(ORDER BY (SELECT 1))
            FROM coqb_questionbank_t qb
            WHERE qb.section_id = '{}';
        '''.format(section_id))
        
        return cursor.fetchall()
        
        
def edit_qb(qb_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT qb.qb_id, c.course_id, c.course_name, s.section_no, qb.question, qb.marks
            FROM coqb_questionbank_t qb,
                 coqb_course_t c,
                 coqb_section_t s
            WHERE qb.qb_id = '{}'
            AND qb.section_id = s.section_pk
            AND s.course_id = c.course_id;
        '''.format(qb_id))
        
        return cursor.fetchone()
        
        
def edit_qb_sql(args):
    with connection.cursor() as cursor:
        cursor.execute('''
            UPDATE coqb_questionbank_t
            SET question = '{}',
                marks = '{}'
            WHERE qb_id = '{}';
        '''.format(args.get('question'),
                   args.get('marks'),
                   args.get('qb_id')))


def get_co_info_student(student_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT se.section_pk, c.course_id, c.course_name, se.section_no
            FROM coqb_registration_t r,
                 coqb_student_t st,
                 coqb_section_t se,
                 coqb_course_t c
            WHERE r.student_id = st.student_id
            AND r.section_id = se.section_pk
            AND se.course_id = c.course_id
            AND st.student_id = '{}';
        '''.format(student_id))
        
        return cursor.fetchall()


def get_all_co_data(section_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT c.course_id,
                   c.course_name,
                   se.section_no,
                   c.no_of_credits,
                   c.co_offered_courses,
                   co.course_type,
                   co.course_description,
                   co.course_obj,
                   co.course_policy,
                   co.academic_dishonesty,
                   co.non_discrimination,
                   co.student_disability,
                   co.course_requrement,
                   co.course_content,
                   co.assesment_evaluation_section,
                   co.reference
            FROM coqb_registration_t r,
                 coqb_student_t st,
                 coqb_section_t se,
                 coqb_course_t c,
                 coqb_courseoutline_t co
            WHERE r.student_id = st.student_id
            AND r.section_id = se.section_pk
            AND se.course_id = c.course_id
            AND co.section_id = se.section_pk
            AND se.section_pk = '{}';
        '''.format(section_id))
        
        return cursor.fetchone()
        

def get_all_qb_data(section_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT ROW_NUMBER() OVER(ORDER BY (SELECT 1)),
                   qb.marks,
                   qb.question
            FROM coqb_questionbank_t qb
            WHERE qb.section_id = '{}';
        '''.format(section_id))
        
        return cursor.fetchall()
