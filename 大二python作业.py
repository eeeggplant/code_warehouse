#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  
#
#    Student no:    1922441014
#    Student name:  Cindy
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  OUR WORLD
#
#  Countries come in all shapes and sizes.  There is an enormous
#  difference between the population levels of cities in different
#  parts of the world.  In this task you will develop a program
#  that helps visualise the population differences between cities
#  and countries.  To do so you will make use of three different
#  computer languages, Python, SQL and HTML.  You will develop
#  a Python function, show_population, which accesses data in an 
#  SQLite database and uses this to generate HTML documents which
#  visually display a comparison of city population in a country.
#  See the instructions accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Acceptance Tests-----------------------------------------------#
#
#  This section contains unit tests that run your program.  You
#  may not change anything in this section.  NB: 'Passing' these
#  tests does NOT mean you have completed the assignment because
#  they do not check the HTML files produced by your program.
#
"""
##Test 1: China cities > 1m
##>>> show_population(['China'], 1000000, 'Test01') 
##
##Test 2: Aus cities > 100000
##>>> show_population(['Australia'], 100000, 'Test02') 
##
##Test 3 - 2 countries
##>>> show_population(['China', 'Australia'], 1000000, 'Test03') # 

##Test 4 - 3 countries
##>>> show_population(['China', 'India', 'United States'], 10000, 'Test04') 

##Test 5 - 4 countries
##>>> show_population(['Germany', 'New Zealand', 'Austria', 'Australia'], 1000000, 'Test05') 
##
##Test 6 - 6 countries
##>>> show_population(['Indonesia', 'Japan', 'Thailand', 'Taiwan', 'Ireland', 'United Kingdom'], 1000, 'Test06')
##
##Test 7 - empty results set
##>>> show_population(['Australia'], 5000000, 'Test07')

""" 
#
#--------------------------------------------------------------------#



#-----Students' Solution---------------------------------------------#
#
#  Complete the task by filling in the template below.

# Get the sql functions
from sqlite3 import *
from math import *
# (You may NOT import any other modules)
##### PUT YOUR show_population FUNCTION HERE


def show_population(list_place_name, population, name):
    page_number = 0  # Set the number of pages
    # Connect to database
    world = 'world.db'
    conn = connect(world)
    cur = conn.cursor()
    for item in list_place_name:
        page_number += 1  # Increase the number of pages
        # Find country code
        sql_code = 'select Code from Country where Name == "%s" ' % (item)
        cursor = cur.execute(sql_code)
        for row in cursor:
            country_code = row[0]
            pass
        # Obtain city data based on country code
        sql_code = 'select Name, Population from City where CountryCode == "%s"' % (country_code)
        cursor = cur.execute(sql_code)
        city = {}  # Create a dictionary 'city' to hold data about cities and populations
        for row in cursor:  # Store the data in the dictionary
            if row[1] >= population:
                city['%s' % (row[0])] = row[1]
                pass
        count = len(city)  # Count the number of cities
        # Sort the items in the dictionary alphabetically by city name and store the data in the list
        city_list = sorted(city.items())
        conn.commit()

        # Write data to a web page
        with open(name + '_' + item + '.html', 'w') as html:
            # Write the text at the top of the page
            html_code = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <title>Cities of %s</title>
                </head>
            <body>
                <h1 style = "text-align: center">Cities of %s</h1>
                <h3 style = "text-align: center">with population >= %d</h3>
                <h3 style = "text-align: center">city count: %d</h3>
                <hr>
            </body>
            </html>""" % (item, item, population, count)
            html.write(html_code)
            html.write('<center>')  # Center the city name
            for name_and_population in city_list:
                # Adjust the font size
                font_size = int(name_and_population[1] / 50000 + 10)
                font_size = int((font_size / 70) ** 0.5 * 70)
                # Set the color of the text according to the size
                r, g, b = 0, 0, 0
                if font_size < 20:
                    r = (font_size - 10) * 25
                elif 30 > font_size >= 20:
                    r = 255
                    g = (font_size - 20) * 25
                elif 50 > font_size >= 30:
                    r = 255 - (font_size - 30) * 12
                    g = 255
                elif 65 > font_size >= 50:
                    g = 255
                    b = (font_size - 50) * 17
                elif 80 > font_size >= 65:
                    g = 255 - (font_size - 65) * 17
                    b = 255
                elif font_size >= 80:
                    b = 255 - font_size + 80
                # Write the city name
                html_code = """
                <span style="color: rgb(%d, %d, %d); font-size: %dpx;">%s</span>""" \
                            % (r, g, b, font_size, name_and_population[0])
                html.write(html_code)
                pass
            html.write('</center>')
            html.write('<hr>')
            total_number = len(list_place_name)  # Count the total number of web pages
            # Add hyperlinks
            if total_number > 1:  # Determine what hyperlinks are required
                if page_number < total_number:
                    html_code = '<a href="%s_%s.html" style="float:right;">Next page</a>' \
                                % (name, list_place_name[page_number])
                    html.write(html_code)
                if page_number > 1:
                    html_code = '<a href="%s_%s.html" style="float:left;">Previous page</a>' \
                               % (name, list_place_name[page_number - 2])
                    html.write(html_code)
            pass
        pass
    cur.close()
    conn.close()  # End the connection to the database

show_population(['Indonesia', 'Japan', 'Thailand', 'Taiwan', 'Ireland', 'United Kingdom'], 1000, 'Test06')

#
#--------------------------------------------------------------------#



#-----Automatic Testing----------------------------------------------#
#
#  The following code will automatically run the unit tests
#  when this program is "run".  Do not change anything in this
#  section.  If you want to prevent the tests from running, comment
#  out the code below, but ensure that the code is uncommented when
#  you submit your program.
#
if __name__ == "__main__":
     from doctest import testmod
     testmod(verbose=False)   

#--------------------------------------------------------------------#
