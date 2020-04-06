import sys
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
import pandas as pd
import webbrowser

create_book_flag = input("Do you want to create a gradebook? (Y/[N])\n")

if "y" in create_book_flag.lower():

    gradebook_name = input("Please enter a name for this new exam.\n")

    if "exit" in gradebook_name.lower():
        exit()

    exam2 = gb.create_grade_book(gradebook_name, in_domain = True)

    print("New Gradebook created.\n")

    #form_link = "https://docs.google.com/forms/d/e/1FAIpQLSfhrthrM_-clN2mNsI2aCHHbn1ghCAxL2tZCya8rQtBxAAOBg/viewform"

    #webbrowser.open(gb.get_link(exam2))

    #webbrowser.open(form_link)

#print("Thank you for using ExamWizard(TM)!")
