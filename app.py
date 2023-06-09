from dotenv import load_dotenv
import streamlit as st
import os
import openai


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
The headline has to be less than 30 characters in length. 

Structure your output like the following example.

Summary: <your summary goes here>

Headline: <your headline goes here>'''

SYSTEM_ROLE = '''Use the provided content delimited by triple quotes to answer questions. If the answer cannot be \
found in the content, write "I could not find an answer."'''

MODEL = 'gpt-3.5-turbo'


def get_completion(prompt, role=SYSTEM_ROLE, model=MODEL, temperature=0, max_tokens=1600, top_p=.95,
                   frequency_penalty=0, presence_penalty=0, stop=None):
    messages = [{'role': 'system', 'content': role},{'role': 'user', 'content': prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
    print(response)
    return response.choices[0].message['content']


def main():
    _ = load_dotenv()  # sets env vars as defined in .env
    openai.api_key = os.environ['OPENAI_API_KEY']

    st.title('Prompt Guru')
    st.header('A tool to improve your Chat GPT prompt 💬')

    content = st.text_area('Content:', value=EXAMPLE_CONTENT, height=200)
    prompt = st.text_area('Chat GPT Task:', value=EXAMPLE_TASK, height=200)

    if st.button('Process'):
        response = get_completion(f'{prompt} \n \n Content: """{content}"""')
        st.write(response)

    settings = st.json({'role': SYSTEM_ROLE, 'model': MODEL, 'temperature': 0.0, 'max_tokens': 1600, 'top_p': 0.95,
                        'frequency_penalty': 0, 'presence_penalty': 0, 'stop': None})


if __name__ == '__main__':
    main()
