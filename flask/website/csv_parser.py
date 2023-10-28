import csv

def process_uploaded_csv(file):
    try:
        # Assuming our CSV file has a header row with columns: question, answer1, answer2, answer3, answer4
        # We may need to adjust this based on our actual CSV format.
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            question = row['question']
            answers = [row['answer1'], row['answer2'], row['answer3'], row['answer4']]
            
            # Here, we can insert the question and answers into our database
            # For example, we can use SQLAlchemy to add them to the database

            # Replace the following print statements with our database insertion code
            print(f'Question: {question}')
            print(f'Answers: {answers}')

        return True
    except Exception as e:
        print(f'Error processing CSV: {e}')
        return False
