"""
Contributor: Min Joon So
Date: 04 Feb 2018
"""

class hour:
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
            :param candidate <class stdudent> student to add to an hour.
        add the new candidate and take out least wanted candidate'''
        self._add_candidate(candidate)
        if self._is_over():
            self.workers = self.workers[:-1]
            self.workers[-1].taken[self] = False
            
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
                
            
class candidate:
    def __init__(self, name):
        self.name = name
        self.preferences = []

    @property
    def taken(self):
        '''updates taken according to preferences
        return: dictionary of preferences <class hour> as keys and availability <bool> as values'''
        taken = {}
        for preference in self.preferences:
            print(preference.name)
            taken[preference] = False
        return taken

class match:
    def __init__(self):
        self.students = []
        self.hours = []
    
    def add_student(self, student):
        self.students.append(student)
    
    def add_hour(self, hour):
        self.hours.append(hour)
    
    def assign(self):
        '''
        assigns each candidate's [preference] to [hours]
        '''
        students = self.students
        hours = self.hours
        
        finished = False
        while not finished:
            finished = True
            for student in students:
                for preference in student.preferences:
                    if student.taken[preference] == False:
                        preference.try_matching(student)

if __name__ == '__main__':
    h0 = hour('h0', 2)   
    h1 = hour('h1', 2)
    
    c0 = candidate('c0')    
    c1 = candidate('c1')    
    c2 = candidate('c2')    
    c3 = candidate('c3')    
    
    h0.preferences = [c3,c1,c2,c0]
    h1.preferences = [c1,c2,c0,c3]
    
    c0.preferences = [h0, h1]
    c1.preferences = [h1, h0]
    c2.preferences = [h0, h1]
    c3.preferences = [h1, h0]
    
    students = [c0, c1, c2, c3]
    hours = [h0]
    
    new_match = match()
    for x in students:
        new_match.add_student(x)
    for y in hours:
        new_match.add_hour(y)
    new_match.assign()

    