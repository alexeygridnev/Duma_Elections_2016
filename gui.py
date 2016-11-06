from tkinter import *
from tkinter.ttk import *
from textdata import *  #list of websites, codebook for PR
from modfunctions import * #functions to upload the data
import requests


#for singe-mandate districts:
def fptp(url, lbl):
#getting OIK names
    pageforcrawling=requests.get(url)
    start=pageforcrawling.text.find('Нижестоящие избирательные комиссии')
    end=pageforcrawling.text.find('</select>')
    workingpage=pageforcrawling.text[start:end]
    listing=workingpage.split('</option>')
    listing=listing[1:len(listing)]
    for i in range(len(listing)):
        listing[i]=listing[i].lstrip('<option value="')
        listing[i].find('"')
        listing[i]=listing[i] [0:(listing[i].find('"'))]
        listing[i]=listing[i].replace('amp;', '')
        root.update()

    listingfin=[]
    for k in range (len(listing)-1):
        listingfin.append(gettik(listing[k]))
        root.update()
    
    codebooklist=[]

    #getting codebook for each district, from the page of 0th UIK from 0th TIK for each district
    for num_tik_row in range(len(listingfin)):
        try:
            codebooklist.append(reqvarnames(getpageuik(getlistuik(listingfin[num_tik_row][0])[0])))
            root.update()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            connectionerror()
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
            continue

    #writing each codebook in a separate file
    for n in range(len(codebooklist)):
        file=open(lbl+' codebook '+str(n+1)+'.txt', "w")
        for p in range(len(codebooklist[n])):
            file.write('v'+str(p+1)+'-' + codebooklist[n][p]+'\n')
            root.update()
        file.close()
        
    ###opening csv file for each OIK
    for num_tik_row in range(len(listingfin)):
        filecsv=open(lbl+' FPTP '+str(num_tik_row+1)+".csv", "w")
        filename=lbl+' FPTP '+str(num_tik_row+1)+".csv"

    #writing variable names for each csv file
        for vlength in range(len(codebooklist[num_tik_row])):
            filecsv.write('v'+str(vlength+1)+',')
        filecsv.write('\n')

    #getting the data for each csv file
        try:
            for num_tik_col in range(len(listingfin[num_tik_row])):
                for j in range (len(getlistuik(listingfin[num_tik_row][num_tik_col]))):
                    filecsv.write(reqdata(getpageuik(getlistuik(listingfin[num_tik_row][num_tik_col])[j])))
                    root.update()       
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            filecsv.close()
            connectionerror()
            root.update()
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
            continue
        filecsv.close()

#for party lists:
def pr(url, lbl):
    #writing a codebook:
    file=open(lbl+ ' codebook PR.txt', "w")
    file.write(textpr)
    file.close()
    
    #getting OIK names
    pageforcrawling=requests.get(url)
    start=pageforcrawling.text.find('Нижестоящие избирательные комиссии')
    end=pageforcrawling.text.find('</select>')
    workingpage=pageforcrawling.text[start:end]
    listing=workingpage.split('</option>')
    listing=listing[1:len(listing)]
    for i in range(0, len(listing)):
        listing[i]=listing[i].lstrip('<option value="')
        listing[i].find('"')
        listing[i]=listing[i] [0:(listing[i].find('"'))]
        listing[i]=listing[i].replace('amp;', '')
        root.update()

    listingfin=[]
    for k in range (len(listing)-1):
        listingfin.append(gettik(listing[k]))
        root.update()
    
    ###opening csv
    filecsv=open(lbl+' PR.csv', "w")
    filename=(lbl+' PR.csv')
    #writing variable names for the csv file
    for vlength in range(19):
        filecsv.write('v'+str(vlength+1)+',')
    for vlength in range(19, 33):
        filecsv.write('v'+ str(vlength+1)+',' + 'v'+str(vlength+1)+'.1,')
    filecsv.write('\n')

    #getting the data for the csv file
    try:
        for num_tik_row in range(len(listingfin)):
            try:
                for num_tik_col in range(len(listingfin[num_tik_row])):
                    for j in range (len(getlistuik(listingfin[num_tik_row][num_tik_col]))):
                        filecsv.write(reqdata(getpageuik_pr(getlistuik(listingfin[num_tik_row][num_tik_col])[j])))
                        root.update()
            except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                continue
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        filecsv.close()
        connectionerror()
        root.update()

    filecsv.close()


#button press command:
def start():
    reg=comboboxreg.get()
    t_elect=comboboxtype.get()
    #disabling comboboxes and the button command during the download:
    comboboxreg.config(state='disabled')
    comboboxtype.config(state='disabled')
    btn.config(state='disabled')
    labelact.configure(text='Загружаю данные...')
    labelact.pack()
    root.update()
    try:
        guistart(reg, t_elect, typetable)
        labelact.configure(text='Готово!')
        comboboxreg.config(state='readonly')
        comboboxtype.config(state='readonly')
        comboboxtypetab.config(state='readonly')
        btn.config(state='normal')
        root.update()
    except requests.exceptions.ConnectionError:
        connectionerror()

