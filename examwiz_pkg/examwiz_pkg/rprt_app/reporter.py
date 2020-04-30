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
    '''
    Takes a path (to save the image), a column that you would like to visualize,
    the student's score (so that it may be highlighted on the graph), a file_tag (in case for special naming),
    out_of which represents how many points the question is out of, and admin which is True only when generating
    the Overall Report.

    input:
    path: Path to where the images subfolder will be made to contain the pngs that are produced. (str)
    gradebook_column: the column of the gradebook to visualize (pd.Series)
    student_score: the individual student's score (this will be metadata in the Overall/Admin report) (int)
    file_tag: additional file name information. (str)
    out_of: Number of points the question is out of (int)
    admin: Whether of not we are producing the Overall/Admin report (boolean)

    returns:
    None: No return type, as it saves the image to be used later.
    '''

    # gotta clear the plot space
    plt.gcf().clf()

    # remove the old image (sometimes there is a bug where it won't save over the old image, so
    # we need to make sure to remove it here)
    try:
        os.remove(path+"images/"+file_tag+".png")
    except:
        pass

    # general formatting
    sns.set_style('whitegrid')
    if admin:
        label = "Median"
    else:
        label = "Your Score"

    # make sure the bars are in order
    sorted_gb = gradebook_column.sort_values().unique()

    # get the idx of which bar should be highlighted to represent what the student scored
    if admin:
        pass
    else:
        idx = np.where(sorted_gb == student_score)[0][0]

    # if the lowest score someone got is greater than 5, set the lower bound of the graph
    # to be that minimum score minus 5.
    min_score = int(sorted_gb[0] - 5) if int(sorted_gb[0] - 5) >= 0 else 0

    # decompose the graph elements so we can highlight the right path
    # I don't like the Seaborn histogram, so instead I decide to make one in matplotlib
    # and stack the distribution plot ontop of it.
    n, bins, patches = plt.hist(gradebook_column,
                                bins = len(gradebook_column.unique()), density = True, color = 'grey')
    dist_curve = sns.distplot(gradebook_column, hist=False)

    # if we are not generating the overall report, we now highlight the bar that represents the
    # student's score on the exam.
    if not admin:
        patches[idx].set_fc('r')
        red_patch = mpatches.Patch(color = 'red', label = label)
        dist_curve.legend(handles=[red_patch])

    # make my labels nice, and set my x-limits.
    plt.xlabel("Score out of %s"%(out_of))
    plt.xlim([min_score,out_of])

    # make sure my path exists
    if not os.path.isdir(path+"images/"):
        os.makedirs(path+"images/")

    # actually save the PNG
    temp = dist_curve.get_figure()
    temp.savefig(path+"images/" +file_tag + ".png")

def produce_hist(path, gradebook_column, student_score, question, file_tag = "", out_of = 0, admin = False):
    '''
    Takes a gradebook column, a student's score, and the question in order to produce
    a detailed graph pertaining to their score on the exam.

    input:
    path: Path to where the images subfolder will be made to contain the pngs that are produced. (str)
    gradebook_column: the column of the gradebook to visualize (pd.Series)
    student_score: the individual student's score (this will be metadata in the Overall/Admin report) (int)
    file_tag: additional file name information. (str)
    out_of: Number of points the question is out of (int)
    admin: Whether of not we are producing the Overall/Admin report (boolean)

    returns:
    student_score: Score student got on this question.

    '''

    # clear working space
    plt.gcf().clf()

    # remove old image
    try:
        os.remove(path+"images/"+file_tag+".png")
    except:
        pass

    # want to get only unique scores
    scores = gradebook_column.unique()
    scores.sort()

    # shouldn't need this anymore....
    # student_score = int(student_score)

    # get my labels nice
    label = "Median" if admin else "Your Score"

    # print(question)
    # print("using ", scores, " as scores")
    # print("using ", student_score, " as student score")

    # this is the way we handle the red patch in these scores, we know that
    # the corresponding bar will be the one we want to paint red instead of
    # grey.
    clrs = ['red' if x == student_score else 'grey' for x in scores]

    # to check if we are using the right colors
    # print("We are using ", clrs, " to color ", question)

    # nice formatting, set patch to red
    sns.set_style("whitegrid")
    red_patch = mpatches.Patch(color = 'red', label = label)
    student_score = sns.countplot(gradebook_column, palette=clrs)
    plt.ylabel("# of Students")
    plt.xlabel("Score out of %s"%(out_of))
    plt.xlim([-1,len(scores)])
    student_score.yaxis.set_major_locator(MaxNLocator(integer = True))
    student_score.legend(handles=[red_patch])

    # make sure path exists
    if not os.path.isdir(path+"images/"):
        os.makedirs(path+"images/")

    # save the image to a png
    temp = student_score.get_figure()
    temp.savefig(path+"images/" + file_tag + ".png")

    return student_score

