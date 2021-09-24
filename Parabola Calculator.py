from matplotlib import pyplot as plt
from tkinter import *
import numpy as np
import os

class Input:
    errors = {'empty':'Empty', 'int':'Not integer'}
    def __init__(self, master, x, y, txt_lab):
        self.access = False
        
        self.label = Label(master , text=txt_lab)
        self.label.place(x=x , y=y)

        self.entry = Entry(master , width=15)
        self.entry.place(x=x+20 , y=y+2)

        self.state = Label(master , text="", fg='red')
        self.state.place(x=x+125 , y=y)    
        
    def check(self):
        value = self.entry.get()
        
        if not value:
            self.state.config(text=self.errors['empty'])
            self.access = False
            
        else:
            try:
                value = eval(value)
                self.insert(value)
                self.state.config(text='')
                self.access = True
                
            except:
                self.state.config(text=self.errors['int'])
                self.access = False
                
    def insert(self, txt):
        self.entry.delete(0, 'end')
        self.entry.insert(0, txt)

                
class App:
    def __init__(self, master):
        self.window = master
        self.window.config(menu=self.init_menu()) 
        self.window.bind('<Return>', self.submit)
        self.window.bind('<Escape>', self.escape)
        
        self.steps = ' You have not been active yet '

        self.a = Input(self.window, 16, 20, 'a :')
        self.b = Input(self.window, 16, 60, 'b :')
        self.c = Input(self.window, 16, 100, 'c :')
       
        self.submit_button = Button(self.window, text="Submit", width=15, height=1, bd=2)
        self.submit_button.place(x=20, y=140)
        self.submit_button.bind("<Button>", self.submit)
 
        self.steps_button = Button(self.window, text="Steps", width=8, height=1, bd=2, state='disabled')
        self.steps_button.place(x=145, y=140)
        self.steps_button.bind("<Button>", lambda _: messagebox.showinfo('Steps', self.steps))
        
    def escape(self, event):
        self.a.entry.delete(0, 'end')
        self.b.entry.delete(0, 'end')
        self.c.entry.delete(0, 'end')
    
    def submit(self, event):
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


help_msg = '''This program helps you to calculate parabolas
Just fill fields and submit it!'''

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
