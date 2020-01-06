from google_apps import GDrive, GMail

myDrive = GDrive()

file_link = myDrive.upload_file('test_pdf.pdf', domain_only=True)

myGmail = GMail("charles.cohen@nycdatascience.com")

msg = myGmail.create_message("iamcharliecohen@gmail.com", "Private PDF", "Download the submissions at this link: " + file_link)

myGmail.send_message(msg)



