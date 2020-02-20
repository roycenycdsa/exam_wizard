from fpdf import FPDF
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator

'''
These functions below are the HELPER FUNCTIONS. They are:

precentile: gives us percentile rankings based on scores on the exam.

produce_distplot: returns a distribution plot over a histogram based on the specific column
                  of the gradebook.

produce_hist: returns a histogram based on a specific column of the gradebook.

section_total: takes a DF, section_name, and the exam_str and adds a new column that is
               named '<section_name> Total'.

'''

def produce_distplot(path, gradebook_column, student_score, file_tag = "", out_of = 0, admin = False):

    plt.gcf().clf()
    try:
        os.remove(path+"images/"+file_tag+".png")
    except:
        pass
    sns.set_style('whitegrid')

    if admin:
        label = "Median"
    else:
        label = "Your Score"

    sorted_gb = gradebook_column.astype(int).sort_values().unique()

    if admin:
        pass
    else:
        idx = np.where(sorted_gb == student_score)[0][0]

    min_score = int(sorted_gb[0] - 5) if int(sorted_gb[0] - 5) >= 0 else 0

    n, bins, patches = plt.hist(gradebook_column.astype(int),
                                bins = len(gradebook_column.unique()), density = True, color = 'grey')
    dist_curve = sns.distplot(gradebook_column.astype(int), hist=False)

    patches[idx].set_fc('r')
    plt.xlabel("Score out of %s"%(out_of))
    plt.xlim([min_score,out_of])

    red_patch = mpatches.Patch(color = 'red', label = label)
    dist_curve.legend(handles=[red_patch])

    if not os.path.isdir(path+"images/"):
        os.makedirs(path+"images/")

    temp = dist_curve.get_figure()
    temp.savefig(path+"images/" +file_tag + ".png")

def produce_hist(path, gradebook_column, student_score, question, file_tag = "", out_of = 0, admin = False):
    '''
    Takes a gradebook column, a student's score, and the question in order to produce
    a detailed graph pertaining to their score on the exam.
    '''

    # clear working space
    plt.gcf().clf()
    try:
        os.remove(path+"images/"+file_tag+".png")
    except:
        pass

    scores = gradebook_column.unique().astype(int)
    scores.sort()
    student_score = int(student_score)
    if admin:
        label = "Median"
    else:
        label = "Your Score"
    # print(question)
    # print("using ", scores, " as scores")
    # print("using ", student_score, " as student score")

    clrs = ['red' if x == student_score else 'grey' for x in scores]
    # print("We are using ", clrs, " to color ", question)
    sns.set_style("whitegrid")
    red_patch = mpatches.Patch(color = 'red', label = label)
    student_score = sns.countplot(gradebook_column, palette=clrs)
    plt.ylabel("# of Students")
    plt.xlabel("Score out of %s"%(out_of))
    plt.xlim([-1,len(scores)])
    student_score.yaxis.set_major_locator(MaxNLocator(integer = True))
    student_score.legend(handles=[red_patch])

    if not os.path.isdir(path+"images/"):
        os.makedirs(path+"images/")

    temp = student_score.get_figure()
    temp.savefig(path+"images/" + file_tag + ".png")

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

def section_total(df, section_name, exam_structure):
    df[section_name + " Total"] = df[exam_structure[section_name][0].keys()].astype('int64').sum(axis=1)
    return df


'''
These functions are for formatting the PDF. They come in several flavors.

newpage: determines whether or not the current section should be placed on the next page or not.

fmt_section: formatting by section

fmt_question: formatting by question

fmt_header: formats the header

'''

def newpage(pdf):
    '''
    If the current section to be formatted is too close to the end of the page,
    it will create a new page for the PDF and format a line on the top properly.
    Should not return anything besides the pdf object
    Input:
    pdf: the current PDF being worked on

    Returns:
    Nothing, the original PDF object is modified without needing to return it.
    '''
    if pdf.get_y() > 200:
        pdf.add_page()
        pdf.ln(1)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())

