from tkinter import *
import pandas as pd
from PIL import Image
from PIL import ImageGrab

def draw():


    root=Tk()
    root.geometry("1000x500")
    root.attributes('-fullscreen', True)

    df1 = pd.read_csv(r'AppData\Files\distributed_load.csv')
    df2 = pd.read_csv(r'AppData\Files\point_load.csv')
    df3 = pd.read_csv(r'AppData\Files\moment_load.csv')
    df4=pd.read_csv(r'AppData\Files\boundary_condition.csv')

    from fractions import Fraction

    def func(f):
        if type(f) == str:
            f=float(sum(Fraction(s) for s in f.split()))
            return f
        else:
            return f

    left=str(df4['LEFT'].iloc[0])
    right=str(df4['RIGHT'].iloc[0])
    print(left)
    print(right)

    figure= Canvas(root,width=1000,height=500,bg='white')
    figure.pack()

    def create_arrow(x):
        figure.create_line(x,175,x,220,fill='black')
        figure.create_line(x,220,x+10,215,fill='black')
        figure.create_line(x,220,x-10,215,fill='black')

    def create_moment(f4,M):
        x=200+f4*600
        if '-' in M:
            figure.create_line(x,225,x-50,275,x,325,fill='black',smooth=1)
            figure.create_line(x,240,x,225,x-15,225,fill='black')
            
        else:
            figure.create_line(x,225,x+50,275,x,325,fill='black',smooth=1)
            figure.create_line(x,240,x,225,x+15,225,fill='black')
            

        figure.create_text(x,275,text=M, fill="black", font=('Calibri 15 bold'))
        #figure.create_line(x,450,x,475,fill='black')
        #figure.create_text(x,500,text="x=%0.2f"%(f4)+" L",fill='black',font=('Calibri 8'))



    def create_dload(f1,f2):
        x1=200+f1*600
        x2=200+f2*600
        create_arrow(x1)
        x=x1
        while (x<=x2):
            create_arrow(x)
            x=x+25

        figure.create_line(x1,175,x2,175,fill='black')

        figure.create_text((x1+x2)/2,120,text="P=f(x)", fill="black", font=('Calibri 15 bold')) 
        #figure.create_line(x1,450,x1,475,fill='black')
        #figure.create_line(x2,450,x2,475,fill='black')
        #figure.create_text(x1,500,text="x=%0.2f"%(f1)+" L",fill='black',font=('Calibri 8'))
        #figure.create_text(x2,500,text="x=%0.2f"%(f2)+" L",fill='black',font=('Calibri 8'))



    def create_pload(f3,P):
        x=200+f3*600
        #print(P[0])
        

        if '-'in P :
            figure.create_line(x,330,x,400,fill='black',width=4)
            figure.create_line(x,330,x+10,335,fill='black',width=3)
            figure.create_line(x,330,x-10,335,fill='black',width=3)
            figure.create_text(x,420,text=P, fill="black", font=('Calibri 15 bold'))

        else:
            figure.create_line(x,150,x,220,fill='black',width=4)
            figure.create_line(x,220,x+10,215,fill='black',width=3)
            figure.create_line(x,220,x-10,215,fill='black',width=3)
            figure.create_text(x,120,text=P, fill="black", font=('Calibri 15 bold'))
        

        #figure.create_line(x,450,x,475,fill='black')
        #figure.create_text(x,500,text="x=%0.2f"%(f3)+" L",fill='black',font=('Calibri 8'))



    #create_axes
    figure.create_line(250,50,200,50,200,100,fill='black')
    figure.create_line(245,45,250,50,245,55,fill='black')
    figure.create_line(205,95,200,100,195,95,fill='black')
    figure.create_text(200,40,text="x=0", fill="black", font=('Calibri 13'))
    figure.create_text(255,50,text="x", fill="black", font=('Calibri 15'))
    figure.create_text(200,105,text="z", fill="black", font=('Calibri 15'))

    #rectangle
    beam= figure.create_rectangle(200,300,800,250,outline='black',fill='white')

    i=0
    j=0
    k=0

    while i<df1[df1.columns[0]].count():
        f1=func(df1["LEFT_LIMIT"].iloc[i])
        f2=func(df1["RIGHT_LIMIT"].iloc[i])
        create_dload(f1,f2)
        i=i+1

    while j<df2[df2.columns[0]].count():
        f3=func(df2["LOCATION"].iloc[j])
        if str(df2["MULTIPLIER"].iloc[j])=='1':
            P='P'
        elif str(df2["MULTIPLIER"].iloc[j])=='-1':
            P='-P'
        else:
            P=str(df2["MULTIPLIER"].iloc[j])+'P'
        create_pload(f3,P)
        j=j+1

    while k<df3[df3.columns[0]].count():
        f4=func(df3["LOCATION"].iloc[k])
        if str(df3["MULTIPLIER"].iloc[k])=='1':
            M='M'
        elif str(df3["MULTIPLIER"].iloc[k])=='-1':
            M='-M'
        else:
            M=str(df3["MULTIPLIER"].iloc[k])+'M'
        create_moment(f4,M)
        k=k+1


    #left bc

    if(left=='fixed'):
        figure.create_line(195,225,195,325,fill='grey',width=10)

    elif(left=='roller'):
        figure.create_polygon(200,275,180,295,180,255,fill='black',outline='black')
        figure.create_oval(180,295,170,285,fill='white',outline='black')
        figure.create_oval(180,255,170,265,fill='white',outline='black')
        figure.create_line(165,225,165,325,fill='grey',width=10)

    elif(left=='hinged'):
        figure.create_polygon(200,275,220,320,180,320,fill='black',outline='black')
        figure.create_oval(195,270,205,280,fill='white',outline='black')
        figure.create_line(170,325,230,325,fill='grey',width=10)


    #right_bc

    if(right=='fixed'):
        figure.create_line(805,225,805,325,fill='grey',width=10)

    elif(right=='roller'):
        figure.create_polygon(800,275,820,295,820,255,fill='black',outline='black')
        figure.create_oval(820,295,830,285,fill='white',outline='black')
        figure.create_oval(820,255,830,265,fill='white',outline='black')
        figure.create_line(835,225,835,325,fill='grey',width=10)

    elif(right=='hinged'):
        figure.create_polygon(800,275,820,320,780,320,fill='black',outline='black')
        figure.create_oval(795,270,805,280,fill='white',outline='black')
        figure.create_line(770,325,830,325,fill='grey',width=10)



    root.update()

    def getter(widget):
        widget.update()
        x=root.winfo_rootx()+widget.winfo_x()
        y=root.winfo_rooty()+widget.winfo_y()
        x1=x+widget.winfo_width()
        y1=y+widget.winfo_height()
        img=ImageGrab.grab()
        wid, hgt = img.size
        left=wid*0.25
        right=wid*0.75
        top=0
        bottom=hgt*0.55
        im1 = img.crop((left, top, right, bottom))
        im1.save(r"AppData\Images\beam_diagram.png")
        # Shows the image in image viewer
        
        # displaying the dimensions
        print(str(wid) + "x" + str(hgt))

    getter(figure)  
    print("All done!!")
    root.destroy()
    root.mainloop()
    root.quit()
    


#draw()