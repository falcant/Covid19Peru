Remember to follow this website when for deploying for updates:

https://dash.plotly.com/deployment

updates:

Ver 1.02

7/23/2020 

 - added title and author
 - updated the data set, the app now includes all the cases reported by the department and city.

Ver 1.03

7/26/2020

 - created another file called "dl.py" that deals with all the data manipulation/cleaning and extraction of the 2 data sources (positive cases and deaths).
 - the data now uses 2 pivoted tables, called "CasesbyDepartment.csv" and "CasesbyDistrict.csv"
 - Column reformatting and now includes:

	 - "Active cases" : number of people who have Covid-19.
	 - "Deaths": Number of people who have died from Covid-19.
	 - "Total" : sum of both.
 - Description was added


8/9/2020

 - Added a dropdown tab for the "Department" and a callback function for the District
 - added a second map that will tell show the location of the Department.
