import os
import pandas as pd
from coqb.models import Course_T, Program_T

os.chdir('scripts')

data = pd.read_csv('summer_2021_tally_sheet.csv')
data = data[['COFFER_COURSE_ID', 'SCHOOL_TITLE', 'COFFERED_WITH', 'CREDIT_HOUR', 'COURSE_NAME']]
data = data.drop_duplicates()
data = data.values.tolist()

for course, school, cooffered, credit, name in data:
    new_course = Course_T(course_id=course,
                          course_name=name,
                          program=Program_T.objects.get(program_id=course[:3]),
                          co_offered_courses=cooffered,
                          no_of_credits=credit)
    new_course.save()
