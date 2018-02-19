"""
Contributor: Min Joon So
Date: 04 Feb 2018
"""
import spreadsheet

class Hour:
    def __init__(self, name, slot):
        '''
        :param slot <int> number of slots
        workers <class student> - workers assigned
        preference <class student> - preference of students
        '''
        self.slot = slot
        self.name = name
        self.preferences = []
        self.workers = [] 
    
    def get_slot(self):
        '''return slot number'''
        return self.slot
    
    def get_preference(self):
        return self.preferences
    
    def get_workers(self):
        return self.workers
    
    def _is_full(self):
        '''return: true is full, false if not full'''
        if len(self.workers) == self.slot:
            return True
        return False
    
    def _is_over(self):
        '''return: true is over, false if not'''
        if len(self.workers) > self.slot:
            return True
        return False
    
    def try_matching(self, candidate):
        '''
        add the new candidate and take out least wanted candidate
        
        param candidate <class stdudent> student to add to an hour.
        return: True if candidate is matched, False othrwise
        '''
        self._add_candidate(candidate)
        candidate.work_hour += 1
        if self._is_over():
            dropped_worker = self.workers[-1]
            dropped_worker.taken[self] = False
            dropped_worker.work_hour -= 1
            self.workers = self.workers[:-1]
            if candidate != dropped_worker:
                print(candidate.name, "picked up", self.name, "/", dropped_worker.name, "dropped")
            return candidate != dropped_worker
        print(candidate.name, "picked up", self.name)
        return True
            
    def _add_candidate(self, candidate):
        ''' adds candidate to worker array'''
        workers = self.get_workers()
        preference = self.get_preference()
        #chekc if candidate is in the preference list
        try:
            preference.index(candidate)
        except ValueError:
            print(candidate.name,"candidate not found in a preference list")
            return
        #add candidate to worker list and reorder the list
        workers.append(candidate)
        for x in range(2,len(workers)+1):
            if preference.index(workers[-x]) > preference.index(workers[-x+1]):
                workers[-x], workers[-x+1] = workers[-x+1], workers[-x]
            else:
                break
                
            
class Candidate:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences
        self.work_hour = 0
        self.points = 0
        self.taken = self.get_taken()
        
    def get_taken(self):
        '''initializes 'taken' according to preferences
        return: dictionary of preferences <class hour> as keys and availability <bool> as values'''
        taken = {}
        for preference in self.preferences:
            taken[preference] = False
        return taken

class match:
    def __init__(self):
        self.students = []
        self.hours = []

    @property
    def count(self):
        count = 0
        for worker in self.hours:
            count += len(worker.get_workers())
        return count
    
    def add_student(self, student):
        self.students.append(student)
    
    def add_hour(self, hour):
        self.hours.append(hour)
    
    def _build_preference(self):
        for student in self.students:
            for hour in student.preferences:
                hour.preferences.append(student)
    
    def assign_until(self):
        self._build_preference()
        round = 0
        cnt = 0
        while True:
            count = self.count
            self._assign()
            round += 1
            print("test:", count, self.count)
            if count == self.count:
                return
#                cnt += 1
#                if cnt > 10:
#                    return
    
    def _assign(self):
        '''
        assigns each candidate's [preference] to [hours]
        return: None
        '''
        students = self.students        
        for student in students:
            print("------",student.name,"------")
            for hour in student.preferences:
                print("------", hour.name,"------")
                if not student.taken[hour]:
                    print("*",hour.name,"preference: ")
                    hour.preferences = self._calculate_preference(hour)
