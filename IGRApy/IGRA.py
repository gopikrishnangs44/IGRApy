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
        
