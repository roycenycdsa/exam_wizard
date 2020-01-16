from examwiz_pkg.examwiz_pkg.gapi_utils import ml_service, dv_service, st_service
from fpdf import FPDF
import os
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator


def produce_distplot(gradebook_column, student_score, file_tag = ""):

    plt.gcf().clf()

    sns.set_style('whitegrid')

    n, bins, patches = plt.hist(gradebook_column.astype(int),
                                bins = np.arange(0, 26, 1), density = True, color = 'grey')
    dist_curve = sns.distplot(gradebook_column.astype(int), hist=False)

    patches[student_score].set_fc('r')
    plt.xlabel("Score out of 25")
    plt.xlim([0,26])

    red_patch = mpatches.Patch(color = 'red', label = 'Your Score')
    dist_curve.legend(handles=[red_patch])

    if not os.path.isdir("./demo/example_exam/student_submissions/reports/images/"):
        os.makedirs("./demo/example_exam/student_submissions/reports/images/")

    temp = dist_curve.get_figure()
    temp.savefig("./demo/example_exam/student_submissions/reports/images/" + file_tag + "temp_report.png")

def produce_hist(gradebook_column, student_score, question, file_tag = ""):
    '''
    Takes a gradebook column, a student's score, and the question in order to produce
    a detailed graph pertaining to their score on the exam.
    '''

    # clear working space
    plt.gcf().clf()

    scores = gradebook_column.unique().astype(str)
    scores.sort()
    student_score = str(student_score)
    # print(question)
    # print("using ", scores, " as scores")
    # print("using ", student_score, " as student score")

    clrs = ['red' if x == student_score else 'grey' for x in scores]
    # print("We are using ", clrs, " to color ", question)
    sns.set_style("whitegrid")
    red_patch = mpatches.Patch(color = 'red', label = 'Your Score')
    student_score = sns.countplot(gradebook_column, palette=clrs)
    plt.ylabel("# of Students")
    plt.xlabel("Score out of 5")
    plt.xlim([-1,5])
    student_score.yaxis.set_major_locator(MaxNLocator(integer = True))
    student_score.legend(handles=[red_patch])

    if not os.path.isdir("./demo/example_exam/student_submissions/reports/images/"):
        os.makedirs("./demo/example_exam/student_submissions/reports/images/")

    temp = student_score.get_figure()
    temp.savefig("./demo/example_exam/student_submissions/reports/images/" + file_tag + "temp_report.png")

    return student_score

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

