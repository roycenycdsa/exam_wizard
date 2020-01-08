from ..gapi_utils import ml_service, dv_service, st_service
from fpdf import FPDF
import pandas as pd


def process_gradebook(df, questions, exam_tag):

    exam_ids = df['Exam ID']

    for exam_id in exam_ids:
        process_single_report(exam_id, df, questions, exam_tag)

    pass

def process_single_report(exam_id, df, questions, exam_tag):

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
    pdf.cell(200, 8, txt="Which places you at the [placeholder] percentile.", align = "C")
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

    pdf.output(file_name)
    pass
