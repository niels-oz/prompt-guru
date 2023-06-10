from dotenv import load_dotenv
import streamlit as st
import os
import openai

from defaults import MODEL, SYSTEM_ROLE, EXAMPLE_CONTENT, EXAMPLE_TASK


def get_completion(prompt, role=SYSTEM_ROLE, model=MODEL, temperature=0, max_tokens=1600,  # TODO: calc max. tokens
                   top_p=1.0, frequency_penalty=0, presence_penalty=0, stop=None):
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

    st.set_page_config(layout='wide')

    st.title('Prompt Guru')
    st.subheader('A tool to iteratively improve your Chat GPT prompt 💬')

    col1, col2 = st.columns([2,1])

    content = col1.text_area('Content:', value=EXAMPLE_CONTENT, height=100)
    prompt = col1.text_area('Chat GPT Task:', value=EXAMPLE_TASK, height=200)

    with col2.expander('Advanced settings'):
        st.write('If your task falls in the category of creative writing you can consider adjusting these values.')
        temperature = st.slider('temperature (0 = kinda deterministic, 2 = as creative as it gets)', 0.0, 2.0, 0.0)
        frequency_penalty = st.slider('frequency_penalty (↑ = don\'t repeat yourself)', 0.0, 2.0, 0.0)
        presence_penalty = st.slider('presence_penalty (↑ = use less common phrases)', 0.0, 2.0, 0.0)

    if col1.button('Process'):
        response = get_completion(f'{prompt} \n \n Content: """{content}"""', temperature=temperature,
                                  frequency_penalty=frequency_penalty, presence_penalty=presence_penalty)
        col1.write(response)


if __name__ == '__main__':
    main()