def fmt_section(path, pdf, section_name, section_str, gradebook,
                exam_to_process, out_of, percentile_dict, align = "R", admin = False):
    # do some section formatting here

    file_tag = section_name.replace("\\", "").replace("/", "")

    if admin:
        comment = '''Number of students to score a 1: %s out of %s
        Percentage: %.2f'''%(sum(gradebook[section_name + " Total"] == 1), len(gradebook),
             ((sum(gradebook[section_name + " Total"] == 1)/len(gradebook))*100))

        score_report = '''
        Average Score: %.2f out of %s
        Median score: %s out of %s'''%(exam_to_process.loc['mean', section_name + " Total"], out_of,
             exam_to_process.loc['median', section_name + " Total"], out_of)

        produce_distplot(path, gradebook[section_name + " Total"], exam_to_process.loc['median', section_name + " Total"], file_tag = file_tag, out_of = out_of)

    else:
        comment_col = [col for col in gradebook.columns if section_name in col and "Total" not in col]
        print(exam_to_process[comment_col].values[0])
        comment_typecast = str(exam_to_process[comment_col].values[0].encode('UTF-8', 'ignore'))
        comment_typecast = comment_typecast[slice(2, len(comment_typecast)-1)]
        comment = "TA Comment: %s"%(comment_typecast)

        score_report = "\nScore: %s/%s"%(exam_to_process[section_name + " Total"], out_of)

        produce_distplot(path, gradebook[section_name + " Total"], exam_to_process[section_name + " Total"], file_tag = file_tag, out_of = out_of)

    print("Section %s is aligned %s"%(section_name, align))

    newpage(pdf)

    x_image, x_text = (110, 10) if align == "R" else (10, 110)

    align_image, align_text = ("R", "L") if align == "R" else ("L", "R")

    pdf.ln(1)
    pdf.set_font("Arial", size = 12)

    pdf.set_x(x_image)
    pdf.cell(90, 8, txt=section_name, align = align_image)

    temp = pdf.get_y()

    pdf.set_font("Arial", size = 10)
    pdf.set_x(x_text)
    pdf.ln(2)
    pdf.set_x(x_text)
    pdf.multi_cell(90, 5, txt=comment, align = "L", border = 0)
    temp2 = pdf.get_y()

    pdf.set_y(temp)
    pdf.ln(4)
    pdf.set_x(x_image)
    pdf.cell(90, 8, txt=score_report, align = align_image)
    pdf.ln(6)


    pdf.image(path+"images/" + file_tag + ".png", x = x_image, w = 90)

    # do some question formatting here
    pdf.ln(2)

    y_space = pdf.get_y() if temp2 < pdf.get_y() else temp2

    for item in section_str.items():
        align = "L" if align == "R" else "R"

        pdf.line(10, y_space, 200, y_space)

        fmt_question(path = path, pdf = pdf, question_name = item[0], question_text = item[1][0],
                     gradebook = gradebook, exam_to_process = exam_to_process,
                     out_of = item[1][1], align = align, admin = admin)

        pdf.ln(2)
        y_space = pdf.get_y()
        pdf.line(10, y_space, 200, y_space)


def fmt_question(path, pdf, question_name, question_text, gradebook,
                 exam_to_process, out_of, align = "R", admin = False):

    file_tag = question_name.replace("\\", "").replace("/", "")

    if admin:
        comment = '''Number of students to score a 1: %s out of %s
        Percentage: %.2f'''%(sum(gradebook[question_name] == 1), len(gradebook),
             (sum(gradebook[question_name] == 1)/len(gradebook))*100)

        score_report = '''
        Average Score: %.2f out of %s
        Median score: %s out of %s'''%(exam_to_process.loc['mean', question_name], out_of,
             exam_to_process.loc['median', question_name], out_of)

        produce_hist(path, gradebook[question_name], exam_to_process.loc['median', question_name], question_name, file_tag = file_tag, out_of = out_of, admin = admin)

    else:
        comment_typecast = str(exam_to_process[question_name + " Comment"].encode('UTF-8', 'ignore'))
        comment_typecast = comment_typecast[slice(2, len(comment_typecast)-1)]
        comment = "TA Comment: %s"%(comment_typecast)

        score_report = "\nScore: %s/%s"%(exam_to_process[question_name], out_of)

        produce_hist(path, gradebook[question_name], exam_to_process[question_name], question_name, file_tag = file_tag, out_of = out_of)


    print(question_name, " is aligned ", align)

    newpage(pdf)

    x_image, x_text = (10, 110) if align == "L" else (110, 10)

    align_image, align_text = ("R", "L") if align == "R" else ("L", "R")

    pdf.ln(1)
    pdf.set_font("Arial", size = 11)

    temp_y = pdf.get_y()

    pdf.set_x(x_image)
    pdf.cell(90, 4, txt=question_name+" : "+question_text, align = align_image)
    pdf.ln(1)
    pdf.set_font("Arial", size = 9)
    pdf.set_x(x_image)
    pdf.multi_cell(90, 4, txt=score_report, align = align_image)

    temp = pdf.get_y()

    pdf.set_font("Arial", size = 10)
    pdf.set_x(x_text)
    pdf.ln(2)
    pdf.set_xy(x_text, temp_y)
    pdf.multi_cell(90, 5, txt=comment, align = "L", border = 0)

    temp_y = pdf.get_y()

    pdf.set_y(temp)
    pdf.image(path+"images/" + file_tag + ".png", x = x_image, w = 90)
    if pdf.get_y < temp_y:
        pdf.set_y(temp_y)

