from modfunctions import *
import requests
#getting OIK names
pageforcrawling=requests.get('http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=show&root_a=784001001&vrn=2782000678445&region=78&global=null&type=0&sub_region=78&prver=0&pronetvd=0')
start=pageforcrawling.text.find('Нижестоящие избирательные комиссии')
end=pageforcrawling.text.find('</select>')
workingpage=pageforcrawling.text[start:end]
listing=workingpage.split('</option>')
listing=listing[1:27]
for i in range(0, len(listing)):
    listing[i]=listing[i].lstrip('<option value="')
    listing[i].find('"')
    listing[i]=listing[i] [0:(listing[i].find('"'))]
    listing[i]=listing[i].replace('amp;', '')

listingfin=[]
for k in range (len(listing)-1):
    listingfin.append(gettik(listing[k]))

codebooklist=[]

#getting codebook for each district, from the page of 0th UIK from 0th TIK for each district
for num_tik_row in range(len(listingfin)):
    codebooklist.append(reqvarnames(getpageuik(getlistuik(listingfin[num_tik_row][0])[0])))

###opening csv file for each OIK
for num_tik_row in range(len(listingfin)):
    filecsv=open("/home/aleksei/zakso_fptp/zakso_fptp_tab"+str(num_tik_row+1)+".csv", "w")

#writing variable names for each csv file
    for vlength in range(18):
        filecsv.write('v'+str(vlength+1)+',')
    for vlength in range(18, len(codebooklist[num_tik_row])):
        filecsv.write('v'+ str(vlength+1)+',' + 'v'+str(vlength+1)+'.1,')
    filecsv.write('\n')

#getting the data for each csv file
    try:
        for num_tik_col in range(len(listingfin[num_tik_row])):
            for j in range (len(getlistuik(listingfin[num_tik_row][num_tik_col]))):
                filecsv.write(reqdata(getpageuik(getlistuik(listingfin[num_tik_row][num_tik_col])[j])))
        firecsv.close()
    except Exception:
        continue

#writing each codebook in a separate file
for n in range(len(codebooklist)):
    file=open("/home/aleksei/zakso_fptp/zakso_fptp_codebook"+str(n+1)+'.txt', "w")
    for p in range(18):
        file.write('v'+str(p+1)+'-' + codebooklist[n][p]+'\n')
    for p in range(18, len(codebooklist[n])):
        file.write('v'+str(p+1)+' , v'+str(p+1)+'.1' + ' -'+codebooklist[n][p]+' (abs, %) '+'\n')
    file.close()
           

        

