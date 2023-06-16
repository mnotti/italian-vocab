from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import random
from datetime import datetime
import json

from max_heap import MaxHeap


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
WORDS_RANGE = 'Words!A2:G'
WORDS_BEFORE_RETESTING_RANDOM = 3

class Word:
  def __init__(self, english, italian, row_num, correct_count = 0, tested_count = 0, last_test = ''):
    self.english = english
    self.italian = italian 
    self.row_num = row_num
    self.correct_count = correct_count
    self.tested_count = tested_count 
    self.last_test = last_test

  def get_priority(self):
    priority = 0
    if self.last_test == '': # Accounts for if not tested
        priority += 200
    else:
        priority += days_since_date_str(self.last_test)
    if self.tested_count > 0:
        percentage_incorrect = (self.tested_count - self.correct_count) / self.tested_count
        priority += int(percentage_incorrect * 100) # Accounts for correct:incorrect ratio
    priority += (100 - self.tested_count) # Accounts for total times tested
    return priority

  # For debugging
  def __str__(self):
    return f"[{self.row_num}] {self.english}:{self.italian}, ({self.correct_count}/{self.tested_count}), last attempt: {self.last_test}"

def main():
    # Load config
    with open('config.json') as f:
        config = json.load(f)
        sheet_id = config['sheet_id']
    
    # Authenticate with Gsheets
    creds = authenticate()

    try:
        # Load words into mem 
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=WORDS_RANGE).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return

        # Parse words and start quizzing
        words = parse_rows_to_words(values)
        pq = construct_priority_queue(words)
        start_quizzing(service, sheet_id, pq)

    except HttpError as err:
        print(err)

def start_quizzing(service, sheet_id, pq):
    session_words = [] #Words tested this session
    word_num = 1
    while True:
        word = None
        if word_num % WORDS_BEFORE_RETESTING_RANDOM == 0: 
            word = get_random_word(session_words)
        else:
            word = pq.extract_max()
        old_priority = word.get_priority()
        user_answer = input(f'{word.english}: ')
        correct = False
        if (user_answer == word.italian):
            print("Bravo!")
            correct = True
        else:
            print("Penso che hai sbagliato... ")
            print(f"Hai detto: {user_answer}, Previsto: {word.italian}")
            is_correct = input("Coretto o no? (s/n): ")
            if is_correct == 's':
                print("Che sollievo! Mi dispiace... sto registrando come coretto.")
                correct = True
            else:
                print("Farai meglio la prossima volta!")
        word.tested_count+=1
        word.last_test = datetime.today().date().strftime('%-m/%-d/%y')
        if correct:
            word.correct_count+=1
        update_word_stats(service, sheet_id, word)
        new_priority = word.get_priority()
        print(f'{old_priority}->{new_priority}')
        word_num+=1
        session_words.append(word)
        #pq.insert(word, new_priority)
        continue

def get_random_word(words):
    return random.choice(words)

def construct_priority_queue(words): 
    pq = MaxHeap()
    for word in words:
        priority = word.get_priority()
        pq.insert(word, priority)
    return pq

def parse_row_to_word(row, row_num): 
    word = Word(english = row[1], italian = row[0], row_num = row_num)
    try:
        word.tested_count = int(row[3])
    except: 
        pass
    try: 
        word.correct_count = int(row[4])
    except: 
       pass
    try: 
        word.last_test = row[6]
    except:
        pass
    return word

def parse_rows_to_words(rows): 
    words = []
    for idx, row in enumerate(rows): 
        if len(row) >= 2:
            word = parse_row_to_word(row, idx+2)
            words.append(word)
    return words

def update_word_stats(service, sheet_id, word):
    range = f'D{word.row_num}:G{word.row_num}'
    value_obj = {
        'values': [
            [word.tested_count, word.correct_count, f'=E{word.row_num}/D{word.row_num}', word.last_test]
        ]
    }
    service.spreadsheets().values().update(spreadsheetId=sheet_id, range=range, valueInputOption='USER_ENTERED', body=value_obj).execute()

def authenticate(): 
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Takes string in format 'MM/DD/YY'
def days_since_date_str(date_str):
    return (datetime.today().date() - datetime.strptime(date_str, '%m/%d/%y').date()).days

if __name__ == '__main__':
    main()
