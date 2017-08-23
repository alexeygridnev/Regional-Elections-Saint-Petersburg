#UIK - polling station
#TIK - territorial electoral commission (one level up)
#OIK - distict level electoral commission (two levels up)

import requests
import bs4

#getting variable names from the page of UIK
def reqvarnames(url):
    rawdoc=requests.get(url)
    rawdoctxt=rawdoc.text
    start=rawdoctxt.find("Дата голосования")
    end=rawdoctxt.find('br/')
    doc=rawdoctxt[start:end]
    docbs=bs4.BeautifulSoup(doc)
    datalist=[]
    datalist.append('Номер УИК')
    print(datalist[0]+'\n')
    ##getting all the variable names
    docfin=docbs.findAll(align="left")
    for i in range (len(docfin)):
        datalist.append(docfin[i].text)    
        print(datalist[i+1]+'\n')
    return(datalist)

#getting variable values from the page of UIK
def reqdata(url):
    try:
        rawdoc=requests.get(url)
        rawdoctxt=rawdoc.text
        start=rawdoctxt.find("Дата голосования")
        end=rawdoctxt.find('br/')
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
        for i in range (0, 17):
            datalist.append(docfin[i+1].text.replace('\n', ','))
        for i in range (17, (len(docfin)-1)):
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
        print(string)
        datastring=string
        return datastring ##returns a string!
    except Exception:
        pass

#getting TIK addresses from OIK page
def gettik(area):
    pageforcrawling=requests.get(area)
    start=pageforcrawling.text.find('Нижестоящие избирательные комиссии')
    end=pageforcrawling.text.find('</select>')
    workingpage=pageforcrawling.text[start:end]
    listingtik=workingpage.split('</option>')
    listingtik=listingtik[1:len(listingtik)]
    for item in listingtik:
        item=item.lstrip('<option value="')
        item=item [0:(item.find('">'))]
        item=item.replace('amp;', '')
    return listingtik

#getting to the results page of UIK from the raw data
def getpageuik(pageuikraw):
    pageuikraw=pageuikraw.lstrip('<option value="')
    pageuikraw.find('"')
    pageuikraw=pageuikraw[0:(pageuikraw.find('"'))]
    pageuikraw=pageuikraw.replace('amp;', '')
    pageuikraw=pageuikraw.replace('&pronetvd=0', '')
    pageuikraw=pageuikraw.replace('&global=true', '')
    pageuikraw=pageuikraw.replace('&type=0', '')
    pageuikraw=pageuikraw.replace('null', '0')
    tuplemin=pageuikraw.partition('vibid')
    pageuikraw=tuplemin[0]+'type=423&'+tuplemin[1]+tuplemin[2]
    pageuik=pageuikraw
    return pageuik

#getting UIK addresses from TIK page
def getlistuik(pagetik):
    pageforcrawlingmin=requests.get(pagetik)
    startmin=pageforcrawlingmin.text.find('Нижестоящие избирательные комиссии')
    endmin=pageforcrawlingmin.text.find('</select>')
    workingpagemin=pageforcrawlingmin.text[startmin:endmin]
    listingmin=workingpagemin.split('</option>')
    listingmin=listingmin[1:len(listingmin)-1]
    return listingmin
