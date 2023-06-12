MODEL = 'gpt-3.5-turbo'
SYSTEM_ROLE = '''Use the provided content delimited by triple quotes to answer questions. If the answer cannot be \
found in the content, write "I could not find an answer."'''

EXAMPLE_CONTENT = \
'''Himpelchen und Pimpelchen stiegen auf einen Berg.
Himpelchen war ein Heinzelmann und
Pimpelchen ein Zwerg.
Sie blieben lange dort oben sitzen
und wackelten mit ihren Zipfelmützen.
Doch nach dreiunddreißig Wochen
sind sie in den Berg gekrochen.
Da schlafen sie in guter Ruh.
Seid mal still und hör gut zu!'''

EXAMPLE_TASK = \
'''Your task is to generate a short summary of the content in 1 sentence. Then come up with a descriptive headline. \
The headline has to be less than 30 characters in length. Structure your output like the following example.

Summary: <your summary goes here>

Headline: <your headline goes here>'''



