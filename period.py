
import numpy as np
import pandas as pd
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

path='datas.xlsx'
today = pd.Timestamp('today')

#Period remindnew excel is call or not.
#Or A new excel is need to create!
try:
    dataset = pd.read_excel(path)
    if dataset['Menstrual level'][len(dataset)-1] != 0:
        reminder_index = len(dataset)-2
        while dataset['Menstrual level'][reminder_index] != 0:
            reminder_index = reminder_index-1
        remind_days = (today - pd.to_datetime(dataset['Date'][reminder_index+1])).days+1
        if remind_days > 0:            
            remind = Tk()
            remind.title('Period remind')
            remind.geometry('300x300') 
            remind_lable = Label(remind, text= str(remind_days)+"st days in period!\n")
            remind_lable.pack(fill=BOTH, expand = True)             
            remind_lable.mainloop()   
except:
    #exit()
    dataset = pd.DataFrame({'Date':[],'Fahrenheit':[],'Menstrual level':[],'Progesterone':[],'Sexual behaviour':[]})
    remind = Tk()
    remind.title('Warnning!')
    remind.geometry('300x300') 
    remind_lable = Label(remind, text="A new excel is created!\n")
    remind_lable.pack(fill=BOTH, expand = True)    
    
  



root = Tk()
root.title('Data recording')
root.geometry('300x300')

def addin():    
    try:
        a=(pd.to_datetime(Date_input.get())).strftime('%m/%d/%y')
        b=float(Fahrenheit_input.get()) 
        if (b>110.0 or b<95.0) and b != 0:
             raise
        if menstrual_level.get()==0:
            menstrual_level_get = "Free day.\n"
        else: 
            menstrual_level_get = "You have period.\n"
        progesterone_get_get = ""    
        if progesterone_get.get() == 1:
            progesterone_get_get = "Take progesterone today.\n"   
        sex_get_get = ""         
        if sex_get.get() == 1:
            sex_get_get = "Having sexual behaviour today.\n"
        
        confirm = Tk()
        confirm.title('You date is added!')
        confirm.geometry('300x300')
        addin_lable = Label(confirm, text=Date_input.get()+"\n"+ \
            Fahrenheit_input.get()+'\xB0F\n'+menstrual_level_get+\
            progesterone_get_get+sex_get_get+"Data is recorded!")
        addin_lable.pack(fill=BOTH, expand = True)
        
        #update excel
        global dataset 
        for i in range (len(dataset)):
            if dataset['Date'][i]==a:
                dataset=dataset.drop(index = i)
        df = pd.DataFrame({'Date': [a],'Fahrenheit': [b],'Menstrual level': [int(menstrual_level.get())],
            'Progesterone': [int(progesterone_get.get())],'Sexual behaviour': [int(sex_get.get())]})
        dataset=dataset.append(df,sort=False, ignore_index=True)
        dataset['Date'] =pd.to_datetime(dataset['Date'])        
        dataset = dataset.sort_values(by = 'Date')
        dataset['Date']=pd.to_datetime(dataset['Date']).apply(lambda x:x.strftime('%m/%d/%y'))
        dataset.to_excel(path,index=False)      
        return
    except:
        confirm = Tk()
        confirm.title('Warrning')
        confirm.geometry('300x300')
        addin_lable = Label(confirm, text="Input data has error!")
        addin_lable.pack(fill=BOTH, expand = True)
        return
        
    
