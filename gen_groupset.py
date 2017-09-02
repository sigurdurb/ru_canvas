#!/usr/bin/python3

'''https://github.com/ucfopen/canvasapi'''
from canvasapi import Canvas
from canvas_config import *
import pandas as pd
from itertools import chain
from math import isnan
'''Course id is in your url https://reykjavik.instructure.com/courses/{Course_ID}'''
COURSE_ID = 256
ASSIGN_ID = 2835


'''This script generates csv for groupsets where each group has only one row.
It adds rubriks parts to a column name so TA's can mark their name and if they are done with
the question.
The rest of the students that have the assignment but are not
a group or/and have not submitted are also put in afterwards at the end of the file'''

def main():
	canvas = Canvas(API_URL, API_KEY)
	# First, retrieve the Course object
	course = canvas.get_course(COURSE_ID)
	
	group_cats_lis = course.list_group_categories()
	print(*group_cats_lis,sep="\n")
	g_cat_id = int(input("Enter the (number) of the group category you want to generate: "))
	g_cat = [i for i in group_cats_lis if g_cat_id == i.id]
	
	rm_nosubs = input("Do you want to remove those who have not submitted? (y/n): ")

	sec_params = {"include[]":["students"]}
	sections = course.list_sections(**sec_params)

	csv_name = "Assign_" + str(ASSIGN_ID) + "_"# "This is changed dynamicly to the groupset name"
	max_group_cnt = 0
	all_rows = []

	if g_cat:
		g_cat = g_cat[-1]
		csv_name += g_cat.name
		print("Getting students in groups")
		groups = g_cat.list_groups()
		for g in groups:
			if g.members_count == 0:
				continue
			user_details = []
			users = g.list_users()
			for user in users:
				sec_name = find_sections(sections, user.id)
				guser_row = [user.name, int(user.id), sec_name]
				user_details.extend(guser_row)
			max_group_cnt = int(max(max_group_cnt,int(len(user_details) / 3)))
			group_details = [g_cat.name, int(g_cat.id), g.name, int(g.id)]
			group_details.extend(user_details)
			all_rows.append(group_details)
	else:
		print("No id was found for Group Category number:", int(g_cat_id))
		answer = input("Do you wish to continue getting the students for the assignment? (y/n): ")
		if answer != "y":
			exit(1)
	
	header_cols = ['Student', 'Student_ID','StudentSection']
	
	# If there are groups with students in them then we want to add the extra headers
	# So this script will also work if you have only an empty groupset and only individuals
	if all_rows:
		extra_st_cols = list(chain.from_iterable(("Student"+str(i),"Student"+str(i)+"_ID","Student"+str(i)+"Section") for i in range(2,max_group_cnt+1)))
		group_cols = ['GroupSet', 'GroupSetID', 'Group', 'GroupID']
		header_cols[0:0] = group_cols
		header_cols.extend(extra_st_cols)

	df = pd.DataFrame(all_rows, columns=header_cols)
	
	'''Beginning of getting rubrik '''
	set_rubrik_headers(course, df)
	'''End of getting rubrik '''
	
	'''Beginning of adding students that have the assignment but are not in a group
	and also finding their sections'''
	print("Adding rest of students that have this assignment")
	params = {"include[]": ["user"]}
	subs = course.list_submissions(ASSIGN_ID,**params)
	id_cols = [x for x in header_cols if "_ID" in x]
	
	for sub in subs:
		boomap = []
		for idc in id_cols:
			boomap.extend([df[idc].isin([sub.user_id]).any()])
			if idc == id_cols[-1]:
				if not any(boomap):
					#print("Adding:", sub.user['name'], sub.user_id)
					sec_name = find_sections(sections, sub.user_id)
					df = df.append({'Student':sub.user['name'],'Student_ID':int(sub.user_id),'StudentSection': sec_name},ignore_index=True)

	# Doing this afterwards simply because we only need it for one student in the row
	set_submission_date(subs, df)
	if rm_nosubs == 'y':
		print("Removing students/groups that have not submitted")
		df = df.drop(df[df['SubmittedAt'] == "Nothing submitted"].index)
	csv_name += ".csv"

	all_id_cols = [x for x in header_cols if "ID" in x]
	# Changing the types of the ID columns so the csv does not have any extra zeroes for the ids no matter if european or usa sheet
	for col in all_id_cols:
		df[col] = df[col].apply(float_to_str_no_decimal)
	
	df.to_csv(csv_name, index_label = 'Nr', float_format='%.2f', sep=',', decimal=".")
	print("Successfully created CSV:", csv_name)

def find_sections(sections, user_id):
	sec_name = ""
	# Student can be listed in many sections so need to check all 
	for sec in sections:
		for st in sec.students:
			if st['id'] == user_id:
				sec_name += "/" + sec.name if sec_name != "" else sec.name
	return sec_name


def set_rubrik_headers(course, df):
	assign = course.get_assignment(ASSIGN_ID)
	try:
		if assign.rubric is not None:
			print("Getting rubrik for assignment:", assign.name)
			# This is for VERK's and REIR color coding of TA's and completed assignment status
			for crit in assign.rubric:
				col = crit['description'] + "(" + str(crit['points']) + "/" + str(assign.points_possible) + ")"
				df[col] = ""
				df[crit['description']+"x"] = ""
			print("Added rubrik for assignment: ", assign.name)
		else:
			print("No rubrik found for assignment:", assign.name)
	except AttributeError:
		print("No rubric for this assignment", assign.name)

def set_submission_date(subs, df):
	# Resetting it just in case, and because we are using .loc
	df.reset_index(drop=True, inplace=True)
	df["SubmittedAt"] = ""
	df["Grade"] = ""
	for i in range(0,df.shape[0]):
		st_id = df.loc[i, "Student_ID"]
		for sub in subs:
			if sub.user_id == st_id:
				df.loc[i,"Grade"] = sub.score if sub.score != None else float(0)
				df.loc[i,"SubmittedAt"] = "Nothing submitted" if sub.submitted_at == None else sub.submitted_at

def float_to_str_no_decimal(val):
	return "" if isnan(val) else "%d" % val

if __name__ == '__main__':
	main()
