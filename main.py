from flask import Flask, request, render_template, jsonify
from flask_cors import cross_origin
from flask_restful import Resource, Api
import mysql.connector
import os

app = Flask(__name__)
api = Api(app)
port = int(os.environ.get('PORT', 5000))

conn = mysql.connector.connect(user='root', password='ducmin248', host='localhost', database='quizz')

if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")


# API 1
@app.route('/api/v1/category', methods =["GET", "POST"])
@cross_origin()
def queryCate():
    #query
    def queryCate():
        select = "SELECT * FROM category"
        cursor = conn.cursor()
        cursor.execute(select)
        r = cursor.fetchall()
        return r

    result = []
    data = queryCate()
    for row in data:
        mydict = dict()
        mydict["categoryId"] = row[0]
        mydict["category"] = row[1]
        result.append(mydict)
    return jsonify(result)


# API 2
@app.route('/api/v1/quizz', methods=["GET", "POST"])
@cross_origin()
def getQA():
    #query
    def queryQues(categoryId):
        select = "SELECT * FROM question WHERE categoryId =" + str(categoryId) +\
                 " ORDER BY RAND() LIMIT 10"
        cursor = conn.cursor()
        cursor.execute(select)
        r = cursor.fetchall()
        return r

    def queryAns(questionId):
        select = "SELECT * FROM answer WHERE questionId =" + str(questionId)
        cursor = conn.cursor()
        cursor.execute(select)
        r = cursor.fetchall()
        return r

    categoryId = request.args.get("categoryId")

    result = []

    data = queryQues(categoryId)
    for row in data:
        mydict = dict()
        mydict["questionId"] = row[0]
        mydict["question"] = row[1]
        mydict["answers"] = []

        # get answers
        answers = queryAns(mydict["questionId"])

        for a in answers:
            mydict["answers"].append(a[1])

        result.append(mydict)
    return jsonify(result)


# API 3
@app.route('/api/v1/quizz/check', methods=["POST"])
@cross_origin()
def json_example():
    # query
    def checkAns(questionId, submittedAnswer):
        select = "SELECT a.* FROM answer a " \
                 " WHERE a.questionId =" + str(questionId) +\
                 " AND a.answer = '"+str(submittedAnswer)+"'" +\
                 " AND correct = 1" \
                 " LIMIT 1;"
        cursor = conn.cursor()
        cursor.execute(select)
        r = cursor.fetchall()
        return r

    def getQuestionCorrectAns(questionId):
        select = "SELECT q.question, a.answer FROM answer a " \
                 " INNER JOIN question q ON q.questionId = a.questionId" \
                 " WHERE q.questionId =" + str(questionId) + \
                 " AND correct = 1" \
                 " LIMIT 1;"
        cursor = conn.cursor()
        cursor.execute(select)
        r = cursor.fetchall()
        return r

    data = request.get_json(force=True)

    result = []

    for d in data:
        questionId = d['questionId']
        submittedAnswer = d['submittedAnswer']

        incorectQuestion = checkAns(questionId, submittedAnswer)
        if incorectQuestion:
            print("xxxxxxxxxxxxxxxxxxx")
            questionAndCorrectAnswer = getQuestionCorrectAns(questionId)
            result.append({
                "question": questionAndCorrectAnswer[0][0],
                "correctAnswer": questionAndCorrectAnswer[0][1]
            })

    print(result)
    return jsonify(result)

# phuc oc cho

if __name__ == '__main__':
   app.run(port=port, debug=True)
