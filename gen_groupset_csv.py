#!/usr/bin/python3

from canvasapi import Canvas
'''This imports the API_KEY and API_URL from the canvas_config.py file'''
from canvas_config import *
import pandas as pd


'''Course id is in your url; example: https://yourschool.instructure.com/courses/{Course_ID}'''
COURSE_ID = 254 # type int - a number like 254

'''This is the groups-set/category name, Note: not the assignment-group
This category name is on the tabs of YourCourse->People page or url:yourcanvasinstance.com/courses/{course_id}/users'''
GROUP_CATGR_NAME = "V1-Group" # Insert your group set/category name here

TO_CSV_FILE = "groupset_" + GROUP_CATGR_NAME + "_details.csv"

# Set CSV up with a template for grades and comments:
# ..or set these variables to None if you dont want the extra column
GRADES = .0
COMMENTS = '''01. 0/5
02. 0/3
03. 0/2'''

def gen_groupset_csv():

	# Set up our Canvas object
	canvas = Canvas(API_URL, API_KEY)

	# First, retrieve the Course object
	course = canvas.get_course(COURSE_ID)

	# Print the course's name
	print(course.name, course.id)

	list_of_group_cats = get_group_categories(course)

	possible_groups = []
	all_rows = []
	for group_cat in list_of_group_cats:
		possible_groups.append(group_cat.name)
		if group_cat.name == GROUP_CATGR_NAME:
			
			#print(group_cat.to_json())
			groups = list_groups_in_group_category(course,group_cat.id)
			for g in groups:
				#print(g.to_json())
				
				'''list_membership also returns the id's of users for a group, but not their names'''
				'''So instead we use list_users'''
				#membership = g.list_membership()
				users_in_group = g.list_users()
				for u in users_in_group:
					row = []
					row.extend([group_cat.name, group_cat.id, g.name, g.id, u.name, u.id])
					
					all_rows.append(row)
					#print(u.to_json())

	if all_rows:
		df = pd.DataFrame(all_rows, columns=['GroupSet', 'GroupSetID', 'Group', 'GroupID', 'Student', 'StudentID'])
		if GRADES is not None:
			df["Grade"] = GRADES
		if COMMENTS is not None:
			df["Comment"] = COMMENTS
		

		df.to_csv(TO_CSV_FILE, index_label = "Nr")
		print("Successfully created CSV:", TO_CSV_FILE)

	else:
		print("No Category found for:", GROUP_CATGR_NAME)
		print("Possible groups include:", *possible_groups, sep='\n')

def get_group_categories(course):

	return course.list_group_categories()

def list_groups_in_group_category(course, cat_id):

	'''You can make your own custom request like this'''
	from canvasapi.paginated_list import PaginatedList
	from canvasapi.group import Group
	groups_plist = PaginatedList(Group,course._requester,
					'GET',
					'group_categories/{}/groups'.format(cat_id)
					,{})
	return groups_plist
	

'''contrib: If you have your groupCategoryID/groupsetID 
You could use
canvas.get_group_category(category_id) # That returns single group_category object
So that function is available if you want to select only the one you need
'''

if __name__ == '__main__':
	gen_groupset_csv()
