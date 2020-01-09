EXAM WIZARD: THE PRESENTONINING

Introduction:
  - Why are we doing this?
    + Centralize the grades to allow for better analysis across cohorts
    + Reduce the labor required to enter grades and send the reports
    + Produce better reports for students so they can get more information/feedback.
    + Anonymize exams in order to reduce bias that arises from grading

  - How does this help?
    + Integration with the website means we can move away from Google's suite of products
    + Automated report generation + sending means no one will have to be responsible for dealing
    with these tasks.

The App Itself:

0. Creating the Gradebook

\* We will show how to run the script to produce the new gradebook *
  - Each exam will have a corresponding Gradebook that will link to a submission form on the website
    + Allows us to store the data on our servers, not google's
    + Allows us to move away from Sheets, Forms.
    + Only needs to be done once per exam
  - Centralizes the exam information
    + Can be stored as simple CSV since # of entries / year will be low (~250 rows/yr)
    + Tracks changes between cohorts

1. Downloading the Exams

\* Conceptual step, will most likely just show folder of downloaded exams *
  - Can be done in an anonymized way, in order to reduce bias.
    + Several ways to do this, currently looking towards either
      a. Anonymize locally
      b. Download with submission number as the filename
  - Will be a 'batch-download' which will allow an admin to download all the student submissions
  at one time.

2. Send Anonymized Exams to the TAs

\* Run script and show tester email *
  - Flag TAs that will be available for grading + distribute exams
    + Will allow the exams to be automatically sent + equally divided based on # of TAs.
  - Generate a dataframe that contains which TAs should be grading which exams.
  - This process can be automated!


3. TAs submit grades

\* Display Form + show updated / completed sheets *
  - Currently handled through Google Sheets, would eventually like to move towards hosting this
  on the website
    + Akin to how we can submit grades for the projects on the website, but a little different.
  - TAs submit grades based on the exam ID that they receive, then on the backend the information
  is stored un-anonymized.

3a. Remind TAs who haven't graded their exams a reminder to do so

\* Conceptual? *
  - Hopefully can be automated, right now the Google Rest API does not allow you to schedule emails.
  - Allow us to keep better track of who is doing what work, as well as reminding people of the work
  that they need to do.


4. Admin audits the Gradebook

\* Show completed gradebook *
  - Manual, need to make sure that there are no mistakes, could be helped by several small helper functions.


5. Admin flags Gradebook to be sent out

\* Show completed gradebook *
  - Also manual, need to make sure that the gradebook is complete.

6. Generate Reports automatically + distribute them

\* Run script to process gradebook data into individual reports for the students *
  - Create PDFs based on the information submitted by the TAs, and then email them out to the students.
    + This can be done automatically, both the generation + sending
  - Allows for more robust information (i.e., percentile, avg. score, additional comments if under a certain
  score).
    + Better product for the students & gives them better and more exacting information.
  - Expandable in order to give metadata about each room, how the cohort is doing versus other cohorts,
  which questions were most missed, etc.
