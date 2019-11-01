import itertools

course_infos = [[['M W F', '11:00AM - 11:50AM'], ['M W F', '2:00PM - 2:50PM'], ['T R', '2:00PM - 3:20PM'], ['T R', '9:30AM - 10:50AM'], ['T', '5:00PM - 8:00PM']], [['M W F', '9:00AM - 9:50AM'], ['M W F', '11:00AM - 11:50AM'], ['M W F', '1:00PM - 1:50PM'], ['T R', '3:30PM - 4:50PM'], ['R', '6:30PM - 9:30PM'], ['T R', '9:30AM - 10:50AM']]]

def test():
    for i in itertools.product(*course_infos):
        print (i)

test()