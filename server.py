from flask import request
from flask import Flask, render_template, json,make_response
app = Flask(__name__)
import sys
import os
import re
import math
import string
import json
from jinja2 import evalcontextfilter, Markup, escape

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/searchbytags')
def searchbytags():

  return render_template('searchbytags.html')

# @app.route('/searchbymajor', methods=['GET','POST'])
# def searchbymajor():
#     string_no="No file selected."
#     file_name=request.form.getlist('SelBranch')
#     st=""
#     for f in file_name:
#         st+=str(f)
#         st+="\n"
    
#     if len(st)!=0:   
#     #     return render_template('searchbymajor.html', po=open(file_name).read())
#         return render_template('searchbymajor.html', po=st.replace('\n', Markup('<br>\n')))
#     else:
#         return render_template('searchbymajor.html', po=string_no)

@app.route('/searchbymajor')
def searchbymajor():
  return render_template('searchbymajor.html')
@app.route('/about')
def about():
  return render_template('about.html')
# @app.route('/searchbytags')
# def searchbytags():
#   return redirect('searchbytags.html')

# @app.route('/my-link/')
# def my_link():
#   print 'I got clicked!'

#   return 'Click.'


# @app.route('/searchbymajor', methods=['GET','POST'])
# def three_scores():
#     string_no="No file selected."
#     file_name=request.form['SelBranch']
#     # if file_name:   
#     #     return render_template('searchbymajor.html', po=open(file_name).read())
#     return render_template('searchbymajor.html', po=string_no)
    
def tf(foldername):
    #dlist: filepath, dictionary
    dlist = {}
    df = {}
    #dict: tf, idf, tfidf
    #loop in one file
    for filepath in foldername:
        dict = {}
        input_file = open(filepath, 'r')
        for line in input_file:
            line = re.sub('[^0-9a-zA-Z]+', ' ', line)
            words = line.split()
            for word in words:
                word = word.lower()
                if len(word) > 2:
                    if word in dict:
                        dict[word] =(dict[word][0] + 1, 0, 0)
                    else:
                        dict[word] = (1, 0, 0)
        for word in dict:
            if word in df:
                df[word] = df[word] + 1
            else:
                df[word] = 1
        dlist[filepath] = dict
        #print dict
    #end loop
    #print df


    #calculate log-weighted term frequency: 1+log(tf)
    #and the log-weighted inverse document frequency: log (N/df)
    #and TFIDF = tf*idf
    #and normalized
    for filepath in dlist:
        for word in dlist[filepath]:
            dlist[filepath][word] = (1 + math.log10(dlist[filepath][word][0]), math.log10(len(dlist)/(df[word]*1.0)), 0)
           # print len(dlist), df[word],math.log10(len(dlist)/(df[word]*1.0))
            dlist[filepath][word] = (dlist[filepath][word][0], dlist[filepath][word][1], dlist[filepath][word][0] * dlist[filepath][word][1])
        normalize(dlist[filepath])
        #print dlist[filepath]
    input_file.close()
    return dlist

def normalize(dict):
    sum = 0
    #get the square sum of the  tf-idf
    for term in dict:
        sum = sum + math.pow(dict[term][2], 2.0)
    sum = math.sqrt(sum)
    #normalize the tf-idf
    for term1 in dict:
        dict[term1]= (dict[term1][0], dict[term1][1], dict[term1][2]/(sum*1.0))
        #print dict[term1][2]/(sum*1.0)
def normalizequery(dict):
    sum = 0
    #get the square sum of the  tf-idf
    for term in dict:
        sum = sum + math.pow(dict[term], 2.0)
    sum = math.sqrt(sum)
    #normalize the tf-idf
    for term1 in dict:
        dict[term1]= dict[term1]/(sum*1.0)


def tfquery(query):
    dict = {}
    query = re.sub('[^0-9a-zA-Z]+', ' ', query)
    words = query.split()
    for word in words:
        word = word.lower()
        if len(word) > 2:
            if word in dict:
                dict[word] =dict[word] + 1
            else:
                dict[word] = 1
    normalizequery(dict)
    #print dict
    return dict


@app.route('/foldername, query', methods=['GET','POST'])
def rank(foldername, query):
    dlist = tf(foldername)
    dict = tfquery(query)

    #calcuate cosine score for each doc
    #score: filepath, cosine score
    score = {}
    for filepath in dlist:
        sum = 0
        for word in dict:
            if word in dlist[filepath]:
                sum = sum + dlist[filepath][word][2] * dict[word]
        score[filepath] = sum

    #for file in score:
        #if file == "reviews/cv032_22550.txt": print score[file]
    #output top5 document
    # list=[]
    # items = sorted(score.items(), key = lambda score: score[1], reverse = True)
    # n = 1
    # for item in items[:5]:

    #     list.append( "%(num)s. %(item0)s (score is %(item1)s)" % {"num": n, "item0": item[0], "item1": item[1]})
    #     n += 1
    
    # json_string=json.dumps(list)
    # print 'Json: %s' % json_string
    # new_obj=json.loads(json_string) #convert json to python object
    # print 'obj: ', new_obj
    # return render_template('searchbytags.html', json=json_string, list=new_obj)
    items = sorted(score.items(), key = lambda score: score[1], reverse = True)
    n = 1
    string = ""
    results2=[]
    for item in items[:5]:
        #print "%(num)s. %(item0)s (score is %(item1)s)" % {"num": n, "item0": item[0], "item1": item[1]}
        regex = re.compile('[^a-zA-Z\d\s:]')
        string =  str(n) + ". " + regex.sub('', item[0][48:])+"\n"
        results2.append(string)
        n += 1
    print string
    return render_template('searchbytags.html',results = results2)
#@app.route('/foldername', methods=['GET', 'POST'])
def print_top(foldername):
    dict = tf(foldername)
    items = sorted(dict.items(), key = lambda dict: dict[1], reverse = True)
    n = 1
    for item in items[:5]:
        print "%(num)s. %(item0)s (frequency is %(item1)s)" % {"num": n, "item0": item[0], "item1": item[1]}
        n += 1
    

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    query = text.lower()
    folder = "ratemyprofessorsdata"
    file_paths = []
    filelist = os.listdir(folder)

    for filename in filelist:

        dic_name = folder + '/'
        path_txt= dic_name+ filename
        file_paths.append(path_txt)

    #print file_paths
    return rank(file_paths, query)

    

if __name__ == '__main__':
  app.run(debug=True)