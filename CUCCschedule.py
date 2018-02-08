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
            candidate.work_hour += 1
            if self._is_over():
                dropped_worker = self.workers[-1]
                dropped_worker.taken[self] = False
                dropped_worker.work_hour -= 1
                self.workers = self.workers[:-1]            
    #            return candidate == rejected_worker
    #        return True
                
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
            self.work_hour = 0
            self.points = 0
    
        @property
        def taken(self):
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
        
        def add_student(self, student):
            self.students.append(student)
        
        def add_hour(self, hour):
            self.hours.append(hour)
        
        def assign(self):
            '''
            assigns each candidate's [preference] to [hours]
            '''
            students = self.students        
    #        finished = False
    #        while not finished:
    #            finished = True
            for student in students:
                print("------",student.name,"------")
                for preference in student.preferences:
                    print("------", preference.name,"------")
                    if not student.taken[preference]:
                        print("*",preference.name,"preference: ")
                        preference.preferences = self.calculate_preference(preference)
                        preference.try_matching(student)
    #                        if not preference.try_matching(student):
    #                            finished = False
        
        def calculate_preference(self, hour):
            '''
            :para [hour]: <class hour> orders preferred students
            return: preference list
            '''
            for student in self.students:
                student.points = 0
                student.points += self.calculate_hours_taken(student)
                student.points += self.calculate_consecutive(student, hour)
    #            print(student.name, "has score", student.points)
            return self.sort_preference()
    
        def sort_preference(self):
            '''
            *sorts students based on their points
            return: preference list of students
            '''
            preference_list = []
            for student in self.students:
                preference_list.append((student, student.points))
            preference_list.sort(key=takeSecond, reverse=True)
            for x in preference_list:
                print(x[0].name,x[1])
            return [i[0] for i in preference_list]
            
        def calculate_hours_taken(self, student):
            ''' returns points based on how many hours the student has taken'''
            return 20 - student.work_hour
        
        def calculate_consecutive(self, student, hour):
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
        h0 = hour('h0', 2)   
        h1 = hour('h1', 2)
        h2 = hour('h2', 2)   
        h3 = hour('h3', 2)
        
        c0 = candidate('c0')    
        c1 = candidate('c1')    
        c2 = candidate('c2')    
        c3 = candidate('c3')    
        
    #    h0.preferences = [c3,c1,c2,c0]
    #    h1.preferences = [c1,c2,c0,c3]
        
        c0.preferences = [h0, h1]
        c1.preferences = [h1, h0]
        c2.preferences = [h0, h1]
        c3.preferences = [h1, h0]
        
        students = [c0, c1, c2, c3]
        hours = [h0,h1,h2,h3]
        
        new_match = match()
        for x in students:
            new_match.add_student(x)
        for y in hours:
            new_match.add_hour(y)
        new_match.assign()
        
    #    for x in h1.workers:
    #        print(x.name)
        
    
        
