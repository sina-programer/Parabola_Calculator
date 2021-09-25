from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import webbrowser
import os

class Input:
    __errors = {'empty':'Empty', 'int':'Not integer'}
    def __init__(self, master, x, y, txt, width=15):
        self.access = False
        self.__x = x
        self.__y = y
        
        self.__variable = StringVar()
        self.__variable.trace('w', lambda *args: self.check())
        
        self.__label = Label(master, text=txt)
        self.__label.place(x=self.__x, y=self.__y)

        self.__entry = Entry(master, width=width, bd=2, textvariable=self.__variable)
        self.__entry.place(x=self.__x+20, y=self.__y+2)
        self.__entry.bind('<Enter>', self.__hover)
        self.__entry.bind('<Leave>', self.__leave)

        self.__state = Label(master)
        self.__state.place(x=self.__x+125, y=self.__y)    
        
    def check(self):
        value = self.__variable.get()
        
        if not value.strip():
            self.__state.config(text=self.__errors['empty'], fg='red')
            self.access = False
            
        else:
            try:
                value = eval(value)
                assert isinstance(value, int) or isinstance(value, float)
                self.insert(value)
                self.__state.config(text='Ok', fg='green')
                self.access = True
                
            except:
                self.__state.config(text=self.__errors['int'], fg='red')
                self.access = False
        
    def __hover(self, event):
        self.__entry.config(bd=4)
        self.__entry.place(x=self.__x+20, y=self.__y)
        self.__label.config(width=3)
        
    def __leave(self, event):
        self.__entry.config(bd=2)
        self.__entry.place(x=self.__x+20, y=self.__y+2)
        self.__label.config(width=2)
        
    def get(self):
        return self.__variable.get()
                
    def insert(self, txt):
        self.__variable.set(txt)
        
    def clear(self):
        self.__variable.set('')

class Btn:
    __h_color = '#DBDBDB'
    __l_color = '#F0F0F0'
    def __init__(self, master, text, width, x, y, func, state='normal'):
        self.__state = state
        
        self.__btn = Button(master, text=text, width=width, bd=2, state=self.__state, command=func)
        self.__btn.place(x=x, y=y)
        self.__btn.bind('<Enter>', self.__hover)
        self.__btn.bind('<Leave>', self.__leave)  
        
    def change_state(self, state):
        self.__state = state
        self.__btn.config(state=self.__state)
        
    def __hover(self, event):
        if self.__state != 'disabled':
            self.__btn.config(bg=self.__h_color)
    
    def __leave(self, event):
        self.__btn.config(bg=self.__l_color)

              
class App:
    def __init__(self, master):
        master.config(menu=self.init_menu(master)) 
        master.bind('<Return>', lambda _: self.submit())
        master.bind('<Escape>', lambda _: self.clear())
        
        self.formula = None
        self.steps = ' You have not been active yet '
        self.a = Input(master, 16, 20, 'a :')
        self.b = Input(master, 16, 60, 'b :')
        self.c = Input(master, 16, 100, 'c :')
        self.x = Input(master, 140, 175, 'x: ', width=7)
        
        Btn(master, 'Submit', 25, 20, 140, self.submit) 
        self.find_btn = Btn(master, "Show 'y' for any 'x'", 15, 20, 175, self.show_y, state='disabled')
        
    def submit(self):
        if self.a.access and self.b.access and self.c.access:   
            if eval(self.a.get())!=0:
                a = eval(self.a.get())
                b = eval(self.b.get())
                c = eval(self.c.get())
                self.formula = lambda x: a*(x**2) + b*x + c
                x = -b/(a*2)
                y = self.formula(x)
                    
                self.find_btn.change_state('normal')
                self.show_steps(a, b, c, x, y)
                self.show_plot(x, y)
                
            else:
                messagebox.showwarning("Parabola or Line?","Your parabola is a line!")
        else:
            messagebox.showwarning('ERROR', 'Not Complete!')
        
    def show_y(self):
        if self.x.access:
            x = eval(self.x.get())
            y = self.formula(x)
            self.x.insert(x)
            messagebox.showinfo('Show y', f"'y' for {x}: {y:.3f}")
                
        else:
            messagebox.showwarning('ERROR', 'Please enter a valid number!')

    def show_steps(self, a, b, c, x, y):                
        xs = np.arange(x-2, x+2.1, 1)
        ys = list(map(self.formula, xs))

        self.steps = f''' 
X = -{b} / 2*{a} =  {x:.4f}
Y = {a}X² + {b}X + {c} =  {y:.4f}

X : {xs[0]:.3f} ,  {xs[1]:.3f} ,  {xs[2]:.3f} ,  {xs[3]:.3f} ,  {xs[4]:.3f}
                                  ˅
Y :  {ys[0]:.3f} ,  {ys[1]:.3f} ,  {ys[2]:.3f} ,  {ys[3]:.3f} ,  {ys[4]:.3f}
'''

        messagebox.showinfo('Steps', self.steps)
                
    def show_plot(self, x, y):
        xs = np.arange(x-3, x+3.1, 0.1)
        ys = list(map(self.formula, xs))
        
        plt.plot(xs, ys)
        plt.grid()
        plt.show()
        
    def clear(self):
        self.a.clear()
        self.b.clear()
        self.c.clear()
        self.x.clear()
    
    def show_about(self):
        dialog = Tk()
        dialog.title('About us')
        dialog.geometry('300x100+550+350')
        dialog.resizable(False, False)
        if os.path.exists(icon):
            dialog.iconbitmap(icon)
        dialog.focus_force()
        
        print('\a')
        Label(dialog, text='This program made by Sina.f').pack(pady=12)
        Button(dialog, text='GitHub', width=8, command=lambda: webbrowser.open('https://github.com/sina-programer')).place(x=30, y=50)
        Button(dialog, text='Instagram', width=8, command=lambda: webbrowser.open('https://www.instagram.com/sina.programer')).place(x=120, y=50)
        Button(dialog, text='Telegram', width=8, command=lambda: webbrowser.open('https://t.me/sina_programer')).place(x=210, y=50)
        
        dialog.mainloop()

    def init_menu(self, master):
        menu = Menu(master)  
        menu.add_command(label='Steps', command=lambda: messagebox.showinfo('Steps', self.steps))
        menu.add_command(label="Help", command=lambda: messagebox.showinfo('Help', help_msg))  
        menu.add_command(label="About us", command=self.show_about)  
        
        return menu              


help_msg = '''This program helps you to calculate parabola's
Just fill the fields and submit it!

Parameters:
y = ax² + bx + c

Shortcuts
<Return> Calculate your parabola
<Esc>        Clear all fields'''

icon = r'Files\icon.ico'

if __name__ == '__main__':
    root = Tk()
    root.title('Parabola Calculator')
    root.geometry('220x210+550+300')
    root.resizable(False, False)  
    root.focus_force()
    
    if os.path.exists(icon):
        root.geometry('220x230+550+300')
        root.iconbitmap(icon)
    
    app = App(root)
    
    root.mainloop()
