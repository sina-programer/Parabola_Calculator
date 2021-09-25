import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import *
import numpy as np
import os

class Input:
    __errors = {'empty':'Empty', 'int':'Not integer'}
    def __init__(self, master, x, y, txt):
        self.access = False
        self.__x = x
        self.__y = y
        
        self.__label = Label(master, text=txt)
        self.__label.place(x=self.__x, y=self.__y)

        self.__entry = Entry(master, width=15, bd=2)
        self.__entry.place(x=self.__x+20, y=self.__y+2)
        self.__entry.bind('<Enter>', self.__hover)
        self.__entry.bind('<Leave>', self.__leave)

        self.__state = Label(master, fg='red')
        self.__state.place(x=self.__x+125, y=self.__y)    
        
    def check(self):
        value = self.__entry.get()
        
        if not value.strip():
            self.__state.config(text=self.__errors['empty'])
            self.access = False
            
        else:
            try:
                value = eval(value)
                assert isinstance(value, int) or isinstance(value, float)
                self.insert(value)
                self.__state.config(text='')
                self.access = True
                
            except:
                self.__state.config(text=self.__errors['int'])
                self.access = False
        
    def __hover(self, event):
        self.__entry.config(bd=4)
        self.__entry.place(x=self.__x+20, y=self.__y)
        self.__label.config(width=3)
        
    def __leave(self, event):
        self.__entry.config(bd=2)
        self.__entry.place(x=self.__x+20, y=self.__y+2)
        self.__label.config(width=2)
                
    def insert(self, txt):
        self.__entry.delete(0, 'end')
        self.__entry.insert(0, txt)
        
    def get(self):
        return self.__entry.get()
        
    def clear(self):
        self.__entry.delete(0, 'end')


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
        self.window = master
        self.window.config(menu=self.init_menu()) 
        self.window.bind('<Return>', lambda _: self.submit())
        self.window.bind('<Escape>', lambda _: self.escape())
        
        self.steps = ' You have not been active yet '

        self.a = Input(self.window, 16, 20, 'a :')
        self.b = Input(self.window, 16, 60, 'b :')
        self.c = Input(self.window, 16, 100, 'c :')
       
        Btn(master, 'Submit', 15, 20, 140, self.submit) 
        Btn(master, 'Steps', 8, 145, 140, lambda: messagebox.showinfo('Steps', self.steps), 'disabled')
        
    def escape(self):
        self.a.clear()
        self.b.clear()
        self.c.clear()
    
    def submit(self):
        self.a.check()
        self.b.check()
        self.c.check()
        
        if self.a.access and self.b.access and self.c.access:   
            if eval(self.a.entry.get())!=0:
                a = eval(self.a.entry.get())
                b = eval(self.b.entry.get())
                c = eval(self.c.entry.get())
                x = -b/(2*a)
                x = np.arange(x-3 , x+3.1 , 0.1)
                y = list(map(lambda x: a*(x**2)+(b*x)+c , x))
                
                if a>0:
                    messagebox.showinfo("a > 0","Your parabola is up")
                    
                else:
                    messagebox.showinfo("a < 0","Your parabola is down")
                    
                self.steps_button.config(state='normal')
                self.show_steps()
                plt.plot(x,y)
                plt.show()
                messagebox.showinfo('Steps', self.steps)
                
            else:
                messagebox.showinfo("a = 0","Your parabola is a line!")
        else:
            messagebox.showwarning('ERROR', 'Not Complete')

    def show_steps(self):
        a = eval(self.a.entry.get())
        b = eval(self.b.entry.get())
        c = eval(self.c.entry.get())
        x = eval('-b/(2*a)')

        self.x = f'-{b} / 2*{a} =  {x}'
        self.y = f'{a}X² + {b}X + {c}'
        y = f"{eval('a*x**2')} + {eval('b*x')} + {c}"
        self.steps = f'''Steps:   
            
1_  X = {self.x} 
2_  Y = {self.y}
3_  Y = {y}'''

    def init_menu(self):
        self.menu = Menu(self.window)  
        self.menu.add_command(label="Help", command=lambda: messagebox.showinfo('Help', help_msg))  
        self.menu.add_command(label="About us", command=lambda: messagebox.showinfo('About us', about_msg))  
        
        return self.menu              


help_msg = '''This program helps you to calculate parabola's
Just fill the fields and submit it!

Parameters:
y = ax² + bx + c

Shortcuts
<Return> Calculate your parabola
<Esc>        Clear all fields'''

about_msg = '''This program made by Sina.f\n
GitHub: sina-programer
Telegram: sina_programer
Instagram: sina.programer'''

icon = r'Files\icon.ico'

if __name__ == '__main__':
    root = Tk()
    root.title('Parabola Calculator')
    root.geometry('220x180+550+300')
    root.resizable(False, False)  
    
    if os.path.exists(icon):
        root.geometry('220x200+550+300')
        root.iconbitmap(icon)
    
    app = App(root)
    
    root.mainloop()