def percentile(lst):
    '''
    Takes a list and produces percentile numbers for said list.
    Returns a dictonary containing the score and what percentile that
    score comapares to.

    input:
    lst: A list of numbers to convert to percentiles

    returns:
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
    '''
    Takes a gradebook, along with an associated section_name and the exam_structure
    (i.e., the part that actually represents the structure of the section_name) and
    creates the total for that section. This information is not stored in the gradebook
    online because we can generate it here, and also reduces the chance for user error
    when entering in numbers.

    Note that this foces the datatype to 'int64', as well as creating a new column that
    is the sum of the questions in that section, with the column name section_name + ' Total'
    i.e., 'Building the Forest Total'. Returns the whole dataframe with the updated columns.

    input:
    df: a gradebook (pandas.DataFrame)
    section_name: the name of the section you are trying to total (note, totalling the whole exam is done later) (str)
    exam_structure: A nested dictonary taken from exam_details.json that contains what sections contain which questions.

    returns:
    df: all questions designated by the questions contained in section_name will have their datatype changed to 'int64',
        and a new column will be added called section_name + " Total" (i.e., 'Building the Forest Total')
    '''
    df.loc[::,exam_structure[section_name][0].keys()] = df.loc[::,exam_structure[section_name][0].keys()].astype('int64')
    df[section_name + " Total"] = df[exam_structure[section_name][0].keys()].sum(axis=1)
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

    Input:
    pdf: the current PDF being worked on

    Returns:
    Nothing, the original PDF object is modified without needing to return it.
    '''

    # I found 200 is the value that works the best here.
    # We also add a line at the top for consistent formatting.
    if pdf.get_y() > 200:
        pdf.add_page()
        pdf.ln(1)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())