#                    print(self._slot_left(hour),self._student_with_same_point(hour, student))
                    if hour.slot >= self._student_with_same_point(hour, student):
                        if hour.try_matching(student):
                            student.taken[hour] = True
                        
    def _student_with_same_point(self, hour, student):
        cnt = 0
        try:
            index = hour.preferences.index(student)
        except:
            print("error")
            return
        temp = index
        while True:
            if temp>0 and student.points == hour.preferences[temp-1].points:
                cnt += 1
                temp -= 1
            else: 
                break
        temp = index
        while True:
            if temp+1 < len(hour.preferences) and student.points == hour.preferences[temp+1].points:
                cnt += 1
                temp += 1
            else:
                break
        return cnt+1
        
    def _slot_left(self,hour):
        return hour.slot - len(hour.workers)
    
    def _sort_preference(self, hour):
        '''
        *sorts students based on their points
        return: ordered preference list of students
        '''
        preference_list = []
        for student in hour.preferences:
            preference_list.append((student, student.points))
        preference_list.sort(key=takeSecond, reverse=True)
        for x in preference_list:
            print(x[0].name,x[1])
        return [i[0] for i in preference_list]

    def _calculate_preference(self, hour):
        '''
        :para [hour]: <class hour> orders preferred students
        return: preference list
        '''
        for student in self.students:
            student.points = 0
            student.points += self._calculate_hours_taken(student)
            student.points += self._calculate_consecutive(student, hour)
        return self._sort_preference(hour)
        
    def _calculate_hours_taken(self, student):
        ''' returns points based on how many hours the student has taken'''
        return 20 - student.work_hour
    
    def _calculate_consecutive(self, student, hour):
        ''' returns points based on consecutive hours'''
        point = 0
        n_th = 1
        hours = self.hours
        while hours.index(hour) - n_th >= 0 and student in hours[hours.index(hour)-n_th].workers:
            point += 30
            n_th += 1
        n_th = 1
        while hours.index(hour) + n_th < len(hours) and student in hours[hours.index(hour)+n_th].workers:
            point += 30
            n_th += 1
        return point

#Util Functions        
def takeSecond(elem):
    return elem[1]

if __name__ == '__main__':
#    h0 = Hour('h0', 3)   
#    h1 = Hour('h1', 3)
#    h2 = Hour('h2', 4)   
#    h3 = Hour('h3', 5)
#    h4 = Hour('h4', 5)
#    h5 = Hour('h5', 4)
#    h6 = Hour('h6', 3)
#    
#    c0_pref = [h0,h1,h2,h3]
#    c1_pref = [h0,h1,h4,h5]
#    c2_pref = [h4,h5,h6]
#    c3_pref = [h5,h6]
#    c4_pref = [h0, h1, h2]
#    c5_pref = [h1,h2,h3]
#    c6_pref = [h1,h2,h3]
#    c7_pref = [h1,h2,h3,h4]
#    c8_pref = [h3,h4,h5,h6]
#    c9_pref = [h2,h3]
#    c10_pref = [h1,h2,h3]
#    c11_pref = [h0,h1,h4,h5]
#    
#    c0 = Candidate('c0', c0_pref)    
#    c1 = Candidate('c1', c1_pref)    
#    c2 = Candidate('c2', c2_pref)    
#    c3 = Candidate('c3', c3_pref)    
#    c4 = Candidate('c4', c4_pref)    
#    c5 = Candidate('c5', c5_pref) 
#    c6 = Candidate('c6', c6_pref)
#    c7 = Candidate('c7', c7_pref)
#    c8 = Candidate('c8', c8_pref)
#    c9 = Candidate('c9', c9_pref)
#    c10 = Candidate('c10', c10_pref)
#    c11 = Candidate('c11', c11_pref)
    
#    students = [c0, c1, c2, c3, c4, c5, c6, c7,c8,c9,c10,c11]
#    hours = [h0,h1,h2,h3,h4,h5,h6]
    hours, hour_dict = spreadsheet.create_hours()
    students = spreadsheet.create_students(hour_dict)
    
    new_match = match()
    for x in students:
        new_match.add_student(x)
    for y in hours:
        new_match.add_hour(y)
    new_match.assign_until()
    
    spreadsheet.update_cells(students, hours)
    
#    print("---h0 workers----")
#    for x in h0.workers:
#        print(x.name)
#    print("---h1 workers----")
#    for x in h1.workers:
#        print(x.name)
#    print("---h2 workers----")
#    for x in h2.workers:
#        print(x.name)
#    print("---h3 workers----")
#    for x in h3.workers:
#        print(x.name)
#    print("---h4 workers----")
#    for x in h4.workers:
#        print(x.name)
#    print("---h5 workers----")
#    for x in h5.workers:
#        print(x.name)
#    print("---h6 workers----")
#    for x in h6.workers:
#        print(x.name)