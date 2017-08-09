# ru_canvas
Python scripts for use by Teachers and TA's to interact with the canvas api.
 
All the scripts use canvasapi in some form: https://github.com/ucfopen/canvasapi

Some scripts also have costum made requests that are not yet in the canvasapi but use parts of the canvasapi methods for simplicity. 

### Requirements:

```
pip install canvasapi
pip install pandas 
```


## scripts:

### gen_groupset_csv.py

This script generates a detailed csv for your groupset with columns for 
'GroupSet', 'GroupSetID', 'Group', 'GroupID', 'Student', 'StudentID'

If you have any empty groups(groups with no students) it wont list those.
Also, It will only list students that are in the groups within the groupset.
Those students that have not entrolled or the teacher has not enrolled in a group within the groupset won't be listed.

You need to:

Get your api key/token from your profile->settings


* API_KEY = "" 

Get your api url. i.e. "https://{yourschool}.instructure.com/api/v1/" 

* API_URL = ""

Get the Course id from your course url https://reykjavik.instructure.com/courses/{yourcourseID}
Enter it as an integer

* COURSE_ID = 123

Get your group set category name, Note: not the assignment-group
You can find this category name on the Tabs of YourCourse->People page or at yourcanvasinstance.com/courses/{your_course_id}/users and look at the tab

* GROUP_CATGR_NAME = ""