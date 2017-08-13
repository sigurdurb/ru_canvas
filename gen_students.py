#!/usr/bin/python3

'''https://github.com/ucfopen/canvasapi'''
from canvasapi import Canvas

'''This imports the API_KEY and API_URL from the canvas_config.py file'''
from canvas_config import *

'''
This script main function as a standalone can either call the
get_users(course) : returns all students and teachers/TA's and other people affiliated
get_students(course) : returns only those with enrollment_type=student
'''

'''Course id is in your url https://yourschool.instructure.com/courses/{Course_ID}'''
COURSE_ID = 254 # Type int

def main():
	canvas = Canvas(API_URL, API_KEY)
	# First, retrieve the Course object
	course = canvas.get_course(COURSE_ID)

	users = get_students(course)

	for user in users:
	    # print (user.to_json()) # This calls the to_json method inside super canvasapi/canvasobject.py
	    # print(user.__repr__()) # This calls the __repr__ method inside super canvasobject.py and leaves nothing behind
	    # print(user) # This calls the __str__ method for the User object(see canvasapi/user.py) that prints out only name and id
	    print(user.id, end=" ") # could also print user.name
	    try:
			print(user.login_id) # The beginning of the schools mail address
		
		except AttributeError: 
			print("\nError: No login_id for:", user.id, user.name,"or your account does not have rights to view this content, Contact admin")
		


def get_users(course):

	# Grab all users in the course
	users = course.get_users()
		

def get_students(course):

	# Grab all users from a course with the 'student' enrollment type
	param = {"enrollment_type": "student"}
	st_users = course.get_users(**param)

	return st_users
	
if __name__ == '__main__':
	main()