'''
Legacy might be reintroduced in a further refactor

def fmt_header(pdf, student_id, gradebook, exam_str, percentile_dict, admin = False):
    # filter DF into series for easy manipulation
    exam_to_process = gradebook[gradebook['Student ID'] == student_id]
    exam_to_process = exam_to_process.iloc[-1]

    # extract repeated information
    grader = exam_to_process['Grader']
    tag = list(exam_str.keys())[0]
    file_name = exam_to_process['name'].strip()+"_"+tag+".pdf"
    total_score = exam_to_process['Total Score']

    # set up text info
    intro = "\t\t\t\tThis is your exam report for the %s. Your grader was %s, so please feel free to reach out to them if you have additional questions about the exam, or any of the grades you received."%(tag, grader)
    temp_comment = "GAMBATE!!!"

    print("All done!\n\n\n\n", "*"*50)

    # initiate PDF object, format header

    pdf = FPDF()
    pdf.add_page()
    pdf.image("./structure_files/nycdsalogo.png", x=55, y=8, w=100)

    pdf.set_line_width(0.5)
    pdf.set_fill_color(255, 0, 0)
    pdf.line(10, 35, 200, 35)

    pdf.set_font("Arial", size=10)
    pdf.ln(30)
    pdf.cell(190, 6, txt="Hello %s,"%(exam_to_process['name']), ln=1, align="L")
    pdf.ln(2)
    pdf.multi_cell(190, 6, txt=intro, align = "L")

    pdf.ln(5)
    pdf.set_font("Arial", size = 12)
    pdf.cell(95, 8, txt="Overall: %s out of %s"%(exam_to_process['Total Score'], exam_str[tag][1]), ln = 0, align="L")

    temp_y = pdf.get_y()
    pdf.set_font("Arial", size = 10)

    produce_distplot(gradebook['Total Score'].astype(int), exam_to_process['Total Score'],
                     file_tag = "Overall_Graph", out_of = exam_str[tag][1])

    pdf.image("./images/Overall_Graphtemp_report.png",
              x = 110,
              w = 90)
    final_y = pdf.get_y()

    pdf.set_y(temp_y)
    pdf.ln(4)
    pdf.cell(90, 8, txt="Which places you at the %s percentile."%(percentile_dict['Total Score'][str(exam_to_process['Total Score'])]), align = "L")
    pdf.ln(8)
    pdf.multi_cell(90, 5, txt="Overall Comment: {}".format(exam_to_process['Exam Comment']), align = 'L', border = 0)

    pdf.set_y(final_y)

    pdf.line(10, final_y, 200, final_y)

    pdf.ln(2)

    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

'''

'''
These functions process the gradebook.

process_gradebook: processes the entire gradebook

process_single_report: process a single row of the gradebook, or process the overall report.

process_gradebook will call process_single_report, while also generating the percentile_dict
required to run process_single_report.
'''

