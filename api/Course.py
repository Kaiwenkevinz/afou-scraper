from datetime import datetime
from collections import namedtuple

class Course(object):
    def __init__(self, course, class_id, section, days, times, location, open_seats, instructor):
        self.class_id = class_id
        self.course = course
        self.section = section
        self.days = days
        self.times = times
        self.location = location
        self.open_seats = open_seats
        self.instructor = instructor

    # self == other  --> overlap
    def __eq__(self, other): 
        t1 = [self.days, self.times]
        t2 = [other.days, other.times]

        days1 = t1[0]
        days2 = t2[0]

        if days1 != days2 and (days1 not in days2) and (days2 not in days1):
            return False
        
        Range = namedtuple('Range', ['start', 'end'])

        tp1 = t1[1].split(" - ")
        tp2 = t2[1].split(" - ")

        tp1_a = tp1[0]
        tp1_b = tp1[1]

        tp2_a = tp2[0]
        tp2_b = tp2[1]

        FMT = '%I:%M%p'
        tp1_a_obj = datetime.strptime(tp1_a, FMT)
        tp1_b_obj = datetime.strptime(tp1_b, FMT)
        tp2_a_obj = datetime.strptime(tp2_a, FMT)
        tp2_b_obj = datetime.strptime(tp2_b, FMT)

        r1 = Range(start=tp1_a_obj, end=tp1_b_obj)
        r2 = Range(start=tp2_a_obj, end=tp2_b_obj)

        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        time_delta = latest_start - earliest_end

        if time_delta.days < 0:
            return True
        else:
            return False

    def __str__(self):
        return self.course + ' ' + self.days + ' ' + self.times