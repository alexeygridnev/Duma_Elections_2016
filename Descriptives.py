import pandas
import os

def region_corr(filename):
    f=open(filename)
    dfreg=pandas.read_csv(f)
    dfreg['turnout']=(dfreg['v5']+dfreg['v6'])/dfreg['v2']*100
    dfreg['take_home']=dfreg['v6']/(dfreg['v5']+dfreg['v6'])*100
    dfreg['ER']=dfreg['v23.1']
    dfreg['LDPR']=dfreg['v26.1']
    dfreg['KPRF']=dfreg['v31.1']
    dfreg['SR']=dfreg['v33.1']
    dfreg['Yabloko']=dfreg['v30.1']

    df_fin=dfreg[['ER','LDPR', 'KPRF', 'SR', 'Yabloko', 'turnout', 'take_home']]
    return df_fin
    

path='/home/aleksei/Документы/SNS-related files/SNS_Studies/Python/All_Russia_2016PR/All_Russia_2016PR'
endfile=open('Correlations.csv', "w")
endfile.write('Region,ER,LDPR,KPRF,SR,Yabloko,turnout,take_home\n')

file_names_excl=tuple(['FINAL','Corr'])

for entry in os.scandir(path):
    if entry.is_file() and entry.name.endswith('.csv') and not entry.name.startswith(file_names_excl):
        print(entry.name)
        print(region_corr(entry.name).corr())
        print('\n')
        
        df=pandas.read_csv(entry.name)
                
        
        df['turnout']=(df['v5']+df['v6'])/df['v2']*100 #явка
        df['take_home']=df['v6']/(df['v5']+df['v6'])*100 #надомники

        #в целом по России: 
        ER=df['v23.1'].mean()
        LDPR=df['v26.1'].mean()
        KPRF=df['v31.1'].mean()
        SR=df['v33.1'].mean()
        Yabloko=df['v30.1'].mean()
        
        turnout=df['turnout'].mean()
        take_home=df['take_home'].mean()
        

        linedata=entry.name.rstrip(' PR.csv')+','
        linedata=linedata+str(ER)+','+str(LDPR)+','+str(KPRF)+','+str(SR)+','+str(Yabloko)+','+str(turnout)+','+str(take_home)+'\n'

        ##print(linedata)
        endfile.write(linedata)
endfile.close()
       
dfnew=pandas.read_csv('Correlations.csv')
print(dfnew.corr())
##



        

        
        
                

       
