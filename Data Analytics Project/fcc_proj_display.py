
import builtins
from tkinter import *
from fcc_danayproj import *
from matplotlib.pyplot import get, text, title
from tkinter import messagebox


window1 = Tk()

window1.title("Victoria Avenue Accident Analysis")
window1.geometry("1560x720")
label1 = Label(window1, text='Victoria Avenue Accident Data Analysis', font=('Arial', 30, 'bold'))
label1.pack()
pic1 = PhotoImage(file='pic3.png')
pic_label = Label(image=pic1)
pic_label.place(x=300, y=500)

label2 = Label(window1, text="Enter initial date here in YYYY-MM-DD format: ")
label2.place(x=10, y=200)
txt1 = Entry(window1, font=('Arial', 10))
txt1.place(x=300, y=200)

label3 = Label(window1, text=" Enter final date here in above mentioned format: ")
label3.place(x=10, y=300)
txt2 = Entry(window1, font=('Arial', 10))
txt2.place(x=300, y=300)
txt3 = Entry(window1, font=('Arial', 10))
txt3.place(x=300, y=400)

def gen_data():
    window2 = Tk()
    try:
        if txt3.get() == '':
            label5 = Message(window2, text= accident_details(txt1.get(),txt2.get()))
            label5.pack()
        else:
            label8 = Message(window2, text= precise_accident_details(txt1.get(),txt2.get(),txt3.get()))   
            label8.pack()
    except Exception as e:
        messagebox.showinfo(title='Exception', message='Invalid date or keyword!')
    window2.mainloop()

    
def gen_analysis():
    try:
        accidents_by_hours(txt1.get(),txt2.get())
    except Exception as e:
        messagebox.showinfo(title='Exception', message='Enter a valid date!')

button3 = Button(window1, text="Generate data", command=gen_data , font=('Arial', 10))
button3.place(x=350, y=450)
button5 = Button(window1, text="Analyse with time", command=gen_analysis, font=('Arial', 10))
button5.place(x=200, y=450)
label7 = Label(window1,text=" Enter keyword (from the list of keywords above): ")
label7.place(x=10, y=400)
label6 = Label(window1, text='[Collision with a fixed object, Collision with vehicle, Fall from or in moving vehicle, No collision and no object struck, Other accident, Struck Pedestrian, Struck animal, Vehicle overturned (no collision), collision with some other object]' )
label6.place(x=10, y= 350)
def vis_alc_imp():
    alcohol_accident()


def vis_alcohol_imp():
    alcohol_accidents_trend()

label4 = Label(window1, text=" Types of accidents due to alcohol: ")
label4.place(x=1200, y=200)
button4 = Button(window1, text='Visualise', command=vis_alc_imp, font=('Arial', 10))
button4.place(x=1400, y=200)
label8 = Label(window1, text="Trend of accidents related to alcohol over the years: " )
label8.place(x=1110, y=150)
button1 = Button(window1, text='Visualise', command=vis_alcohol_imp, font=('Arial', 10))
button1.place(x=1400, y=150)
window1.mainloop()