def graph():
    global dataset 
    s_table=pd.DataFrame(dataset,columns= ['Date','Sexual behaviour'])
    s_table['Sexual behaviour'] = s_table['Sexual behaviour']*40
    p_table=pd.DataFrame(dataset,columns= ['Date','Progesterone'])
    p_table['Progesterone'] = p_table['Progesterone']*120
    f_table=pd.DataFrame(dataset,columns= ['Date','Fahrenheit'])
    m_table=pd.DataFrame(dataset,columns= ['Date','Menstrual level'])
    m_table['Menstrual level'] = m_table['Menstrual level']*20
    k= np.linspace(0,len(dataset)-1,len(dataset),dtype = "int")
    
    table_g= Tk() 
    table_g.title('Data recording')
    table_g.geometry('1280x720')

    figure1 = plt.Figure()
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, table_g)
    bar1.get_tk_widget().pack(side=LEFT,fill=BOTH, expand = True)
    p_table = p_table[['Date','Progesterone']].groupby('Date').sum()
    p_table.plot(kind='bar',ax=ax1,color='y')
    #s_table = s_table[['Date','Sexual behaviour']].groupby('Date').sum()
    #s_table.plot(kind='bar',ax=ax1,color='m')
    #ax1.set_title('Day for Progesterone')
    #for i_a, i_b in (zip(k,p_table['Progesterone'])):
    #    ax1.text(i_a-0.2,48, '{}'.format("Yes" if i_b else ""))
    #for i_a, i_b in (zip(k,p_table['Progesterone'])):
    #    ax1.text(i_a-0.2,8, '{}'.format("Yes" if i_b else ""))
    #ax1.tick_params(labelrotation=45,labelleft=False)
    
    figure2 = plt.Figure()
    #ax2 = figure2.add_subplot(111)
    #line2 = FigureCanvasTkAgg(figure2, table_g)
    #line2.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand = True)
    f_table = f_table[['Date','Fahrenheit']].groupby('Date').sum()
    f_table.plot(kind='line', ax=ax1, marker='o',color='blue')
    #ax2.set_title('Temperature of body')
    for i_a, i_b in (zip(k,f_table['Fahrenheit'])):
        ax1.text(i_a-0.2, i_b, '{:.2f}\xB0F\n'.format(i_b))
    #ax1.tick_params(labelrotation=45,labelleft=False)
    
    figure3 = plt.Figure()
    #ax3 = figure3.add_subplot(111)
    #bar3 = FigureCanvasTkAgg(figure3, table_g)
    #bar3.get_tk_widget().pack(side=LEFT,fill=BOTH, expand = True)
    m_table = m_table[['Date','Menstrual level']].groupby('Date').sum()
    m_table.plot(kind='line', ax=ax1, marker='v',color='red')
    #ax3.set_title('Day for period')
    for i_a, i_b in (zip(k,m_table['Menstrual level'])):
        if i_b == 0:
            level="Zero"
        elif i_b == 20:
            level="Spotting"
        elif i_b == 40:
            level="Light"
        elif i_b == 60:
            level="Medium"
        else:
            level="Heavy"   
        ax1.text(i_a-0.3, i_b+2, '{}'.format(level))
    ax1.tick_params(labelrotation=60,labelleft=False)
    
    table_g.mainloop()
    
    
#Date
Date_lab = Label(root,text='Data')
Date_lab.place(x=20,y=20)    
Date_input = Entry(root, width=8)
Date_input.insert(0,today.strftime('%m/%d/%y'))
Date_input.place(x=120,y=20)

#Fahrenheit
Fahrenheit_lab = Label(root,text='Fahrenheit')
Fahrenheit_lab.place(x=20,y=60)
Fahrenheit_input = Entry(root, width=8)
Fahrenheit_input.insert(0,0)
Fahrenheit_input.place(x=120,y=60)

Fahrenheit_lab = Label(root,text='\xB0F (0 as None)')
Fahrenheit_lab.place(x=200,y=60)

#menses
menses_lab = Label(root,text='menstrual level')
menses_lab.place(x=20,y=100)
menstrual_level = IntVar()

rb1=Radiobutton(root,text='Zero',value='0',variable=menstrual_level)
rb1.place(x=120,y=100)
rb2=Radiobutton(root,text='Spotting',value='1',variable=menstrual_level)
rb2.place(x=120,y=123)
rb3=Radiobutton(root,text='Light',value='2',variable=menstrual_level)
rb3.place(x=120,y=146)
rb2=Radiobutton(root,text='Medium',value='3',variable=menstrual_level)
rb2.place(x=200,y=100)
rb3=Radiobutton(root,text='Heavy',value='4',variable=menstrual_level)
rb3.place(x=200,y=123)

menstrual_level.set(0)
    
#progesterone
progesterone_get = IntVar() 
   
progesterone_lab = Label(root,text='Progesterone')
progesterone_lab.place(x=20,y=180)

progesterone_input = Checkbutton(root,text='Yes/No',variable = progesterone_get, \
                 onvalue = 1, offvalue = 0, width=8)
progesterone_input.place(x=110,y=180)

#Sex
sex_get = IntVar() 
   
sex_lab = Label(root,text='Sexual behaviour')
sex_lab.place(x=20,y=210)

sex_input = Checkbutton(root,text='Yes/No',variable = sex_get, \
                 onvalue = 1, offvalue = 0, width=8)
sex_input.place(x=110,y=210)

#Submit
Finish = Button(root, text="Submit", command=addin)
Finish.place(x=100,y=250)

#graph
graph_out = Button(root, text="graph", command=graph)
graph_out.place(x=180,y=250)

root.mainloop()


