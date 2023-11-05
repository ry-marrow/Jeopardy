# import csv

# def process_uploaded_csv(file):
#     try:
#         # Assuming our CSV file has a header row with columns: question, answer1, answer2, answer3, answer4
#         # We may need to adjust this based on our actual CSV format.
#         csv_reader = csv.DictReader(file)
#         for row in csv_reader:
#             question = row['question']
#             answers = [row['answer1'], row['answer2'], row['answer3'], row['answer4']]
            
#             # Here, we can insert the question and answers into our database
#             # For example, we can use SQLAlchemy to add them to the database

#             # Replace the following print statements with our database insertion code
#             print(f'Question: {question}')
#             print(f'Answers: {answers}')

#         return True
#     except Exception as e:
#         print(f'Error processing CSV: {e}')
#         return False

import csv
from . import db
from .models import questions_answers  # Import the questions_answers model from your Flask app
from io import TextIOWrapper

def process_uploaded_csv(file):
    try:
        file = TextIOWrapper(file, encoding='utf-8')
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # These are the csv headings 
            question_text = row['question']
            answer_text = row['answer']
            category = row['category']
            difficulty = int(row['difficulty'])

            new_question_answer = questions_answers(
                questionText=question_text,
                answerText=answer_text,
                category=category,
                difficulty=difficulty,
                # We can set other fields like createDate, deleted, and isDailyDbl as needed
            )
            db.session.add(new_question_answer)

        db.session.commit()
        return True
    except Exception as e:
        print(f'Error processing CSV: {e}')
        return False
