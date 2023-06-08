Just a little script for my Italian Learning... probably won't be very helpful for anyone reading this!

## Premise 
 
I learn Italian vocab by appending new words that I come across to a google sheet. 
I sort the sheet by lesson, homework, article etc. and have a column for writing sentences.
I also have columns to track when I've tested my knowledge on specific words and how well I've done.

I was manually quizzing myself by copying chunks of words at a time from one sheet to another, writing down the translation in the adjacent cell, then copying that column back over to check it against the correct answers. 

This was tedious. 
I could do better!

So I made this script to pull the words I have in the sheet and quiz me in the terminal!
Then, correct or not, it updates the stats in the sheet so I know how I've done on particular words and I can see which ones I've nailed down and which ones I need to spend more time on. 

## Sheet Format
Row 1 - headers (ignored in script)
Row 2:infinity - words data
Columns: italian | english | sentence | tested_count | correct_count | =correct_count/tested_count | last_tested_date

## Setup

I have gitignored 
> config.json (w/ "sheet_id" key)
> credentials.json (w/ "google sheets credentials")
> venv things
>> pyvenv.cfg
>> bin
>> lib
>> include

Set up venv

Make sure to pip install the google api things

## Run 
`python quiz.py`

1. Write translation in italian for english
2. Answer y/n as prompted
3. Let your knowledge grow like a blossom in the spring
