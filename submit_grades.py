#!/usr/bin/python3
import sys
import pandas as pd
'''https://github.com/ucfopen/canvasapi'''
from canvasapi import Canvas

'''This imports the API_KEY and API_URL from the canvas_config.py file'''
from canvas_config import *


'''Course id is in your url https://yourschool.instructure.com/courses/{Course_ID}'''
COURSE_ID = 254 # Type int
ASSIGN_ID = 3049
CSV_FILE = sys.argv[1]

def main():
	# Here is an example
	canvas = Canvas(API_URL, API_KEY)
	# First, retrieve the Course object
	course = canvas.get_course(COURSE_ID)
	
	df = pd.read_csv(CSV_FILE, index_col="Nr")

	submit_grades(course, df)

	print("Successfully submitted all new grades")

def submit_grades(course, df):

	hasCmt = True if 'Comment' in df.columns else False
	comment = ""
	for index, row in df.iterrows():
		if hasCmt:
			comment = row["Comment"]
		put_grade_and_comment(course,row["Student_ID"], row["Grade"], comment, True, row["Student"])
		

def put_grade_and_comment(course, user_id, grade, comment, is_group_cmt = True, user_name = ""):
    # If comment is an empty string/space Canvas will only put the new grade, so no need to have a special case.
    data = {"comment[text_comment]": str(comment),
            "comment[group_comment]": bool(is_group_cmt),
            "submission[posted_grade]": str(grade) }
    
    sub_resp = course.update_submission(ASSIGN_ID,user_id,**data) 

    
    
    print("Successfully updated user: ", user_name,'\t',sub_resp.user_id, "with grade:", sub_resp.grade)


if __name__ == '__main__':
	main()
