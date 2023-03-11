import os
import pandas as pd
from coqb.models import Employee_T, Faculty_T, Course_T, Section_T

os.chdir('scripts')

data = pd.read_csv('summer_2021_tally_sheet.csv')
data = data[['COFFER_COURSE_ID', 'SECTION', 'ROOM_ID',
             'FACULTY_FULL_NAME', 'STRAT_TIME', 'END_TIME', 'ST_MW']]
data = data.drop_duplicates()
data = data.values.tolist()
data = data[:len(data)-1]

for course, section, room, faculty, start, end, day in data:
    faculty = faculty.split('-')[0]
    section = Section_T(section_no=section,
                        course=Course_T.objects.get(course_id=course),
                        room=room,
                        faculty=Faculty_T.objects.get(
                            emp=Employee_T.objects.get(emp_id=faculty)),
                        start_time=start,
                        end_time=end,
                        day=day,
                        semester='Au',
                        year='2022')
    section.save()
