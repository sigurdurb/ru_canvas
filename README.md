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

### gen_groupset_csv.py

This script generates a detailed csv for your groupset.
Use this when you create a group assignment that was created with the "grade each student individually" option. Then use the submit_grades_individual.py (yet to be published). That will make sure that only the grade and comment for that individual will be published to him and not everybody in the group.

This creates a CSV with columns for 'GroupSet', 'GroupSetID', 'Group', 'GroupID', 'Student', 'StudentID' for each student in the Group

It also has optional Grades and Comments variables if you want to set up a template for those. Or set those variables as None if you dont want the extra columns.

If you have any empty groups(groups with no students) it won't list those.
Also, It will only list students that are in the groups within the groupset.
 
This functionality can be added later but Teachers/TA can also view the SpeedGrader(which will display the rest of the students names).
This is ready but is yet to be published.

You need to:

Get your api key/token from your profile->settings


* API_KEY = "" 

Get your api url. i.e. "https://{yourschool}.instructure.com/api/v1/" 

* API_URL = ""

Get the Course id from your course url https://reykjavik.instructure.com/courses/{yourcourseID}
Enter it as an integer

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

Get your api key/token from your profile->settings


* API_KEY = "" 

Get your api url. i.e. "https://{yourschool}.instructure.com/api/v1/" 

* API_URL = ""

Get the Course id from your course url https://reykjavik.instructure.com/courses/{yourcourseID}
Enter it as an integer into the script

* COURSE_ID = 123
