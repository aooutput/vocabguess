import streamlit as st

st.set_page_config(page_title='word guess')

# Initialize session state variables if they don't exist
if 'target_word' not in st.session_state:
    st.session_state.target_word = ''
if 'max_guesses' not in st.session_state:
    st.session_state.max_guesses = 6
if 'guesses' not in st.session_state:
    st.session_state.guesses = []
if 'game_active' not in st.session_state:
    st.session_state.game_active = False

st.subheader("Alphabetical Word Guessing 🤔🔤")

# Load word list from local file
@st.cache_data
def load_word_list(filepath):
    words = []
    with open(filepath, "r") as f:
        for line in f:
            # Take the first token (word) and convert to lowercase
            word = line.split()[0].lower()
            words.append(word)
    return set(words)  # Use a set for fast lookup

# Load the word list
vocab = load_word_list("NSWL2023.txt")

# Show settings only if game hasn't started
if not st.session_state.get("game_active", False):
    with st.expander("Game Settings"):
        new_word = st.text_input("Enter a valid word (2-12 letters), ex. scout:", key="word_input")
        new_max_guesses = st.number_input("Maximum number of guesses:", min_value=1, max_value=99, value=15)
        new_word=new_word.strip()
        if st.button("Start New Game"):
            if 2 <= len(new_word) <= 12 and new_word.isalpha() and new_word.lower() in vocab:
                st.session_state.target_word = new_word.lower()
                st.session_state.max_guesses = new_max_guesses
                st.session_state.guesses = []
                st.session_state.game_active = True
                st.rerun()  # <-- Forces immediate rerun so settings disappear
            else:
                st.error("Please enter a valid word between 2 and 12 letters.")

# Game interface
if st.session_state.get("game_active", False):
    st.write("Game started! Make your guesses below:")
    # Your game logic here
    # Display number of remaining guesses
    remaining_guesses = st.session_state.max_guesses - len(st.session_state.guesses)
    st.write(f"Remaining guesses: {remaining_guesses}")
    
    # Input for guesses
    guess = st.text_input("Enter your guess:", key="guess_input")
    if guess:
        guess = guess.lower().strip()
        if guess.lower() in vocab:
                    
            if st.button("Submit Guess"):
                if guess.lower() == st.session_state.target_word:
                    st.success("Congratulations! You've won!")
                    st.session_state.game_active = False
                elif len(st.session_state.guesses) >= st.session_state.max_guesses - 1:
                    st.error(f"Game Over! The word was: {st.session_state.target_word}")
                    st.session_state.game_active = False
                else:
                    st.session_state.guesses.append(guess)
                    st.info("Try again!")
        else:
            st.warning("Not a valid word.")

    
    # Display previous guesses
    # if st.session_state.guesses:
    #     st.write("Previous guesses:", ", ".join(st.session_state.guesses))
    # Display previous guesses alphabetically and show where target word would be
    if st.session_state.guesses:
        sorted_guesses = sorted(st.session_state.guesses)
        
        # Find where target_word would fit in the sorted list
        target_position = 0
        for guess in sorted_guesses:
            if guess < st.session_state.target_word:
                target_position += 1
            else:
                break
        
        # Insert anonymized placeholder
        display_list = sorted_guesses.copy()
        display_list.insert(target_position, "**:rainbow[>ANSWER<]**")
        st.write("Previous guesses (alphabetical):")
        st.write(" :blue[(A.....)]   ")
        st.write(" , ".join(display_list))
        st.write(" :blue[(.....Z)]   ")
else:

    st.write("Set up a new game in the settings above!")



