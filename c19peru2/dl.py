import pandas as pd
import urllib.request


def pivfiles(active,nactive,deaths,ndeath):
    urllib.request.urlretrieve(active, nactive)
    urllib.request.urlretrieve(deaths, ndeath)
    df = pd.read_csv(nactive, encoding = "ISO-8859-1", sep =';', engine='python')
   
        
    #df['DEPARTAMENTO'] = df['DEPARTAMENTO'].replace(['LIMA REGION'],'LIMA')
   
    
    df2 = pd.read_csv(ndeath, encoding = "ISO-8859-1",sep =';', engine='python')
    #df2['DEPARTAMENTO'] = df2['DEPARTAMENTO'].replace(['LIMA REGION'],'LIMA')
    
    # Adjusting the dates for active cases
    df['FECHA_RESULTADO'] = df['FECHA_RESULTADO'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

    #Adjusting the dates for number of deaths
    df2["FECHA_FALLECIMIENTO"] = df2['FECHA_FALLECIMIENTO'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
    
    
    #cyf = pd.merge(df,df2,on='UUID',how='outer',indicator=True)
    
    # uncomment if you want to fill up the blanks for gender.
    #cyf['SEXO'] = cyf['SEXO_x'].fillna("NOT RECORDED")	
    
    # fixing the merge column
    #cyf["_merge"] = cyf["_merge"].astype(str)
    
    # Active Cases By Department (overall, no dates)
    ADeptdf = df.pivot_table(values='UUID',index=['DEPARTAMENTO'], aggfunc=lambda x: x.count()).reset_index(level=0)
    #removing the axiss on the columns
    ADeptdf = ADeptdf.rename_axis(columns=None)
    ADeptdf  = ADeptdf.fillna(0)
    #Deptdf = Deptdf.reset_index()
    ADeptdf.columns = ["Department", "Active Cases"]
    
    #new_row = ADeptdf[( ADeptdf['Department'] == 'LIMA') | ( ADeptdf['Department'] == 'LIMA REGION')]['Active Cases'].sum()
    #ADeptdf = ADeptdf[( ADeptdf['Department'] != 'LIMA') | ( ADeptdf['Department'] != 'LIMA REGION')] 
    #ADeptdf.append({'Department':'LIMA'},{'Active Cases',new_row})
    
    # Dead by Department (overall, no Dates)
    DDeptdf = df2.pivot_table(values='UUID',index=['DEPARTAMENTO'], aggfunc=lambda x: x.count()).reset_index(level=0)
    #removing the axiss on the columns
    DDeptdf = DDeptdf.rename_axis(columns=None)
    DDeptdf  = DDeptdf.fillna(0)
    #Deptdf = Deptdf.reset_index()
    DDeptdf.columns = ["Department", "Deaths"]
    
    # Active and Deaths by Department (the Joint of these 2)
    Deptdf = pd.merge(ADeptdf,DDeptdf,on='Department',how='outer',indicator=False)
    
    #############
    # Active Cases by Department (with Dates)
    ActiveDeptdf = df.pivot_table(values='UUID',index=['FECHA_RESULTADO','DEPARTAMENTO'], aggfunc=lambda x: x.count()).reset_index(level=0)
    #removing the axiss on the columns
    ActiveDeptdf = ActiveDeptdf.rename_axis(columns=None)
    ActiveDeptdf  = ActiveDeptdf.fillna(0)
    ActiveDeptdf = ActiveDeptdf.reset_index()
    ActiveDeptdf.columns = ["Department", "Date", "Active Cases"]
    
    # Deaths by Department (with Dates)
    # Breakdown by Department (Active)
    DeadDeptdf = df2.pivot_table(values='UUID',index=['FECHA_FALLECIMIENTO','DEPARTAMENTO'], aggfunc=lambda x: x.count()).reset_index(level=0)
    #removing the axiss on the columns
    DeadDeptdf = DeadDeptdf.rename_axis(columns=None)
    DeadDeptdf  = DeadDeptdf.fillna(0)
    DeadDeptdf = DeadDeptdf.reset_index()
    DeadDeptdf.columns = ["Department", "Date", "Deaths"]
    
    
    #Distdf["Total"] = Distdf["Active Cases"] + Distdf["Deaths"]
    #Distdf = Distdf.reindex(['Department','District','Active Cases','Deaths','Total'], axis=1)

    return ActiveDeptdf.to_csv("ActivebyDept_with_Date.csv",index=False), Deptdf.to_csv("CasesbyDepartment.csv",index=False),DeadDeptdf.to_csv("Deaths_byDept_with_date.csv",index=False)
    
# testing if the function works
aa = "https://cloud.minsa.gob.pe/s/Y8w3wHsEdYQSZRp/download" #active
bb = "positivos_covid.csv" #name active
cc = "https://cloud.minsa.gob.pe/s/Md37cjXmjT9qYSa/download" #deaths
dd = "fallecidos_covid.csv"

pivfiles(aa,bb,cc,dd)
print("Completed")