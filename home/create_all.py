from django.db import connections
from collections import namedtuple
import json

class CreateForm:
    def __init__(self, request):
        self.name = json.loads(request.body)['name']
        self.date_start = json.loads(request.body)['date_start']
        self.date_end = json.loads(request.body)['date_end']
        self.description = json.loads(request.body)['description']
        self.questions_and_choices = json.loads(request.body)['questions_and_choices']
        
        
    def forms(self):
        name = self.name
        date_start = self.date_start
        date_end = self.date_end
        description = self.description
        questions_and_choices = self.questions_and_choices


        if date_start == "":
            date_start = "NULL"
        else:
            date_start = "'" + self.date_start + "'"
        
        if date_end == "":
            date_end = "NULL"
        else:
            date_end = "'" + self.date_end + "'"
            
        if description == "":
            description = "NULL"
        else:
            description = "'" + self.description + "'"


        questions = []
        choices = []
        question_type_id = []
        for i in questions_and_choices:
            questions.append(i['question'])
            choices.append(i['choices'])
            if not choices[-1]:
                question_type_id.append(2)
            else:
                question_type_id.append(1)        
        
        
        values = ""
        for i in range(len(questions)):
            values += "(" + str(question_type_id[i]) + ", '" + str(questions[i]) + "', ARRAY" 
            if not choices[i]:
                values += "[NULL]"
            else:
                values += str(choices[i])
            values += ")"
            if i != (len(questions)-1):
                values += ","

         
        queryTxt = '''
                    WITH inserted_form AS (
                        INSERT INTO form 
                            (name, gen_date, date_start, date_end, description)
                        VALUES 
                            ('%s', NOW(), %s, %s, %s)
                        RETURNING 
                            id
                    ), inserted_questions AS (
                        INSERT INTO question 
                            (form_id, question_type_id, question, choices)
                        SELECT 
                            id, q.question_type_id, q.question, q.choices
                        FROM 
                            inserted_form, (
                                VALUES 
                                    %s
                        ) AS q(question_type_id, question, choices)
                        RETURNING 
                            id AS question_id, choices
                    ), inserted_choices AS (
                        INSERT INTO choice 
                            (question_id, choice)
                        SELECT 
                            question_id, choice
                        FROM inserted_questions, 
                            LATERAL unnest(choices) AS choice
                        RETURNING 
                            id AS choice_id
                    )
                    SELECT *
                    FROM inserted_choices;
                   '''% (name, date_start, date_end, description, values)
        
        print(queryTxt)           
        conn = connections['default']
        cursor = conn.cursor()
        cursor.execute(queryTxt)
        cursor.close()
        conn.close()
 