from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import random
import datetime
import json


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
WORDS_RANGE = 'Words!A2:G'

class Word:
  def __init__(self, english, italian, row_num, correct_count = 0, tested_count = 0, last_test = ''):
    self.english = english
    self.italian = italian 
    self.row_num = row_num
    self.correct_count = correct_count
    self.tested_count = tested_count 
    self.last_test = last_test

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
        start_quizzing_randomly(service, sheet_id, words)

    except HttpError as err:
        print(err)

def start_quizzing_randomly(service, sheet_id, words):
    while True: 
        word = random.choice(words)
        user_answer = input(f'{word.english}: ')
        if (user_answer == word.italian):
            print("You got it!")
            word.correct_count+=1
        else:
            print("You might have missed it...")
            print(f"Expected, Input: {word.italian}, {user_answer}")
            is_correct = input("Verify correct or no (y/n)")
            if is_correct == 'y':
                print("Mi dispiace! Recording as correct.")
                word.correct_count+=1
            else:
                print("You'll get it next time!")
        word.tested_count+=1
        word.last_test = datetime.date.today().strftime('%-m/%-d/%y')
        update_word_stats(service, sheet_id, word)
        continue

def parse_row_to_word(row, row_num): 
    word = Word(english = row[1], italian = row[0], row_num = row_num)
    try:
        word.tested_count = int(row[3])
    except: 
        print("Row doesn't have tested_count column")
    try: 
        word.correct_count = int(row[4])
    except: 
        print("Row doesn't have correct_count column")
    try: 
        word.last_test = row[6]
    except:
        print("Row doesn't have last_test column")
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
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
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


if __name__ == '__main__':
    main()
