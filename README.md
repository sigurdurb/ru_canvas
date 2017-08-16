# ru_canvas
Python scripts for use by Teachers and TA's to interact with the canvas api.

All scripts use canvasapi: [https://github.com/ucfopen/canvasapi](https://github.com/ucfopen/canvasapi) which is a pip installable package.

The scripts are standalone now but some of it might be refactored into a module later.

Some scripts also have costum made requests that are not yet in **canvasapi** but use parts of their methods for simplicity. We might add them later to the [https://github.com/ucfopen/canvasapi](https://github.com/ucfopen/canvasapi)
and then refactor this code.

### Requirements:

```
pip install canvasapi
pip install pandas 
```

## Scripts:
For all the scripts you need to:

Get your api key/token from your profile->settings


* API_KEY = "" 

Get your api url. i.e. "https://{yourschool}.instructure.com/api/v1/" 

* API_URL = ""

These settings are stored in the canvas_config.py and are imported
into the scripts below as ```from canvas_config import *```

### gen_groupset.py
This script generates a detailed csv for your groupset.
Each row has only one group with every student listed.
It will list all those students who have the assignment, even those who have not submitted (this is because some assignments might have the "no submission" or "paper handin" option) You can also see in the speedgrader which students have "No Submission"
See this video on how to use the script (to be done)

This creates a CSV with columns for 'GroupSet', 'GroupSetID', 'Group', 'GroupID', 'Student', 'Student_ID','StudentSection','StudentN', 'StudentN_ID','StudentNSection' for each N student in the group


If you later use the upload script(yet to be published) it only needs to submit the the grade for one StudentID in the group for it to go to the whole group because that is how the Canvas API works. The upload script will also have a comment if you want to submit a comment. Later we might add functionality to submit a rubric assessment object but teachers/TA's are going to try and use the speedgrader first.

You need to:

Get the course id from your course url https://reykjavik.instructure.com/courses/{yourcourseID}

Enter it as an integer into the script

* COURSE_ID = 123

Assignment id will be in the url of the assignment https://reykjavik.instructure.com/courses/{yourcourseID}/assignments/{yourassignmentID}

* ASSIGN_ID = 321

### gen_groupset_individual.py

This script generates a detailed csv for your groupset.
Use this when you create a group assignment that was created with the "grade each student individually" option. Then use the submit_grades_individual.py (yet to be published). That will make sure that only the grade and comment for that individual will be published to him and not everybody in the group.

This creates a CSV with columns for 'GroupSet', 'GroupSetID', 'Group', 'GroupID', 'Student', 'StudentID' for each student in the Group

It also has optional Grades and Comments variables if you want to set up a template for those. Or set those variables as None if you dont want the extra columns.

If you have any empty groups(groups with no students) it won't list those.
Also, It will only list students that are in the groups within the groupset. So make sure you have all the students there. (the functionality to add rest of students later is in the gen_groupset.py script)


Get the Course id from your course url https://reykjavik.instructure.com/courses/{yourcourseID}
Enter it as an integer

You need to: 

* COURSE_ID = 123

Get your group set category name, Note: not the assignment-group.
You can also just run the script once and it will print out the possible groupset names that you can then copy into your script.
You can find this category name on the Tabs of YourCourse->People page or at yourcanvasinstance.com/courses/{your_course_id}/users and look at the tab

* GROUP_CATGR_NAME = ""



### gen_students.py

This script prints out students id and beginning of their schools email addresses. This is something the programming web needs.

You can also get all the emails by just adding + "@ru.is" to the end.

This script has 2 functions

* get_users(course) : returns all students and teachers/TA's and other people affiliated
* get_students(course) : returns only those with enrollment_type=student

You need to:

Get the Course id from your course url https://reykjavik.instructure.com/courses/{yourcourseID}
Enter it as an integer into the script

* COURSE_ID = 123
