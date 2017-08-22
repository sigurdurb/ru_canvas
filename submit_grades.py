#!/usr/bin/python3
import sys
'''https://github.com/ucfopen/canvasapi'''
from canvasapi import Canvas

'''This imports the API_KEY and API_URL from the canvas_config.py file'''
from canvas_config import *


'''Course id is in your url https://yourschool.instructure.com/courses/{Course_ID}'''
COURSE_ID = 123 # Type int
ASSIGN_ID = 123
CSV_FILE = sys.argv[1]
def main():
	# Here is an example
	canvas = Canvas(API_URL, API_KEY)
	# First, retrieve the Course object
	course = canvas.get_course(COURSE_ID)
	
	df = pd.read_csv(CSV_FILE)

	post_grades(course, df)

def post_grades(course, df):

	for index, row in df.iterrows():
	
		data = {"comment[text_comment]": row["Comment"] ,
				"comment[group_comment]":True,
				"submission[posted_grade]":row["Grade"]
				}
		st_id = row["Student_ID"]

		response = course.update_submission(ASSIGN_ID,st_id,**data)
	
		

if __name__ == '__main__':
	main()
