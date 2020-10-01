import pandas as pd
import urllib.request


def pivfiles(active,nactive,deaths,ndeath):
    urllib.request.urlretrieve(active, nactive)
    urllib.request.urlretrieve(deaths, ndeath)
    df = pd.read_csv(nactive, encoding = "ISO-8859-1", engine='python')
    df['DEPARTAMENTO'] = df['DEPARTAMENTO'].replace(['LIMA REGION'],'LIMA')
    df2 = pd.read_csv(ndeath, encoding = "ISO-8859-1", engine='python')
    df2['DEPARTAMENTO'] = df2['DEPARTAMENTO'].replace(['LIMA REGION'],'LIMA')
    
    
    cyf = pd.merge(df,df2,on='UUID',how='outer',indicator=True)
    
    cyf['FECHA_RESULTADO'] =  pd.to_datetime(cyf['FECHA_RESULTADO'])
    cyf['FECHA_FALLECIMIENTO'] = pd.to_datetime(cyf['FECHA_FALLECIMIENTO'])
    
    # uncomment if you want to fill up the blanks for gender.
    #cyf['SEXO'] = cyf['SEXO_x'].fillna("NOT RECORDED")	
    
    # fixing the merge column
    cyf["_merge"] = cyf["_merge"].astype(str)
    
    # Breakdown by Department
    Deptdf = cyf.pivot_table(values='UUID',index='DEPARTAMENTO_x',columns=['_merge'], aggfunc=lambda x: x.count()).reset_index(level=0)
    #removing the axiss on the columns
    Deptdf = Deptdf.rename_axis(columns=None)
    Deptdf  = Deptdf.fillna(0)
    # Changing the Name of the Columns
    Deptdf.columns = ["Department", "Deaths", "Active Cases"]
    # Adding the total number of cases
    Deptdf["Total"] = Deptdf["Active Cases"] + Deptdf["Deaths"]
    #re-ordering the columns
    Deptdf = Deptdf.reindex(['Department','Active Cases','Deaths','Total'], axis=1)
    
    #Pivoting Cities (same process as Deptdf)
    # Breakdown by District
    Distdf = cyf.pivot_table(values='UUID',index=['DEPARTAMENTO_x','DISTRITO_x'],columns=['_merge'], aggfunc=lambda x: x.count()).reset_index(level=0)
    #removing the axiss on the columns
    Distdf = Distdf.rename_axis(columns=None)
    Distdf  = Distdf.fillna(0)
    Distdf = Distdf.reset_index()
    Distdf.columns = ["District", "Department", "Deaths", "Active Cases"]
    Distdf["Total"] = Distdf["Active Cases"] + Distdf["Deaths"]
    Distdf = Distdf.reindex(['Department','District','Active Cases','Deaths','Total'], axis=1)

    return Distdf.to_csv("CasesbyDistrict.csv",index=False), Deptdf.to_csv("CasesbyDepartment.csv",index=False)
    

# testing if the function works
aa = "https://cloud.minsa.gob.pe/s/Y8w3wHsEdYQSZRp/download" #active
bb = "positivos_covid.csv" #name active
cc = "https://cloud.minsa.gob.pe/s/Md37cjXmjT9qYSa/download" #deaths
dd = "fallecidos_covid.csv"

pivfiles(aa,bb,cc,dd)
print("Completed")