import streamlit as st
from huggingface_hub import InferenceClient

from wordgame import WordGame

token = "" #Input your HF token here

if "wordgame" not in st.session_state:
    st.session_state.wordgame = WordGame()

st.title("The Word Game")

#model_name = "unsloth/Llama-3.2-1B-Instruct"
#model_name = "HuggingFaceH4/zephyr-7b-beta"
#model_name = "T3lli/test"
#model_name = "T3lli/test_v2"
#model_name = "DrDomedag/LocoLamav3"
#model_name = "DrDomedag/LocoLamav3M"
#model_name = "DrDomedag/LocoLamav3M4bit"
model_name = "DrDomedag/HumanDialoguev2"

client = InferenceClient(model_name, timeout=300, token=token)

#st.markdown(st.session_state.wordgame.update_status())

# Session state to hold chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# User input
user_input = st.text_input("Type your message here...", key="user_input")

# On submit
if st.button("Send"):
    if user_input.strip():
        # Add user's message to the chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Query the model
        with st.spinner("The robot is thinking..."):
            response = client.text_generation(user_input)
            #assistant_reply = response.get("generated_text", "").strip()
            assistant_reply = response.strip()

        # Add the model's reply to the chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        print(assistant_reply)

        if not st.session_state.wordgame.check_input_for_word(user_input.strip().lower()):
            print("Target word not in user input.")
            check_result = st.session_state.wordgame.check_output_for_word(assistant_reply)
            if "Success!" in check_result:
                st.balloons()
            st.session_state.messages.append({"role": "game", "content": check_result})
        else:
            print("Target word found in user input.")
            st.session_state.messages.append({"role": "game", "content": "You're not allowed to input the target word yourself, that's cheating! You just lost one point!"})
        #st.session_state.messages.append({"role": "game", "content": st.session_state.wordgame.update_status()})


        # Clear the input box
        #st.session_state.user_input = ""

# Display the chat history
for message in reversed(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Robot:** {message['content']}")
    elif message["role"] == "game":
        st.markdown(f"**Game:** {message['content']}")


# Instructions for the user
#st.sidebar.title("Instructions")
#st.sidebar.info(
#    f"Current score: {st.session_state.wordgame.points}"
#)
with st.sidebar:
    st.write(f"Current score: {st.session_state.wordgame.points}")
    st.write(f"Remaining attempts: {st.session_state.wordgame.attempts}")
    st.write(f"Target word: **{st.session_state.wordgame.target_word}**")

    st.info(f'The goal of the game is to make the model say the target word. You are not allowed to input the word yourself. Other than that, input any query and click "Send"! You get three points if you make it in one try, two points if you make it in two, and one point if it takes you three tries. If you do not win in three attempts, you will get zero points and a new target word.')
