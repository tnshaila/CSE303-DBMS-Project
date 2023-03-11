import os
import pandas as pd
from django.contrib.auth.models import User
from coqb.models import Employee_T, Faculty_T, Department_T

os.chdir('scripts')

data = pd.read_csv('summer_2021_tally_sheet.csv')
data = data['FACULTY_FULL_NAME']
data = data.drop_duplicates()
data = data.str.split('-')
data = data.values.tolist()
data = data[:len(data)-1]

for faculty_id, faculty_name in data:
    faculty_name = faculty_name.split(' ')
    f_name = faculty_name[0]
    l_name = faculty_name[-1]
    user = User.objects.create_user(faculty_id, password='345123aa')
    user.save()
    employee = Employee_T(emp_id=faculty_id,
                          f_name=f_name,
                          l_name=l_name,
                          dept=Department_T.objects.get(dept_id='CSE'),
                          user=user)
    employee.save()
    faculty = Faculty_T(emp=employee, rank='L')
    faculty.save()
