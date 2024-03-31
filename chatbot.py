import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import string
import warnings
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')
nltk.download('popular', quiet=True)

# Reading in the corpus
with open('C:\\Users\\magdaline suganthi\\Desktop\\New folder (3)\\Building-a-Simple-Chatbot-in-Python-using-NLTK\\chatbot.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

# Tokenization
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Preprocessing
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Generating response
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you"
        # Store user's input in the dataset
        sent_tokens.append(user_response)
        with open('chatbot.txt', 'a', encoding='utf8') as fout:
            fout.write('\n' + user_response)
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response

def send():
    user_response = entry_text.get("1.0", tk.END).strip()
    entry_text.delete("1.0", tk.END)
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_response + "\n", "user")
    user_response = user_response.lower()
    if user_response != 'bye':
        if user_response == 'thanks' or user_response == 'thank you':
            chat_window.insert(tk.END, "Chatbot: You are welcome..\n", "bot")
        else:
            if greeting(user_response) != None:
                chat_window.insert(tk.END, "Chatbot: " + greeting(user_response) + "\n", "bot")
            else:
                chat_window.insert(tk.END, "Chatbot: " + response(user_response) + "\n", "bot")
    else:
        chat_window.insert(tk.END, "Chatbot: Bye! take care..\n", "bot")
    chat_window.config(state=tk.DISABLED)
    chat_window.see(tk.END)  # Automatically scroll to the bottom after each message

root = tk.Tk()
root.title("Chatbot")
root.geometry("600x600")
root.configure(bg="sky blue")

chat_frame = ttk.Frame(root)
chat_frame.pack(pady=10)

chat_window = scrolledtext.ScrolledText(chat_frame, width=60, height=20, wrap=tk.WORD, bg="white", fg="#075E54")
chat_window.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

entry_text = tk.Text(chat_frame, width=50, height=2, wrap=tk.WORD, bg="white", fg="#075E54")
entry_text.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

send_button = tk.Button(chat_frame, text="Send", bg="#C4C4C4", fg="#075E54", font=("Helvetica", 12), command=send)
send_button.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Tag configurations
chat_window.tag_config("user", foreground="blue", font=("Helvetica", 15, "bold"))
chat_window.tag_config("bot", foreground="light blue", font=("Helvetica", 15, "bold"))

root.mainloop()