def process_gradebook(gradebook, student_keys, exam_str, path="./", admin_only = False):
    '''
    Main method of the report generator. Sets up a gradebook to be processed
    by the process_single_report function. By default will also generate an admin report.
    The reports are based on the exam_str, which is a dictionary as seen below:
    {"Example Exam" : ({"Section 1" : ({"Question 1" : ("Binary Search", 5),
                                        "Question 2" : ("Object Oriented", 10)}, 15)}, 15)}
    This dictonary needs to have matching names with the gradebook columns, as a mismatch will
    throw an error. This information will be stored in the exam_structure file, and should only
    be modified when the exam is updated.

    Inputs:
    gradebook: a gradebook of graded student exams.
    student_keys: key linkining submissions to the students real names
    exam_str: the structure of the exam in question
    admin: (might remove) toggle generating overall report

    Returns:
    gradebook: a gradebook of graded student exams, with aggregation columns
               (i.e., "Total Score"), as well as the names attached to the student
               IDs.
    It saves the files to a [FOLDER PATH] specified.
    '''

    print("*"*50, "\n", "Diagnostic", "\n", exam_str[0])

    exam_str = exam_str[0]

    if path[-1] != "/":
        path += "/"

    if not os.path.isdir(path):
        raise ValueError("The path specified does not exist.")

    if admin_only:
        pass
    else:
        student_keys = student_keys[['name', 'student_id']]

        student_keys.loc[::,'name'] = student_keys['name'].str.replace("\W['\"]|['\"]\W", "")
        student_keys.loc[::,'name'] = student_keys['name'].str.replace("^\s", "")

        #print(student_keys.columns)
        #print(gradebook.columns)

        gradebook_names = pd.merge(gradebook, student_keys, how = 'left', left_on = 'Student ID', right_on = 'student_id')

        gradebook_names.drop('student_id', axis = 1, inplace=True)

        gradebook_names.dropna(inplace=True)


    print("Past first block")

    tag = list(exam_str.keys())[0]

    print("*"*50, "\n", tag, "\n", "*"*50)

    to_sum = []
    to_percentile = ['Total Score']

    print("passing ", exam_str[tag])
    for item in exam_str[tag][0].items():
        print("Inside for-loop, currently on ", item)
        if type(item[1][0]) == dict:
            ## process section
            print("Section name:", item[0])
            if admin_only:
                gradebook = section_total(gradebook, item[0], exam_str[tag][0])
            else:
                gradebook_names = section_total(gradebook_names, item[0], exam_str[tag][0])
            to_sum.append(item[0] + " Total")
            to_percentile.append(item[0] + " Total")
    #         print("Out of", item[1][1])
    #         print(example_df[item[0] + " Total"].head(5))

        elif type(item[1][0] == str):
            ## process question
            to_sum.append(item[0])
    print(to_sum)
    print(to_percentile)
    if admin_only:
        gradebook['Total Score'] = gradebook[to_sum].astype('int64').sum(axis=1)

        percentile_dict = {question:percentile(gradebook[question]) for question in to_percentile}

#         num_ids = len(gradebook['Student ID'].unique())

    else:
        gradebook_names['Total Score'] = gradebook_names[to_sum].astype('int64').sum(axis=1)

        percentile_dict = {question:percentile(gradebook_names[question]) for question in to_percentile}

        num_ids = len(gradebook_names['Student ID'].unique())

    i = 1

    if admin_only:
        print("Creating admin report")
        process_single_report(path = path, student_id = "", gradebook = gradebook,
                              exam_str = exam_str, percentile_dict = percentile_dict, admin = True)
        return gradebook
    else:
        for student_id in gradebook_names['Student ID'].unique():
            print("Processing exam %s of %s"%(i, num_ids))
            process_single_report(path = path, student_id = student_id, gradebook = gradebook_names,
                                   exam_str = exam_str, percentile_dict = percentile_dict)
            i += 1
        print("Processing Admin Report")
        process_single_report(path = path, student_id = "Admin"+tag, gradebook = gradebook_names,
                              exam_str = exam_str, percentile_dict = percentile_dict, admin = True)
        return gradebook_names