def fmt_section(path, pdf, section_name, section_str, gradebook,
                exam_to_process, out_of, percentile_dict, align = "R", admin = False):
    '''
    This is for processing sections of the exam at a time. It will eventually call fmt_question,
    but we need to do some handling with the section (i.e., section score and comment) before we
    can move on to the individual questions.

    This function should only be called by the process_single_report, and all arguements are
    inherited from that function call.

    input:
    path: path to parent folder (str)
    pdf: the pyPDF object that represents the current report (FPDF)
    section_name: the name of the section we are currently formatting (str)
    section_str: the nested dictionary contained at exam_str[section_name][0] (dict)
    gradebook: the gradebook we are processing (pd.DataFrame)
    exam_to_process: the individual student's exam (or overall report) we are processing (pd.Series)
    out_of: Score that the section is out of, stored in exam_str[section_name][1] (int)
    percentile_dict: the dictionary containing percentile information for the exam (dict)
    align: what the current alignment is (str)
    admin: whether or not we are generating the overall report (boolean)

    returns:
    None: should just modify the FPDF object.
    '''

    # gotta make sure section name doesn't have any bad characters in it
    file_tag = section_name.replace("\\", "").replace("/", "")

    # handle overall report vs individual
    if admin:
        comment = '''Number of students to score a 1: %s out of %s
        Percentage: %.2f'''%(sum(gradebook[section_name + " Total"] == 1), len(gradebook),
             ((sum(gradebook[section_name + " Total"] == 1)/len(gradebook))*100))

        score_report = '''
        Average Score: %.2f out of %s
        Median score: %s out of %s'''%(exam_to_process.loc['mean', section_name + " Total"], out_of,
             exam_to_process.loc['median', section_name + " Total"], out_of)

        produce_distplot(path, gradebook[section_name + " Total"], exam_to_process.loc['median', 
        	section_name + " Total"], file_tag = file_tag, out_of = out_of, admin = admin)

    else:
        # We know the setion_name should be a column, this might be able to be refactored into just keying into the DF/series
        comment_col = [col for col in gradebook.columns if section_name in col and "Total" not in col]
        print(exam_to_process[comment_col].values[0])
        comment_typecast = str(exam_to_process[comment_col].values[0]).encode('UTF-8', 'ignore')
        comment_typecast = comment_typecast[slice(2, len(comment_typecast)-1)]
        comment = "TA Comment: %s"%(comment_typecast)

        score_report = "\nScore: %s/%s"%(exam_to_process[section_name + " Total"], out_of)

        produce_distplot(path, gradebook[section_name + " Total"], exam_to_process[section_name + " Total"], file_tag = file_tag, out_of = out_of)

    print("Section %s is aligned %s"%(section_name, align))

    # after printing out a large section, we always want to make sure we check whether or not
    # we need to move to a new page.
    newpage(pdf)

    # this is the second part of the align magic, while we know what "L" and "R" stand for as people,
    # the computer only half understands us. So we need to fill in the missing place, which is the
    # x coordinate in our PDF. Images on the right side imply that images need to be at x = 110 with
    # text at x = 110, while images on the left side (i.e., align = "L"), will have x_image = 10 and
    # x_text = 110. We do the same thing for ease of implementation with align_image and align_text.
    x_image, x_text = (110, 10) if align == "R" else (10, 110)
    align_image, align_text = ("R", "L") if align == "R" else ("L", "R")

    pdf.ln(1)
    pdf.set_font("Arial", size = 12)

    pdf.set_x(x_image)
    pdf.cell(90, 8, txt=section_name, align = align_image)

    # we want to store this so we can make sure everything is formatted under where the question
    # or section total is printed.
    temp = pdf.get_y()

    # some font sizing and random formatting, for some reason we need to set_x here twice, as
    # the pdf.ln needs it but also resets our x value at the same time.
    pdf.set_font("Arial", size = 10)
    pdf.set_x(x_text)
    pdf.ln(2)
    pdf.set_x(x_text)
    pdf.multi_cell(90, 5, txt=comment, align = "L", border = 0)

    # this get_y represents the bottom of the comment part of the formatting.
    temp2 = pdf.get_y()

    pdf.set_y(temp)
    pdf.ln(4)
    pdf.set_x(x_image)
    pdf.cell(90, 8, txt=score_report, align = align_image)
    pdf.ln(6)


    pdf.image(path+"images/" + file_tag + ".png", x = x_image, w = 90)

    # do some question formatting here
    pdf.ln(2)

    # if temp2 is less than our current y, (i.e., the y under the image), then we
    # want to use the y below the image to format (image goes below comment). Otherwise,
    # we want to use the y value set at temp2 if the comment goes below the image for
    # proper formatting.
    y_space = pdf.get_y() if temp2 < pdf.get_y() else temp2

    # now we move on to processing the individual sections
    for item in section_str.items():
        # flip the alignment
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
    '''
    Handles formatting the individual questions of the exam. Either called by fmt_section or
    process_single_report, and inherits all arguements from whichever function called it.

    General idea is to have the name of the question on top, with the student's score underneath.
    Below that is an image of the distribution of scores in their cohort, and then next to that is
    the comment that is left by the TA. There is a line that goes above and below each question in
    order to section them off.

    inputs:
    path: path to parent folder (str)
    pdf: the pyPDF object that represents the current report (FPDF)
    section_name: the name of the section we are currently formatting (str)
    section_str: the nested dictionary contained at exam_str[section_name][0] (dict)
    gradebook: the gradebook we are processing (pd.DataFrame)
    exam_to_process: the individual student's exam (or overall report) we are processing (pd.Series)
    out_of: Score that the section is out of, stored in exam_str[section_name][1] (int)
    percentile_dict: the dictionary containing percentile information for the exam (dict)
    align: what the current alignment is (str)
    admin: whether or not we are generating the overall report (boolean)

    returns:
    None: modifies original fPDF object.

    N.B.: line-by-line comments were omitted from this function because it is extremely similar to
          the fmt_section code, and functionality can be inferred from above.
    '''
    file_tag = question_name.replace("\\", "").replace("/", "")

    if admin:
        comment = '''Number of students to score a 1: %s out of %s
        Percentage: %.2f'''%(sum(gradebook[question_name] == 1), len(gradebook),
             (sum(gradebook[question_name] == 1)/len(gradebook))*100)

        score_report = '''
        Average Score: %.2f out of %s
        Median score: %s out of %s'''%(exam_to_process.loc['mean', 
        	question_name], out_of, exam_to_process.loc['median', question_name], 
        	out_of)

        produce_hist(path, gradebook[question_name], 
        	exam_to_process.loc['median', question_name], 
        	question_name, file_tag = file_tag, out_of = out_of, admin = admin)

    else:
        comment_typecast = str(exam_to_process[question_name + 
        	" Comment"].encode('UTF-8', 'ignore'))
        comment_typecast = comment_typecast[slice(2, len(comment_typecast)-1)]
        comment = "TA Comment: %s"%(comment_typecast)

        score_report = "\nScore: %s/%s"%(exam_to_process[question_name], out_of)

        produce_hist(path, gradebook[question_name], 
        	exam_to_process[question_name], question_name, 
        	file_tag = file_tag, out_of = out_of)


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
    if pdf.get_y() < temp_y:
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
    **NOTE: YOU CAN ALSO FIND A MORE INDEPTH GUIDE (AS WELL AS METHODS TO CREATE ONE IN
      ~/exam_wizard/structure_files/exam_structure_updater.ipynb)
    This dictonary needs to have matching names with the gradebook columns, as a mismatch will
    throw an error. This information will be stored in the exam_structure file, and should only
    be modified when the exam is updated.

    Inputs:
    gradebook: a gradebook of graded student exams.
    student_keys: key linkining submissions to the students real names
    exam_str: the structure of the exam in question
    admin_only: generate just the overall report

    Returns:
    gradebook: a gradebook of graded student exams, with aggregation columns
               (i.e., "Total Score"), as well as the names attached to the student
               IDs.
    It saves the files to a [FOLDER PATH] specified.
    '''

    print("*"*50, "\n", "Diagnostic", "\n", exam_str[0])

    # save the structure of the exam as a dictionary
    exam_str = exam_str[0]

    # make sure that the path starts with '/'
    if path[-1] != "/":
        path += "/"

    if not os.path.isdir(path):
        raise ValueError("The path specified does not exist.")


	##################### Merge the student_keys file with the gradebook file #####################
    if admin_only:
        pass
    else:
    	# subsetting the dataset
        student_keys = student_keys[['name', 'student_id']]

        # needs to fix this part!!!!
        student_keys.loc[::,'name'] = student_keys['name'].str.replace("\W['\"]|['\"]\W", "")
        student_keys.loc[::,'name'] = student_keys['name'].str.replace("^\s", "")

        # right merge of gradebook with student_keys on 'Student ID'
        gradebook_names = pd.merge(gradebook, student_keys, how = 'right', left_on = 'Student ID', 
        	right_on = 'student_id')

        # drop the repeated column
        gradebook_names.drop('student_id', axis = 1, inplace=True)

        # drop nas; though it is not that necessary
        gradebook_names.dropna(inplace=True)

    ###############################################################################################
    
    print("Past first block")

    # get the name of the exam, i.g. 'Python Exam'
    tag = list(exam_str.keys())[0]

    print("*"*50, "\n", tag, "\n", "*"*50)

    # empty bracket 
    to_sum = []
    to_percentile = ['Total Score']


    # here we use exam_str to parse the exam into questions and sections.
    print("Processing " + tag + ' Structure:')
    for item in exam_str[tag][0].items():
        print("Inside for-loop, currently on ", item)

        # this is to determine if there is subsection
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

    	# this is when there is no subsection
        elif type(item[1][0] == str):
            ## process question
            ## this is like a small version of section_total
            to_sum.append(item[0])

            # Convert the score of each question to numeric
            #gradebook.loc[::,item[0]] = gradebook.loc[::,item[0]].astype('int64')
            gradebook_names[[item[0]]] = gradebook_names[[item[0]]].apply(pd.to_numeric)

            gradebook[[item[0]]] = gradebook[[item[0]]].apply(pd.to_numeric)

    print(to_sum)
    print(to_percentile)


    # now that we've collected which questions and sections should be added up to
    # our total score, we can actually sum our total score using to_sum, which is
    # all of the numeric columns. This will be stored in 'Total Score'.

    # We also generate a dictonary where each key is the name of the qeustion, and
    # the value is the percentile number generated by the *percentile()* function
    # and then saved to percentile_dict.

    if admin_only:
        gradebook['Total Score'] = gradebook[to_sum].sum(axis=1)

        percentile_dict = {question:percentile(gradebook[question]) for question in to_percentile}


    else:
        gradebook_names['Total Score'] = gradebook_names[to_sum].sum(axis=1)

        percentile_dict = {question:percentile(gradebook_names[question]) for question in to_percentile}

        num_ids = len(gradebook_names['Student ID'].unique())

    i = 1

    # and at this point we've done most of the pre-processing, so we can now go on to
    # generating the individual reports. We will always generate the admin report, but
    # we can choose not to produce the student reports by including the admin_only = True.
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
    Takes a single row of the gradebook and processes it into a PDF. This requires several components to work,
    namely, a path to where the file should be generated, the ID of the student, the gradebook itself, the
    structure of the exam, and the dictonary of all the percentiles for question scores. These are listed
    clearly below. If this function is called through process_gradebook, it shouldn't have a problem with the
    arguements.

    input: (inherited from process_gradebook when called from the above function unless otherwise specified)
    path: Path to where the file should be put.
    student_id: the ID of the student in order to isolate the row
    gradebook: the dataframe of student scores on the exam.
    exam_str: the exam structure as read from exam_details.json in the structure_files subfolder.
    percentile_dict: a dictonary of percentiles for each question and section. Keys are question or
                     section names, which gives way to a nested dictonary that has possible scores as
                     the keys, and the percentiles that those scores place the sutdent in as values.
    admin: Whether or not we are generating the admin (overall) report.

    returns:
    None: Does not return anything, instead outputs a PDF file which has the same name as the studentID.
    '''

    # generated regardless of type
    tag = list(exam_str.keys())[0]

    # the highest possible score for the exam
    out_of = exam_str[tag][1]


    if admin:
        # We want to get some meta-data in order view different aspects of the overall report,
        # the basic statistics we aggregate are median and mean for each question.
        exam_to_process = gradebook.agg(["median", 'mean'])
        total_score_mean = exam_to_process.loc['mean', 'Total Score']
        total_score_median = exam_to_process.loc['median', 'Total Score']

        #file_name = "Overall_Student_Report_"+tag.replace(" ", "") + ".pdf"
        filename = 'admin_report'
        grader = "Admin Report"

        intro = '''This is the overall exam report for %s.'''%(tag)

        score_report = '''
        Average Score: %.2f out of %s
        Median Score: %s out of %s'''%(total_score_mean, out_of,
                            total_score_median, out_of)

        produce_distplot(path, gradebook['Total Score'], int(total_score_median),
                         file_tag = "Overall_Graph", out_of = out_of, admin = admin)


    else:
        # filter DF into series for easy manipulation
        exam_to_process = gradebook[gradebook['Student ID'] == student_id]
        exam_to_process = exam_to_process.iloc[-1]

        # extract repeated information
        grader = exam_to_process['Grader']

        # we extract the first name of the student as the filename
        filename = exam_to_process['name'].split()[0].strip()

        #file_name = exam_to_process['name'].strip()+"_"+tag+".pdf"
        total_score = exam_to_process['Total Score']

        # set up text info
        intro = '''Hello %s,
        \t\tThis is your exam report for the %s. Your grader was %s, so please feel free
         to reach out to them if you have additional 
         questions about the exam.'''%(exam_to_process['name'], tag, grader)

        comment_typecast = str(exam_to_process["Exam Comment"].encode('UTF-8', 'ignore'))
        comment_typecast = comment_typecast[slice(2, len(comment_typecast)-1)]

        score_report = '''
        Overall: %s out of %s
        Which places you at the %s percentile.\n\n
        Overall Comment: %s'''%(exam_to_process['Total Score'], out_of,
             percentile_dict['Total Score'][str(total_score)],
             comment_typecast)

        print("*"*50, "\n", path, "\n", "*"*50)

        # create a distribution for the overall score.
        produce_distplot(path, gradebook['Total Score'].astype(int), 
        	exam_to_process['Total Score'], file_tag = "Overall_Graph", out_of = out_of)

    

    # initiate PDF object, format header

    pdf = FPDF()
    pdf.add_page()
    pdf.image("./structure_files/nycdsalogo.png", x=55, y=8, w=100)

    pdf.set_line_width(0.5)
    pdf.set_fill_color(255, 0, 0)
    pdf.line(10, 35, 200, 35)

    pdf.set_font("Arial", size=11)
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

    # a brief note on the alternating format of the PDF: we handle this via an if/else
    # below, where if alignment is either "L" or "R", it is switched to be the opposite.
    # this allows us to easily go between the left handed and right handed formats. We decide to
    # start with "R", which will give us "L" when formatting the first section or question.
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

    # make sure the path to the reports exists!
    if not os.path.isdir(path+"reports/"):
        os.makedirs(path+"reports/")

    # and then generate the report, along with printing the pdf_path for a quick sanity check.
    pdf_path = path+"reports/"+filename+".pdf"
    #pdf_path = path+"reports/"+student_id+".pdf"
    #pdf_path = pdf_path.replace('\u2019', "")
    print(pdf_path)
    print("Report generated!\n\n\n\n", "*"*50)
    pdf.output(pdf_path)
