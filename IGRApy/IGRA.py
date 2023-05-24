import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

def igra(file_dir, stat=[], save='', save_dir='' ):
    if save==True:
        for stat in stat:
            a = pd.read_csv(file_dir, delim_whitespace=True, header=None, index_col=0)
            station = stat
            df1 = a[a.index==station]
            jj, pp = [], []
            for hh in [9999,1000,925,850,700,500,400,300,250,200,150,100]:
                lev = [hh]   
                try:
                    df2 = df1[df1[3] == lev[0]]
                    for i,j in zip(df2[1],df2[2]):
                        dat = pd.to_datetime(''+str(i)+''+str(j).zfill(2)+'', format='%Y%m')
                        pp.append(dat)
                    date = pd.to_datetime(pp)
                    m0 = pd.date_range(pp[0], pp[len(pp)-1], freq='MS')
                    dfa =  pd.DataFrame(df2[4]).set_index(date)
                    dfa1 = dfa.set_index(date).asfreq('MS').reset_index()
                    q1 = xr.DataArray(pd.DataFrame(dfa1[4]),  coords=[ m0,lev], dims=['time','lev'])
                    jj.append(q1)
                except:
                    dummy_date = pd.date_range('01-01-1950','01-01-2022')
                    myArr = np.empty((len(dummy_date),1))
                    q1_masked = xr.DataArray(myArr, coords=[dummy_date, lev], dims=['time','lev'])
                    jj.append(q1_masked)
                pp = []
            c = xr.combine_by_coords(jj)
            jj = []
            c.to_netcdf(''+str(save_dir)+''+str(df2.index[0])+'.nc')
        return c
    else:
        if save==None:
            for stat in stat:
                a = pd.read_csv(file_dir, delim_whitespace=True, header=None, index_col=0)
                station = stat
                df1 = a[a.index==station]
                jj, pp = [], []
                for hh in [9999,1000,925,850,700,500,400,300,250,200,150,100]:
                    lev = [hh]   
                    try:
                        df2 = df1[df1[3] == lev[0]]
                        for i,j in zip(df2[1],df2[2]):
                            dat = pd.to_datetime(''+str(i)+''+str(j).zfill(2)+'', format='%Y%m')
                            pp.append(dat)
                        date = pd.to_datetime(pp)
                        m0 = pd.date_range(pp[0], pp[len(pp)-1], freq='MS')
                        dfa =  pd.DataFrame(df2[4]).set_index(date)
                        dfa1 = dfa.set_index(date).asfreq('MS').reset_index()
                        q1 = xr.DataArray(pd.DataFrame(dfa1[4]),  coords=[ m0,lev], dims=['time','lev'])
                        jj.append(q1)
                    except:
                        dummy_date = pd.date_range('01-01-1950','01-01-2022')
                        myArr = np.empty((len(dummy_date),1))
                        q1_masked = xr.DataArray(myArr, coords=[dummy_date, lev], dims=['time','lev'])
                        jj.append(q1_masked)
                    pp = []
                c = xr.combine_by_coords(jj)
                jj = []
            return c
        
def plot_fig(var):
    plt.figure(figsize=(12,4), dpi=200)
    var.T.plot(cmap='jet', ylim=(1000,100))
    plt.show()

def RH(temp,vapr):
    temp1, vapr1 = temp/10, vapr/1000
    es = 6.112*np.exp((17.62*temp1)/(temp1+243.12))
    return vapr1/(es)*100

def SH(vapr):
    return 0.622*(vapr/vapr.lev)
        
    
def igra_stn(fil, yr1, yr2, stn_no):
    a = pd.read_csv(fil, header=None)
    s = []
    fi = 'INSTANT/por/INM000'+str(stn_no)+'-data.txt'
    file = open(''+str(fi)+'','r')
    for yr in range(yr1,yr2):
        for line in file:
            if line.startswith('#INM000'+str(stn_no)+' '+str(yr)+''):
                s.append(line.strip())
    print('s done')

    s1 = []
    for lookup in s:
        with open(''+str(fi)+'') as myFile:
            for num, line in enumerate(myFile, 1):
                if lookup in line:
                    #print(num)
                    s1.append(num)
    print('s1 done')

    s2 = []
    for i in range(0,len(s1)-1):
        a1 = a.iloc[s1[i]:s1[i+1]-1,:]
        s2.append(a1)
    print('s2 done')

    temp, pres, se = [],[],[]
    for i in range(len(s2)):
        dt = pd.Timestamp(''+str(s[i][13:17])+''+str(s[i][18:20])+''+str(s[i][21:23])+''+str(s[i][24:26])+'00')
        #print(i,dt)
        for j in range(len(s2[i][0])):
            pres.append(float(str(s2[i].iloc[j])[14:20])/100)
            temp.append(float(str(s2[i].iloc[j])[27:32])/10)
        daa = xr.DataArray(temp, coords=[pres], dims=['pres'], name='temp')
        daa1 = daa.where(daa!=-999.9, np.nan)#.sel(pres=slice(pres[0], 100))#.interp(pres=lev)
        dt1 = pd.to_datetime(dt)
        daa2 = daa1.assign_coords(time=dt1)
        daa2 = daa2.drop_duplicates(dim='pres', keep='first')
        se.append(daa2)
        temp,pres=[],[]
    data = xr.concat(se, dim='time').T
    return data
