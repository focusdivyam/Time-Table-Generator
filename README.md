# Time-Table-Generator
An algorithm that generates a time table using a SAT solver under specific constraints.

1. CONSTRAINTS-
   
	->Classes should run only from Monday to Friday(available days).
	
	->Only 1 lecture of any course on a single day.
	
	->Classes should be in institute specified timings.
	
	->Labs should be continuous on a day.
	
	->No clashes are there for rooms or profs .

2. Main highlights:
   
a) Input:
	A list of students representing the courses chosen by a specific student.
	
	Course info of every course i.e. course id, professor teaching the course, and structure of that course (L-T-P).
	
	A list of available rooms with their respective capacity.
	
	Finally, the institute class/work timings.

b) Output:
	Weekly Schedule for the given courses as per their structure(L-T-P) to a .csv file. 
	
	Clearly mentioning the time slots and room booked for every course without any clashes.

3. TECH USED-
	Used python as it is versatile and readable.
	
	Z3 –SAT solver for checking if the given problem is sat or unsat based upon constraints.

4. Output:
	User can choose to see whole time table or batch specific time table by entering their batch.
	
	The algorithm prints the time table accordingly and clearly represents the:

	 -Day of class
 
	-Room allocated to course
 
	- Course ID and
 
 	- Prof.  Teaching the course.

5. For running:
	Clone the repository to a folder in your local machine and download pyhton z3 sat solver to the same folder and open it in terminal.

	Type 'python main.py' in terminal to generate the time table.

6. [CLick here for sample ouptut] (https://drive.google.com/file/d/1RPfp88cTRErHqzrOb5lVj4ZllDWmvWLO/view?usp=sharing)
   
7. For better understanding please refer the video:


https://github.com/focusdivyam/Time-Table-Generator/assets/107490578/e1b2698d-62cf-4deb-81bd-0499e8d64ac7
