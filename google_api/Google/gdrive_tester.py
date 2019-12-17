from google_apps import GDrive, GMail

myDrive = GDrive()

file_link = myDrive.upload_file('Charlie.zip', domain_only=False)

myGmail = GMail("charles.cohen@nycdatascience.com")

msg = myGmail.create_message("lincoh85@gmail.com", "Grade Python Midterm", "Download the submissions at this link: " + file_link)

myGmail.send_message(msg)



