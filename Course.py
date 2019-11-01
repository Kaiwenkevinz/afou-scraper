class Course():
    def __init__(self, class_id, section, days, times, location, open_seats, instructor):
        self.class_id = class_id
        self.section = section
        self.days = days
        self.times = times
        self.location = location
        self.open_seats = open_seats
        self.instructor = instructor

    

    def __str__(self):
        return self.section + ' ' + self.days + ' ' + self.times
