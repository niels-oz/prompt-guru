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


# sets env vars as defined in .env
_ = load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

# Initializing session state variables
if 'prompts' not in st.session_state:  # prompts are a list of dict containing content, prompt, and settings
    st.session_state['prompts'] = []  # initialise list of prompts of current session

if 'cur_position' not in st.session_state:
    st.session_state['cur_position'] = -1  # a pointer to mark the current prompt


st.set_page_config(layout='wide')
# st.markdown('<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>', unsafe_allow_html=True)
st.markdown('<style>button {height: auto;padding-top: 10px !important;padding-bottom: 10px !important;}</style>',
            unsafe_allow_html=True,)

st.title('Prompt Guru')
st.subheader('A tool to iteratively improve your ChatGPT prompt 💬')

col1, col2 = st.columns([5, 3])
col21, col22, col23, col24 = col2.columns([1, 1, 1, 7])

with col24.expander('Prompt upload'):
    pg_prompt = st.file_uploader(label='Prompt upload', label_visibility=False, type="application/json")
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

    st.session_state['prompts'].append(cur_request)  # 1st iteration turn into class eventually
    st.session_state['cur_position'] = len(st.session_state['prompts']) - 1  # push the val to local var
    col1.write(response)

if col21.button('◀', disabled=True if st.session_state['cur_position'] < 1 else False, help='previous prompt'):
    st.session_state['cur_position'] -= 1
    load_session(st.session_state['prompts'][st.session_state['cur_position']])

if st.session_state['cur_position'] >= 0:
    json_string = json.dumps(st.session_state['prompts'][st.session_state['cur_position']])
    timestamp = datetime.fromtimestamp(st.session_state['prompts'][st.session_state['cur_position']]\
        ['response']['created']).strftime('%Y%m%dT%H%M%S')
else:
    json_string = '{}'
    timestamp = ''

button_download = col22.download_button(
    label='💾',
    disabled=True if st.session_state['cur_position'] < 0 else False,
    file_name=f'prompt_guru_{timestamp}.json',
    mime="application/json",
    data=json_string,
    help='download prompt'
)

if col23.button('▶', disabled=True if st.session_state['cur_position'] == len(st.session_state['prompts']) - 1 \
        else False, help='next prompt'):
    st.session_state['cur_position'] += 1
    load_session(st.session_state['prompts'][st.session_state['cur_position']])

