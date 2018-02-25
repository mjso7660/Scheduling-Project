import cucc
import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("cucc scheduling").sheet1
all_values = sheet.get_all_values()

def create_hours():
    hours = []
    hour_dict = {}
    row = 11
    while row < len(all_values) and all_values[row][1] != '':
        new_hour = cucc.Hour(all_values[row][2],int(all_values[row][1]))
        hours.append(new_hour)
        hour_dict[all_values[row][2]] = new_hour
        row += 1
    return hours, hour_dict

def create_students(hour_dict):
    """
    return: candidate list
    """
    student_list = []
    row = 0
    while all_values[row][0] != '':
        preferences = []
        col = 1
        while col < len(all_values[row]) and all_values[row][col] != '':
            preferences.append(hour_dict[all_values[row][col]])
            col += 1
        new_student = cucc.Candidate(all_values[row][0],preferences)
        student_list.append(new_student)
        row += 1
    return student_list

def update_cells(students, hours):
    for x in range(len(hours)):
        hour = hours[x]
        cell_list = sheet.range(12+x, 4, 12+x, 3 + hour.slot)
        for y in range(len(cell_list)):
            try:
                cell_list[y].value = hour.workers[y].name
            except IndexError:
                continue
        sheet.update_cells(cell_list)
        
        
