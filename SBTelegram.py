import tkinter as tk
from tkinter import ttk
from tkinter import*
from tkinter import messagebox
import keyboard

def get_letter():
    current = []
    while len(current) < 3:
        event = keyboard.read_event()
        if event.event_type == "down":
            current.append(event.name)
    return current

if __name__ == "__main__":
    string = []
    while True:
        current_letter = get_letter()
        if current_letter[0] == 'up' and current_letter[1] == 'up' and current_letter[2] == 'up':
            break
        elif current_letter[0] == 'down' and current_letter[1] == 'down' and current_letter[2] == 'down':
            string.append(' ')
            print(' ', end='')
        elif current_letter[0] == 'right' and current_letter[1] == 'right' and current_letter[2] == 'right':
            string.append('a')
            print('a', end='')
        elif current_letter[0] == 'right' and current_letter[1] == 'right' and current_letter[2] == 'left':
            string.append('b')
            print('b', end='')
        elif current_letter[0] == 'right' and current_letter[1] == 'left' and current_letter[2] == 'right':
            string.append('c')
            print('c', end='')
        elif current_letter[0] == 'left' and current_letter[1] == 'right' and current_letter[2] == 'right':
            string.append('d')
            print('d', end='')
        elif current_letter[0] == 'left' and current_letter[1] == 'left' and current_letter[2] == 'right':
            string.append('e')
            print('e', end='')
        elif current_letter[0] == 'left' and current_letter[1] == 'left' and current_letter[2] == 'left':
            string.append('f')
            print('f', end='')
        elif current_letter[0] == 'right' and current_letter[1] == 'left' and current_letter[2] == 'left':
            string.append('g')
            print('g', end='')
        elif current_letter[0] == 'left' and current_letter[1] == 'right' and current_letter[2] == 'left':
            string.append('h')
            print('h', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'down' and current_letter[2] == 'up':
            string.append('i')
            print('i', end='')
        elif current_letter[0] == 'down' and current_letter[1] == 'up' and current_letter[2] == 'down':
            string.append('j')
            print('j', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'up' and current_letter[2] == 'down':
            string.append('k')
            print('k', end='')
        elif current_letter[0] == 'down' and current_letter[1] == 'down' and current_letter[2] == 'up':
            string.append('l')
            print('l', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'down' and current_letter[2] == 'down':
            string.append('m')
            print('m', end='')
        elif current_letter[0] == 'down' and current_letter[1] == 'up' and current_letter[2] == 'up':
            string.append('n')
            print('n', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'up' and current_letter[2] == 'right':
            string.append('o')
            print('o', end='')
        elif current_letter[0] == 'down' and current_letter[1] == 'down' and current_letter[2] == 'right':
            string.append('p')
            print('p', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'down' and current_letter[2] == 'left':
            string.append('q')
            print('q', end='')
        elif current_letter[0] == 'down' and current_letter[1] == 'up' and current_letter[2] == 'right':
            string.append('r')
            print('r', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'left' and current_letter[2] == 'down':
            string.append('s')
            print('s', end='')
        elif current_letter[0] == 'down' and current_letter[1] == 'right' and current_letter[2] == 'up':
            string.append('t')
            print('t', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'left' and current_letter[2] == 'left':
            string.append('u')
            print('u', end='')
        elif current_letter[0] == 'left' and current_letter[1] == 'up' and current_letter[2] == 'up':
            string.append('v')
            print('v', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'right' and current_letter[2] == 'right':
            string.append('w')
            print('w', end='')
        elif current_letter[0] == 'right' and current_letter[1] == 'up' and current_letter[2] == 'up':
            string.append('x')
            print('x', end='')
        elif current_letter[0] == 'up' and current_letter[1] == 'right' and current_letter[2] == 'left':
            string.append('y')
            print('y', end='')
        elif current_letter[0] == 'left' and current_letter[1] == 'up' and current_letter[2] == 'down':
            string.append('z')
            print('z', end='')

mainloop()
