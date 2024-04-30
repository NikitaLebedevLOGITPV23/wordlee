import tkinter as tk
import random

with open("sonad.txt", "r") as f:
    words = f.read().splitlines()

letter_boxes = []
attempts = 0
max_attempts = 6
alphabet_buttons = []
alphabet_state = {}
target_word = None
word_length = 0
current_index = 0  

def create_new_row():
    global letter_boxes, attempts, target_word, word_length, alphabet_buttons, alphabet_state, current_index
    for entry in letter_boxes:
        entry.destroy()
    
    for btn in alphabet_buttons:
        btn.config(bg="lightgrey", fg="black")
    
    alphabet_state = {chr(i): 'unused' for i in range(97, 123)}
    target_word = random.choice(words).lower()
    attempts = 0
    word_length = len(target_word)

    letter_boxes = [tk.Entry(window, width=3, font=("Arial", 24), justify="center") for _ in range(word_length)]
    for i, entry in enumerate(letter_boxes):
        entry.pack(side="left")
        entry.bind("<KeyRelease>", lambda e, i=i: navigate_text_boxes(e, i))
        entry.bind("<KeyPress>", limit_input)

    current_index = 0
    letter_boxes[current_index].focus_set()

def limit_input(event):
    text = event.widget.get()
    if len(text) > 1:
        event.widget.delete(1, tk.END)

def navigate_text_boxes(event, index):
    global current_index 
    if event.keysym == "BackSpace":
        if index > 0:
            current_index = index - 1
            letter_boxes[current_index].focus_set()
            letter_boxes[current_index].delete(0, tk.END)
    elif event.keysym not in ["BackSpace", "Shift", "Control", "Alt"]:
        if index < word_length - 1 and event.widget.get():
            current_index = index + 1
            letter_boxes[current_index].focus_set()

def add_letter_to_box(letter):
    global current_index
    letter_boxes[current_index].delete(0, tk.END)
    letter_boxes[current_index].insert(0, letter)
    
    if current_index < word_length - 1:
        current_index += 1
        letter_boxes[current_index].focus_set()

def check_word():
    global attempts, target_word
    if attempts >= max_attempts:
        return
    
    entered_word = "".join([entry.get() for entry in letter_boxes]).lower()
    
    if len(entered_word) != word_length:
        result_label.config(text="Mittetäielik sõna, proovige uuesti.", bg="grey", fg="black")
        return
    
    correct_count = 0
    for i in range(word_length):
        if entered_word[i] == target_word[i]:
            letter_boxes[i].config(bg="green", fg="white")
            correct_count += 1
        elif entered_word[i] in target_word:
            letter_boxes[i].config(bg="yellow", fg="black")
        else:
            letter_boxes[i].config(bg="grey", fg="white")
    
    update_alphabet(entered_word)
    
    attempts += 1  
    
    if entered_word == target_word:
        result_label.config(text="Sa võitsid!", bg="green", fg="white")
        check_button.config(state="disabled")
        return
    
    if attempts >= max_attempts:
        result_label.config(text=f"Sa kaotasid! Õige sõna oli: {target_word}", bg="red", fg="white")
        check_button.config(state="disabled")
    else:
        result_label.config(text=f"Teil on {max_attempts - attempts} katsed vasakule.", bg="grey", fg="black")

def update_alphabet(entered_word):
    global alphabet_state, target_word
    for i, letter in enumerate(entered_word):
        if letter == target_word[i]:
            alphabet_state[letter] = 'correct'
        elif letter in target_word:
            alphabet_state[letter] = 'in_word'
        else:
            alphabet_state[letter] = 'not_in_word'
    
    for btn in alphabet_buttons:
        letter = btn.cget("text")
        if letter in alphabet_state:
            state = alphabet_state[letter]
            if state == 'correct':
                btn.config(bg="green", fg="white")
            elif state == 'in_word':
                btn.config(bg="yellow", fg="black")
            elif state == 'not_in_word':
                btn.config(bg="grey", fg="white")

def start_new_game():
    create_new_row()
    check_button.config(state="normal")
    result_label.config(text="Alustage arvamist.", bg="grey", fg="black")

window = tk.Tk()
window.title("Wordle")
window.configure(bg="grey")

centered_label = tk.Label(window, text="Arva ära sõna", font=("Arial", 18), bg="grey")
centered_label.pack(expand=True, pady=10)

new_game_button = tk.Button(window, text="Alusta uut mängu", font="Arial 10", bg="#4a4a4a", command=start_new_game)
new_game_button.pack(pady=10)

check_button = tk.Button(window, text="Check", font="Arial 10", bg="#4a4a4a", command=check_word)
check_button.pack(pady=10)

result_label = tk.Label(window, text="", bg="grey", font=("Arial", 18))
result_label.pack(pady=10)

alphabet_frame = tk.Frame(window, bg="grey")
alphabet_frame.pack(pady=10)

alphabet_buttons = []
for i in range(26):
    letter = chr(97 + i) 
    btn = tk.Button(alphabet_frame, text=letter, font=("Arial", 12), width=2, bg="lightgrey", fg="black")
    btn.config(command=lambda l=letter: add_letter_to_box(l)) 
    alphabet_buttons.append(btn)
    btn.pack(side="left", padx=2)

start_new_game()

window.mainloop()

