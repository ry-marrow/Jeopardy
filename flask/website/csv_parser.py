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
