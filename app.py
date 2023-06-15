from dotenv import load_dotenv
import streamlit as st
import json
from datetime import datetime
import os
import openai

from defaults import MODEL, SYSTEM_ROLE, EXAMPLE_CONTENT, EXAMPLE_TASK


def get_completion(prompt, role=SYSTEM_ROLE, model=MODEL, max_tokens=1600, top_p=1.0, stop=None,
                   temperature=0, frequency_penalty=0, presence_penalty=0):
    messages = [{'role': 'system', 'content': role}, {'role': 'user', 'content': prompt}]
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
    return locals(), response.choices[0].message['content']


def load_session(session):
    """function not yet implemented"""
    pass


_ = load_dotenv()  # sets env vars as defined in .env
openai.api_key = os.environ['OPENAI_API_KEY']

if 'session' not in globals():
    session = []

if 'cur_position' not in globals():
    cur_position = -1

st.set_page_config(layout='wide')
# st.markdown('<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>', unsafe_allow_html=True)
st.markdown('<style>button {height: auto;padding-top: 10px !important;padding-bottom: 10px !important;}</style>',
            unsafe_allow_html=True,)

st.title('Prompt Guru')
st.subheader('A tool to iteratively improve your ChatGPT prompt 💬')

col1, col2 = st.columns([2, 1])
col21, col22 = col2.columns([1, 8])

with col22.expander('Prompt upload'):
    pg_prompt = st.file_uploader(label='', type="application/json")
    # parse the file and load session

with col2.expander('Advanced settings'):
    st.write('If your task falls in the category of creative writing you can consider adjusting these values.')
    temperature = st.slider('temperature (0 = kinda deterministic, 2 = as creative as it gets)', 0.0, 2.0, 0.0)
    frequency_penalty = st.slider('frequency_penalty (↑ = don\'t repeat yourself)', 0.0, 2.0, 0.0)
    presence_penalty = st.slider('presence_penalty (↑ = use less common phrases)', 0.0, 2.0, 0.0)

content = col1.text_area('Content:', value=EXAMPLE_CONTENT, height=100)
prompt = col1.text_area('ChatGPT Task:', value=EXAMPLE_TASK, height=200)

if col1.button('Process'):
    cur_request, response = get_completion(f'{prompt} \n\n Content: """{content}"""', role=SYSTEM_ROLE, model=MODEL,
                                           max_tokens=1600, top_p=1.0, stop=None, temperature=temperature,
                                           frequency_penalty=frequency_penalty, presence_penalty=presence_penalty)

    session.append(cur_request)
    cur_position = len(session) - 1  # mockup implementation turn into class eventually
    col1.write(response)

# if col21.button('◀', disabled=True if cur_position < 1 else False, help='previous prompt'):
#     cur_position -= 1
#     load_session(session[cur_position])

if cur_position >= 0:
    json_string = json.dumps(session[cur_position])
    timestamp = datetime.fromtimestamp(session[cur_position]['response']['created']).strftime('%Y%m%dT%H%M%S')
else:
    json_string = '{}'
    timestamp = ''

button_download = col21.download_button(
    label='💾',
    disabled=True if cur_position < 0 else False,
    file_name=f'prompt_guru_{timestamp}.json',
    mime="application/json",
    data=json_string,
    help='download prompt'
)

# if col23.button('▶', disabled=True if cur_position == len(session) - 1 else False, help='next prompt'):
#     cur_position += 1
#     load_session(session[cur_position])

