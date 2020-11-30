from flask import Flask, request, render_template, jsonify
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
@app.route('/category', methods =["GET", "POST"])
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
@app.route('/quizz', methods=["GET", "POST"])
def getQA():
    #query
    def queryQues(categoryId):
        select = "SELECT * FROM question WHERE categoryId =" + str(categoryId)
        cursor = conn.cursor()
        cursor.execute(select)
        result = cursor.fetchall()
        return result

    def queryAns(questionId):
        select = "SELECT * FROM answer WHERE questionId =" + str(questionId)
        cursor = conn.cursor()
        cursor.execute(select)
        result = cursor.fetchall()
        return result

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


if __name__ == '__main__':
   app.run(port=port, debug=True)