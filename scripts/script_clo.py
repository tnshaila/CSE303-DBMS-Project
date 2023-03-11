import os
import pandas as pd
from coqb.models import Course_T, Program_T, PLO_T, CLO_T

os.chdir('scripts')

data = pd.read_csv('summer_2021_tally_sheet.csv')
data = data['COFFER_COURSE_ID']
data = data.drop_duplicates()
data = data.values.tolist()

for course in data:
    for clo_no in range(1, 7):
        clo_description = f'CLO {clo_no}'
        clo = CLO_T(clo_no=clo_no,
                    course=Course_T.objects.get(course_id=course),
                    description=clo_description,
                    plo=PLO_T.objects.get(plo_no=clo_no, program=Program_T.objects.get(program_id='CSE')))
        clo.save()
