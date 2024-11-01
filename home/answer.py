from django.db import connections
from collections import namedtuple
import json

def fetchAllData(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

class Answer:
    def __init__(self, request):
        self.formID = json.loads(request.body)['formID']
        self.answers = json.loads(request.body)['answers']
        
        
    def answer(self):
        formID = self.formID
        answers = self.answers
        questionID = []
        answer = []
        
        for i in answers:
            questionID.append(i)
            answer.append(answers[i])
            
        values = ""
        for i in range(len(questionID)):
            values += "(" + str(formID) + "," + str(questionID[i]) + ", '" + str(answer[i]) + "' , NOW())"
            if i != len(questionID)-1:
                values += ","
            else:
                values += ";"

        
        queryTxt = '''
                    INSERT INTO answer 
                        (form_id, question_id, answer, response_time)
                    VALUES 
                         %s
                    ''' % (values)
        
        print(queryTxt)           
        conn = connections['default']
        cursor = conn.cursor()
        cursor.execute(queryTxt)
        cursor.close()
        conn.close()
        
        
        
class ShowAnswer:
    def __init__(self, request):
        self.formID = request.POST.get('formID')
        
    def show_answer(self):
        formID = self.formID
        
        queryTxt = '''
                    SELECT
                        f.name AS name,
                        qt."name" AS type,
                        q.question AS question,
                        a.answer AS answer,
                        CASE WHEN q.question_type_id = 1 THEN COUNT(*) ELSE NULL END AS count
                    FROM
                        form f
                    LEFT JOIN
                        question q ON q.form_id = f.id
                    LEFT JOIN
                        answer a ON a.question_id = q.id
                    left join 
                        question_type qt on qt.id = q.question_type_id 
                    WHERE
                        f.id = %s
                    GROUP BY
                        f.name,
                        q.id,
                        qt."name",
                        q.question,
                        a.answer,
                        a.question_id,
                        q.question_type_id
                    HAVING
                        COUNT(*) > 0
                    ORDER BY
                        q.id ASC;
                    ''' % (formID)
        
        print(queryTxt)           
        conn = connections['default']
        cursor = conn.cursor()
        cursor.execute(queryTxt)
        result = fetchAllData(cursor)
        cursor.close()
        conn.close()
        
        tmpinDatas = []
        for data in result:
            tmpinDatas.append({
                'name': data[0],
                'type': data[1],
                'question': data[2],
                'answer': data[3],
                'count': data[4],
            })
            
        # print(tmpinDatas)
        return (tmpinDatas)
        