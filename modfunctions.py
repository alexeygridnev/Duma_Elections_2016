#UIK - polling station
#TIK - territorial electoral commission (one level up)
#OIK - distict level electoral commission (two levels up)

import requests
import bs4
import time
import sys

#setting the limit amount of reconnections by setting the limit of recursion, 
#to make program stop reconnecting to the server after 100 retrials
sys.setrecursionlimit(100)

#getting variable names from the page of UIK
def reqvarnames(url, timeout=2):
    try:
        rawdoc=requests.get(url)
        rawdoctxt=rawdoc.text
        start=rawdoctxt.find("Дата голосования")
        end=rawdoctxt.find('</table> <br/>')
        doc=rawdoctxt[start:end]
        docbs=bs4.BeautifulSoup(doc)
        datalist=[]
        datalist.append('Номер УИК')
        ##getting all the variable names
        docfin=docbs.findAll(align="left")
        for i in range (len(docfin)):
            datalist.append(docfin[i].text)
        return(datalist)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        time.sleep(10)
        return reqvarnames(url)
    except requests.packages.urllib3.exceptions.MaxRetryError:
        time.sleep(300)
        return reqvarnames(url)


#getting variable values from the page of UIK
def reqdata(url, timeout=2):
    try:
        rawdoc=requests.get(url)
        rawdoctxt=rawdoc.text
        start=rawdoctxt.find("Дата голосования")
        end=rawdoctxt.find('</table> <br/>')
        doc=rawdoctxt[start:end]
        docbs=bs4.BeautifulSoup(doc)

        ##finding the name of the UIK
        tablelist=docbs.findAll('td',limit=3)
        uikname=tablelist[2].text
        uikname=uikname.replace('УИК №', 'UIK_Num')
        string=uikname+','

        ##getting all the variables
        docfin=docbs.findAll(align="right")
        datalist=[]
        for i in range (0, 18):
            datalist.append(docfin[i+1].text.replace('\n', ','))
        for i in range (18, (len(docfin)-1)):
            stringaux=str(docfin[i+1])
            stringaux=stringaux.replace('</b>', ',</b>')
            stringaux=stringaux.replace('</td>', '')
            stringaux=stringaux.rstrip()
            datalist.append(bs4.BeautifulSoup(stringaux).text)
        
        for i in range (0, (len(docfin)-1)):
            string=string+datalist[i]
        for symbol in string:
            if symbol=='%':
                string=string.replace('%', ',')
        string=string[0:(len(string)-1)]
        string=string.rstrip()
        string=string.rstrip(',')
        string=string+'\n'
        datastring=string
        return(datastring) ##returns a string!
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        time.sleep(10)
        return reqdata(url)
    except requests.packages.urllib3.exceptions.MaxRetryError:
        time.sleep(300)
        return reqdata(url)

#getting TIK addresses from OIK page
def gettik(area):
    try:
        pageforcrawling=requests.get(area, timeout=2)
        start=pageforcrawling.text.find('Нижестоящие избирательные комиссии')
        end=pageforcrawling.text.find('</select>')
        workingpage=pageforcrawling.text[start:end]
        listingtik=workingpage.split('</option>')
        listingtik=listingtik[1:len(listingtik)]
        for i in range(len(listingtik)):
            listingtik[i]=listingtik[i].lstrip('<option value="')
            listingtik[i]=listingtik[i] [0:(listingtik[i].find('">'))]
            listingtik[i]=listingtik[i].replace('amp;', '')
        return(listingtik)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        time.sleep(10)
        return gettik(area)
    except requests.packages.urllib3.exceptions.MaxRetryError:
        time.sleep(300)
        return gettik(area)

#getting UIK addresses from TIK page
def getlistuik(pagetik):
    try:
        pageforcrawlingmin=requests.get(pagetik, timeout=2)
        startmin=pageforcrawlingmin.text.find('Нижестоящие избирательные комиссии')
        endmin=pageforcrawlingmin.text.find('</select>')
        workingpagemin=pageforcrawlingmin.text[startmin:endmin]
        listingmin=workingpagemin.split('</option>')
        listingmin=listingmin[1:len(listingmin)-1]
        return listingmin
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        time.sleep(10)
        return getlistuik(pagetik)
    except requests.packages.urllib3.exceptions.MaxRetryError:
        time.sleep(300)
        return getlistuik(pagetik)

#getting to the results page of UIK from the raw data, FPTP
def getpageuik(pageuikraw):
    pageuikraw=pageuikraw.lstrip('<option value="')
    pageuikraw.find('"')
    pageuikraw=pageuikraw[0:(pageuikraw.find('"'))]
    pageuikraw=pageuikraw.replace('amp;', '')
    pageuikraw=pageuikraw.replace('&pronetvd=0', '')
    pageuikraw=pageuikraw.replace('&global=true', '')
    pageuikraw=pageuikraw.replace('&type=0', '')
    pageuik=pageuikraw+'&type=463'
    return(pageuik)

#getting to the results page of UIK from the raw data, PR
def getpageuik_pr(pageuikraw):
    pageuikraw=pageuikraw.lstrip('<option value="')
    pageuikraw.find('"')
    pageuikraw=pageuikraw[0:(pageuikraw.find('"'))]
    pageuikraw=pageuikraw.replace('amp;', '')
    pageuikraw=pageuikraw.replace('&pronetvd=0', '')
    pageuikraw=pageuikraw.replace('&global=true', '')
    pageuikraw=pageuikraw.replace('&type=0', '')
    pageuik=pageuikraw+'&type=242'
    return(pageuik)