def connectionerror():        
    labelact.config(text='')
    root.update()
    errormsg=Toplevel(root)
    errormsg.geometry('600x100')
    errormsg.grab_set_global
    errormsg.resizable(False, False)
    errorlabel1=Label(errormsg, text='Неполадки в соединении с сайтом Избиркома. Повторите попытку позднее')
    errorlabel2=Label(errormsg, text='Данные, загруженные до разрыва соединения, сохранены в текущей папке')
    errorbutton=Button(errormsg, text='Закрыть', command=errormsg.destroy)
    #enabling comboboxes and the button after the error:
    comboboxreg.config(state='readonly')
    comboboxtype.config(state='readonly')
    btn.config(state='normal')
    root.update()
    errorlabel1.pack()
    errorlabel2.pack()
    errorbutton.pack(side="bottom")
        
def guistart(region, t_elect):
    url=listdict.get(region)
    if t_elect=="По одномандатным округам":
        fptp(url, region)
    elif t_elect=="По партийным спискам":
        pr(url, region)

#GUI
root=Tk()
root.title('Выборы депутатов ГД ФС РФ 2016')
root.geometry('400x200')
root.resizable(False, False)
labelreg=Label(root,text='Выберите регион')
comboboxreg = Combobox(root,values = ['''Республика Адыгея''',
'''Республика Алтай''',
'''Республика Башкортостан''',
'''Республика Бурятия''',
'''Республика Дагестан''',
'''Республика Ингушетия''',
'''Кабардино-Балкарская республика''',
'''Республика Калмыкия''',
'''Карачаево-Черкесская республика''',
'''Республика Карелия''',
'''Республика Коми''',
'''Республика Крым''',
'''Республика Марий Эл''',
'''Республика Мордовия''',
'''Республика Саха(Якутия)''',
'''Республика Северная Осетия-Алания''',
'''Республика Татарстан''',
'''Республика Тыва''',
'''Удмуртская республика''',
'''Республика Хакасия''',
'''Чеченская республика''',
'''Чувашская республика''',
'''Алтайский край''',
'''Забайкальский край''',
'''Камчатский край''',
'''Краснодарский край''',
'''Красноярский край''',
'''Пермский край''',
'''Приморский край''',
'''Ставропольский край''',
'''Хабаровский край''',
'''Амурская область''',
'''Архангельская область''',
'''Астраханская область''',
'''Белгородская область''',
'''Брянская область''',
'''Владимирская область''',
'''Волгоградская область''',
'''Вологодская область''',
'''Воронежская область''',
'''Ивановская область''',
'''Иркутская область''',
'''Калининградская область''',
'''Калужская область''',
'''Кемеровская область''',
'''Кировская область''',
'''Костромская область''',
'''Курганская область''',
'''Курская область''',
'''Ленинградская область''',
'''Липецкая область''',
'''Магаданская область''',
'''Московская область''',
'''Мурманская область''',
'''Нижегородская область''',
'''Новгородская область''',
'''Новосибирская область''',
'''Омская область''',
'''Оренбургская область''',
'''Орловская область''',
'''Пензенская область''',
'''Псковская область''',
'''Ростовская область''',
'''Рязанская область''',
'''Самарская область''',
'''Саратовская область''',
'''Сахалинская область''',
'''Свердловская область''',
'''Смоленская область''',
'''Тамбоская область''',
'''Тверская область''',
'''Томская область''',
'''Тульская область''',
'''Тюменская область''',
'''Ульяновская область''',
'''Челябинская область''',
'''Ярославская область''',
'''Москва''',
'''Санкт-Петербург''',
'''Севастополь''',
'''Еврейская Авт. Обл.''',
'''Ненецкий АО''',
'''Ханты-Манскийский АО''',
'''Чукотский АО''',
'''Ямало-Ненецкий АО''',
],height=10, width=30, state="readonly")
comboboxreg.set('Республика Адыгея')
labeltype=Label(root, text='Выберите систему выборов')
comboboxtype=Combobox(root, values=['''По одномандатным округам''',
'''По партийным спискам'''], width=30, state="readonly")
comboboxtype.set('По одномандатным округам')
labelact=Label(root, text='')
labelact.pack()
btn=Button(root,text='Скачать данные в текущую папку', command=start)

labelreg.pack()
comboboxreg.pack()
labeltype.pack()
comboboxtype.pack()
labelact.pack(side="bottom")
btn.pack(side="bottom")
root.mainloop()
