#!/usr/bin/python3
import sys
import pandas as pd
'''https://github.com/ucfopen/canvasapi'''
from canvasapi import Canvas

'''This imports the API_KEY and API_URL from the canvas_config.py file'''
from canvas_config import *


'''Course id is in your url https://yourschool.instructure.com/courses/{Course_ID}'''
COURSE_ID = 254 # Type int
ASSIGN_ID = 1929
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
		
		post_grade_and_comment(course,row["Student_ID"],row["Grade"],row["Comment"])
		
	
def post_grade_and_comment(course, st_id, grade, comment, is_group_cmt = True):
	data = {"comment[text_comment]": str(comment) ,
			"comment[group_comment]": bool(is_group_cmt),
			"submission[posted_grade]": str(grade) }

	response = course.update_submission(ASSIGN_ID,st_id,**data)	

if __name__ == '__main__':
	main()