def process_single_report(path, student_id, gradebook, exam_str, percentile_dict, admin = False):
    '''

    '''

    # generated regardless of type
    tag = list(exam_str.keys())[0]
    out_of = exam_str[tag][1]

    if admin:
        pass
        # do some Stuff
        exam_to_process = gradebook.agg(["median", 'mean'])
        total_score_mean = exam_to_process.loc['mean', 'Total Score']
        total_score_median = exam_to_process.loc['median', 'Total Score']

        file_name = "Overall_Student_Report_"+tag.replace(" ", "") + ".pdf"
        grader = "Admin Report"

        intro = '''This is the overall exam report for %s.'''%(tag)

        score_report = '''
        Average Score: %.2f out of %s
        Median Score: %s out of %s'''%(total_score_mean, out_of,
                            total_score_median, out_of)

        produce_distplot(path, gradebook['Total Score'], int(total_score_median),
                         file_tag = "Overall_Graph", out_of = out_of)


    else:
        # filter DF into series for easy manipulation
        exam_to_process = gradebook[gradebook['Student ID'] == student_id]
        exam_to_process = exam_to_process.iloc[-1]

        # extract repeated information
        grader = exam_to_process['Grader']
        file_name = exam_to_process['name'].strip()+"_"+tag+".pdf"
        total_score = exam_to_process['Total Score']

        # set up text info
        intro = '''Hello %s,
        \t\tThis is your exam report for the %s. Your grader was %s, so please feel free to reach out to them if you have additional questions about the exam.'''%(exam_to_process['name'], tag, grader)

        comment_typecast = str(exam_to_process["Exam Comment"].encode('UTF-8', 'ignore'))
        comment_typecast = comment_typecast[slice(2, len(comment_typecast)-1)]

        score_report = '''
        Overall: %s out of %s
        Which places you at the %s percentile.\n\n
        Overall Comment: %s'''%(exam_to_process['Total Score'], out_of,
             percentile_dict['Total Score'][str(total_score)],
             comment_typecast)

        print("*"*50, "\n", path, "\n", "*"*50)

        produce_distplot(path, gradebook['Total Score'].astype(int), exam_to_process['Total Score'],
                         file_tag = "Overall_Graph", out_of = out_of)

    print("All done!\n\n\n\n", "*"*50)

    # initiate PDF object, format header

    pdf = FPDF()
    pdf.add_page()
    pdf.image("./structure_files/nycdsalogo.png", x=55, y=8, w=100)

    pdf.set_line_width(0.5)
    pdf.set_fill_color(255, 0, 0)
    pdf.line(10, 35, 200, 35)

    pdf.set_font("Arial", size=10)
    pdf.ln(30)
    pdf.multi_cell(190, 6, txt=intro, align="L")
    pdf.ln(2)

    y_image = pdf.get_y()

    pdf.ln(2)
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(95, 6, txt=score_report, align="L")

    pdf.set_font("Arial", size = 10)

    pdf.set_y(y_image)
    pdf.image(path+"images/Overall_Graph.png",
              x = 110,
              w = 90)

    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(2)

    pdf.line(10, pdf.get_y(), 200, pdf.get_y())


    alignment = "R"

    for item in exam_str[tag][0].items():
        alignment = "L" if alignment == "R" else "R"
        if type(item[1][0]) == dict:
            ## process section
            print("Section name:", item[0])
            fmt_section(path = path, pdf = pdf, section_name = item[0], section_str = item[1][0],
                        gradebook = gradebook, exam_to_process = exam_to_process,
                        out_of = item[1][1], percentile_dict = percentile_dict, align = alignment, admin = admin)

        elif type(item[1][0] == str):
            ## process question
            print("Question name:", item[0])
            fmt_question(path = path, pdf = pdf, question_name = item[0], question_text = item[1][0],
                         gradebook = gradebook, exam_to_process = exam_to_process,
                         out_of = item[1][1], align = alignment, admin = admin)

        pdf.ln(2)
        y_space = pdf.get_y()
        pdf.line(10, y_space, 200, y_space)

    if not os.path.isdir(path+"reports/"):
        os.makedirs(path+"reports/")

    pdf_path = path+"reports/"+student_id+".pdf"
    pdf_path = pdf_path.replace('\u2019', "")
    print(pdf_path)
    pdf.output(pdf_path)