def process_gradebook(df, student_keys, questions, exam_tag):
    '''
    Process an entire gradebook into PDFs.
    Takes:
    df: A gradebook downloaded into a dataframe.
    student_keys: A dataframe containing the conversion keys from exam ID to
                  student names.
    questions: A dictonary of questions pertaining to that specific exam.
    exam_tag: what the reports will be tagged with, will eventually become the
              flag to choose which 'questions' set up should be used.

    Returns:
    Nothing, but produces as many PDFs as lines in the gradebook. They are saved
    to './reports/'.
    '''
    df['Student ID'] = df['Student ID'].astype(int)
    student_keys = student_keys[['name', 'student_id']]

    combined_df = pd.merge(df, student_keys, how = 'left', left_on = 'Student ID', right_on = 'student_id')

    exam_ids = combined_df['Student ID'].unique()

    percentile_list = {}
    for question in questions.items():
        percentile_list[question[0]] = percentile(df[question[0]])

    percentile_list['total'] = percentile(combined_df['Total Score'])

    num_of_ids = len(exam_ids)
    i = 1

    for exam_id in exam_ids:
        print("Processing exam: ", exam_id)
        print(i, " of ", num_of_ids)
        process_single_report(exam_id, combined_df, questions, exam_tag, percentile_list)
        i += 1
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

    student_exam = df[df['Student ID'] == exam_id]

    student_exam = student_exam.iloc[-1]

    student_name = student_exam['name']
    print(student_exam['name'])
    grader = student_exam['Grader']
    exam = exam_tag
    file_name = student_exam['name'].strip()+"_"+exam+".pdf"

    intro = "\t\t\t\tThis is your exam report for the {}. Your grader was {}, so please feel free to reach out to them if you have additional questions about the exam, or any of the grades you received."

    temp_comment = "GAMBATE!!!"


    pdf = FPDF()
    pdf.add_page()
    pdf.image("./structure_files/nycdsalogo.png", x=55, y=8, w=100)

    pdf.set_line_width(0.5)
    pdf.set_fill_color(255, 0, 0)
    pdf.line(10, 35, 200, 35)

    pdf.set_font("Arial", size=10)
    pdf.ln(30)
    pdf.cell(190, 6, txt="Hello {},".format(student_exam['name'].strip()), ln=1, align="L")
    pdf.ln(2)
    pdf.multi_cell(190, 6, txt=intro.format(exam, grader), align = "L")

    pdf.ln(5)
    pdf.set_font("Arial", size = 12)
    pdf.cell(95, 8, txt="Overall: {} out of 25".format(student_exam['Total Score']), ln = 0, align="L")

    temp_y = pdf.get_y()
    pdf.set_font("Arial", size = 10)

    produce_distplot(df['Total Score'].astype(int), int(student_exam['Total Score']), file_tag = "Overall_Graph")

    pdf.image("./demo/example_exam/student_submissions/reports/images/Overall_Graphtemp_report.png",
              x = 110,
              w = 90)
    final_y = pdf.get_y()

    pdf.set_y(temp_y)
    pdf.ln(4)
    pdf.cell(90, 8, txt="Which places you at the {} percentile.".format(percentile_list['total'][student_exam['Total Score']]), align = "L")
    pdf.ln(8)
    pdf.multi_cell(90, 5, txt="Overall Comment: {}".format(student_exam['Overall Comment']), align = 'L', border = 0)

    pdf.set_y(final_y)

    pdf.line(10, final_y, 200, final_y)

    i = 1

    for question in questions.items():

        if pdf.get_y() > 200:
            pdf.add_page()
            pdf.ln(1)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(1)
        pdf.set_font("Arial", size = 12)

        if i % 4 == 1:

            pdf.cell(100, 8, txt=question[0]+": "+question[1], align = "L")

            temp = pdf.get_y()

            pdf.set_font("Arial", size = 10)
            pdf.set_x(110)
            pdf.ln(2)
            pdf.set_x(110)
            pdf.multi_cell(90, 5, txt="TA Comment: {}".format(student_exam[i+1]), align = "L", border = 0)
            if int(student_exam[i]) < 3:
                pdf.ln(6)
                pdf.set_x(110)
                pdf.multi_cell(190, 6, txt="Instructor Comment: {}".format(temp_comment))
            else:
                pdf.ln(6)

            pdf.set_y(temp)
            pdf.ln(4)
            pdf.cell(90, 8, txt="Score: {}/5".format(student_exam[i]), align = "L")
            pdf.ln(6)

            produce_hist(df[question[0]], student_exam[i], question[0], file_tag = question[0])

            pdf.image("./demo/example_exam/student_submissions/reports/images/" + question[0] + "temp_report.png", x = 5, w = 90)
        else:
            pdf.set_x(110)
            pdf.cell(90, 8, txt=question[0]+": "+question[1], align = "R")

            temp = pdf.get_y()

            pdf.set_font("Arial", size = 10)
            pdf.set_x(10)
            pdf.ln(2)
            pdf.multi_cell(90, 5, txt="TA Comment: {}".format(student_exam[i+1]), align = "L", border = 0)
            if int(student_exam[i]) < 3:
                pdf.ln(6)
                pdf.multi_cell(190, 6, txt="Instructor Comment: {}".format(temp_comment))
            else:
                pdf.ln(6)

            pdf.set_y(temp)
            pdf.ln(4)
            pdf.set_x(110)
            pdf.cell(90, 8, txt="Score: {}/5".format(student_exam[i]), align = "R")
            pdf.ln(6)

            produce_hist(df[question[0]], student_exam[i], question[0], file_tag = question[0])

            pdf.set_x(110)
            pdf.image("./demo/example_exam/student_submissions/reports/images/" + question[0] + "temp_report.png", x = 120, w = 90)

        pdf.ln(2)
        y_space = pdf.get_y()
        i += 2
        pdf.line(10, y_space, 200, y_space)



    pdf.output("./demo/example_exam/student_submissions/reports/" + file_name)
    pass
