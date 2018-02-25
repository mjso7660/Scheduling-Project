import cucc
import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet1 = client.open("cucc scheduling").sheet1
sheet2 = client.open("cucc scheduling").get_worksheet(2)

all_values = sheet1.get_all_values()
all_values2 = sheet2.get_all_values()

def create_hours():
    """
    creates hours based off from hours listed on the google spreadsheet
    return: hours: list of hours / hour_dict: dictionary where key = hour.name, value = class Hour
    """
    hours = []
    hour_dict = {}
    row,col = 2, 0
    while col < len(all_values2[0]):
        while row < len(all_values2) and all_values2[row][0] != 'End':
            if all_values2[row][col+1] == '':
                row += 1
                continue
            hour_name = all_values2[0][col] + all_values2[row][col]
            print(hour_name)
            new_hour = cucc.Hour(hour_name,int(all_values2[row][col+1]))
            hours.append(new_hour)
            hour_dict[hour_name] = new_hour
            row += 1
        empty_hour = cucc.Hour('empty',0)
        hours.append(empty_hour)
        #for weekends
        if col > 25:
            col += 4
        else:
            col += 6
        row = 2
    hour_dict['empty'] = None
    return hours, hour_dict

def create_students(hour_dict):
    """
    creates a list of students, each an instance of class Candidate 
    return: candidate array
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

def update_cells(hours):
    """
    updates cells based on students assigned from cucc.py, each day at a time
    return: None
    """
    
    cell_list = sheet2.range(3,3,17,6)
    index = 0
    while index < len(cell_list): 
        for worker in hours[index//4].workers:
            cell_list[index].value = worker.name
            index += 1
        while index%4 != 0:
            index+= 1
    sheet2.update_cells(cell_list)
        
if __name__ == '__main__':
    pass
