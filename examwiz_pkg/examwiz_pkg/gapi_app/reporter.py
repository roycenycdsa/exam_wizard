from ..gapi_utils import ml_service, dv_service, st_service
from fpdf import FPDF
import pandas as pd


def percentile(lst):
    '''
    Takes a list and produces percentile numbers for said list.
    lst: A list of numbers to convert to percentiles

    Returns a dictonary containing the score and what percentile that
    score comapares to.
    percentile_scores: a dictonary where the keys are the scores, and the
    values are the percentile numbers.

    ex:
    If we have [0,0,1,1,2,3] as our lst, we would get the following output:

    process_gradebook = {'0' : 16.67,
                         '1' : 50.00,
                         '2' : 75.00,
                         '3' : 91.67}
    '''
    lst = pd.to_numeric(lst)
    temp = lst.sort_values()
    temp = temp.astype(str)

    percentile_scores = {}
    i = 0
    for val in temp.unique():
        equal_rank = len(temp[temp == val])

        percentile_scores[val] = round((i + (0.5*equal_rank))/len(temp) * 100, 2)
        i += equal_rank

    return percentile_scores

def process_gradebook(df, questions, exam_tag):
    '''
    Process an entire gradebook into PDFs.
    Takes:
    df: A gradebook downloaded into a dataframe.
    questions: A dictonary of questions pertaining to that specific exam.
    exam_tag: what the reports will be tagged with, will eventually become the
              flag to choose which 'questions' set up should be used.

    Returns:
    Nothing, but produces as many PDFs as lines in the gradebook. They are saved
    to './reports/'.
    '''
    exam_ids = df['Exam ID']

    percentile_list = {}
    for question in questions.items():
        percentile_list[question[0]] = percentile(df[question[0]])

    percentile_list['total'] = percentile(df['Total Score'])

    for exam_id in exam_ids:
        process_single_report(exam_id, df, questions, exam_tag, percentile_list)

    pass

def process_single_report(exam_id, df, questions, exam_tag, percentile_list):
    '''
    Processes a single row of the dataframe (usually denoted gradebook) based
    on exam_id. Produces a PDF that is placed in './reports/'.
    This can be run by itself, but most of the time will be called by the
    function above.

    Takes:
    exam_id: the unique exam ID that needs to be processed. (string)
    df: the gradebook in question (pandas.DataFrame)
    questions: format of the exam (stored as dictonary)
    exam_tag: what the exam should be tagged as. Will eventually be how the
              structure of the exam is determined.
    percentile_list: A list generated from the above function, percentile().
                     It contains what percentiles the individual scores are,
                     and they are linked via a dictonary format.

    Return:
    Nothing, just produces a PDF report in the subfolder "./reports/".
    '''

    student_exam = df[df['Exam ID'] == exam_id]

    student_name = exam_id
    grader = student_exam['Grader'].iloc[0]
    exam = exam_tag
    file_name = student_name+" "+exam+".pdf"

    intro = "\t\t\t\tThis is your exam report for the {}. Your grader was {}, so please feel free to reach out to them if you have additional questions about the exam, or any of the grades you received."

    temp_comment = "GAMBATE!!!"


    pdf = FPDF()
    pdf.add_page()
    pdf.image("./nycdsalogo.png", x=55, y=8, w=100)

    pdf.set_line_width(0.5)
    pdf.set_fill_color(255, 0, 0)
    pdf.line(10, 35, 200, 35)

    pdf.set_font("Arial", size=12)
    pdf.ln(30)
    pdf.cell(200, 6, txt="Hello {},".format(student_name), ln=1, align="L")
    pdf.ln(2)
    pdf.multi_cell(190, 8, txt=intro.format(exam, grader), align = "L")

    pdf.ln(5)
    pdf.set_font("Arial", size = 14)
    pdf.cell(200, 8, txt="Overall: {} out of 25".format(student_exam['Total Score'].iloc[0]), ln = 1, align="C")
    pdf.set_font("Arial", size = 12)
    pdf.ln(2)
    pdf.cell(200, 8, txt="Which places you at the {} percentile.".format(percentile_list['total'][student_exam['Total Score'].iloc[0]]), align = "C")
    pdf.ln(18)

    pdf.line(10, 100, 200, 100)

    i = 1

    for question in questions.items():

        pdf.set_font("Arial", size = 14)
        pdf.cell(200, 8, txt=question[0]+": "+question[1], align = "C")

        pdf.set_font("Arial", size = 12)
        pdf.ln(4)
        pdf.cell(200, 8, txt="Score: {}/5".format(student_exam.iloc[0, i]))
        if int(student_exam.iloc[0,i]) < 3:
            pdf.ln(6)
            pdf.multi_cell(190, 6, txt="Instructor Comment: {}".format(temp_comment))
        else:
            pdf.ln(6)
        pdf.multi_cell(190, 6, txt="TA Comment: {}".format(student_exam.iloc[0, i+1]))
        pdf.ln(2)
        y_space = pdf.get_y()
        i += 2
        pdf.line(10, y_space, 200, y_space)



    pdf.output("./reports/" + file_name)
    pass
