from tkinter import *
from tkinter.ttk import *
from textdata import *  #list of websites, codebook for PR
from modfunctions import * #functions to upload the data
import requests


#for singe-mandate districts:
def fptp(url, lbl):
#getting OIK names
    progbar.start()
    flag=1
    try:
        pageforcrawling=requests.get(url)
    except requests.exceptions.ConnectionError:
        flag=0
    if flag==0:
        connectionerror()
    else:    
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
                progbar.step(amount=3)
                root.update()
            except RecursionError:
                connectionerror()
                progbar.stop()
            except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema, IndexError):
                continue

        #writing each codebook in a separate file
        for n in range(len(codebooklist)):
            file=open(lbl+' codebook '+str(n+1)+'.txt', encoding="utf-8", mode="w")
            progbar.step(amount=3)
            for p in range(len(codebooklist[n])):
                file.write('v'+str(p+1)+'-' + codebooklist[n][p]+'\n')
                progbar.step(amount=3)
                root.update()
            file.close()

        ###opening csv file for each OIK
        for num_tik_row in range(len(listingfin)):
            filecsv=open(lbl+' FPTP '+str(num_tik_row+1)+".csv", encoding="utf-8", mode="w")
            filename=lbl+' FPTP '+str(num_tik_row+1)+".csv"

        #writing variable names for each csv file
            for vlength in range(len(codebooklist[num_tik_row])):
                filecsv.write('v'+str(vlength+1)+',')
                progbar.step(amount=3)
                root.update()
            filecsv.write('\n')

        #getting the data for each csv file
            try:
                for num_tik_col in range(len(listingfin[num_tik_row])):
                    for j in range (len(getlistuik(listingfin[num_tik_row][num_tik_col]))):
                        filecsv.write(reqdata(getpageuik(getlistuik(listingfin[num_tik_row][num_tik_col])[j])))
                        progbar.step(amount=3)
                        root.update()       
            except RecursionError:
                filecsv.close()
                connectionerror()
                progbar.stop()
                root.update()
            except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema, IndexError):
                continue
            filecsv.close()
            progbar.stop()

#for party lists:
def pr(url, lbl):
    progbar.start()
    flag=1
    #writing a codebook:
    file=open(lbl+ ' codebook PR.txt', encoding="utf-8", mode="w")
    file.write(textpr)
    file.close()
    
    #getting OIK names
    try:
        pageforcrawling=requests.get(url)
    except requests.exceptions.ConnectionError:
        flag=0
    if flag==0:
        connectionerror()
    else:
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
            progbar.step(amount=3)
            root.update()

        ###opening csv
        filecsv=open(lbl+' PR.csv', encoding="utf-8", mode="w")
        filename=(lbl+' PR.csv')
        #writing variable names for the csv file
        for vlength in range(19):
            filecsv.write('v'+str(vlength+1)+',')
            progbar.step(amount=3)
        for vlength in range(19, 33):
            filecsv.write('v'+ str(vlength+1)+',' + 'v'+str(vlength+1)+'.1,')
            progbar.step(amount=3)
        filecsv.write('\n')

        #getting the data for the csv file
        try:
            for num_tik_row in range(len(listingfin)):
                try:
                    for num_tik_col in range(len(listingfin[num_tik_row])):
                        for j in range (len(getlistuik(listingfin[num_tik_row][num_tik_col]))):
                            filecsv.write(reqdata(getpageuik_pr(getlistuik(listingfin[num_tik_row][num_tik_col])[j])))
                            progbar.step(amount=3)
                            root.update()
                except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema, IndexError):
                    continue
                except RecursionError:
                    filecsv.close()
                    connectionerror()
                    progbar.stop()
                    root.update()

        filecsv.close()
        progbar.stop()


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
    guistart(reg, t_elect)
    labelact.configure(text='Готово!')
    comboboxreg.config(state='readonly')
    comboboxtype.config(state='readonly')
    btn.config(state='normal')
    root.update()


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
root.title('Выборы депутатов ГД ФС РФ 2016') #Parliamentary elections 2016
root.geometry('400x200')
root.resizable(False, False)
labelreg=Label(root,text='Выберите регион') #Choose the region 
#List items represents all Russian regions
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
labeltype=Label(root, text='Выберите систему выборов') #Choose electoral system 
#in Russia, half of MPs are elected by FPTP system and another half are elected by PR system
#Options represent a choice between FPTP and PR 
comboboxtype=Combobox(root, values=['''По одномандатным округам''',
'''По партийным спискам'''], width=30, state="readonly")
comboboxtype.set('По одномандатным округам')
labelact=Label(root, text='')
labelact.pack()
btn=Button(root,text='Скачать данные в текущую папку', command=start) #Download the data to the current folder
progbar=Progressbar(orient="horizontal", length=150, mode="indeterminate")


labelreg.pack()
comboboxreg.pack()
labeltype.pack()
comboboxtype.pack()
progbar.pack()
labelact.pack(side="bottom")
btn.pack(side="bottom")
root.mainloop()
