#!/usr/bin/env python

import os
import sys
import re
import numpy as np
import pandas as pd

pjoin = os.path.join

class Prescaler():
    '''Compute prescale from given CSV files (brilcalc outputs)'''
    def __init__(self, trigger, year):
        self.trigger = trigger
        self.year = year
        self.inputdir = f'./input/{year}'

    def compute(self):
        '''Compute the prescale as a function of lumi.'''
        trigfile = pjoin(self.inputdir, f'{self.trigger}.csv')
        allfile = pjoin(self.inputdir, f'lumi_{self.year}.csv')
        
        headers_trig = [
            'run:fill','LumiSection','Time','HLT Path','delivered(/fb)','recorded(/fb)','avgpu','source'
        ]
        headers_all = [
            'run:fill','LumiSection','Time','Beam Status','E (GeV)','delivered(/fb)','recorded(/fb)','avgpu','source'
        ]

        df_trig = pd.read_csv(trigfile, delimiter=',', names=headers_trig, comment='#')[['run:fill', 'LumiSection', 'recorded(/fb)']]
        df_all = pd.read_csv(allfile, delimiter=',', names=headers_all, comment='#')[['run:fill', 'LumiSection', 'recorded(/fb)']]

        merged_df = df_trig.merge(df_all, on=['run:fill', 'LumiSection'], suffixes=('_trig', '_all'))
        
        # Compute prescale as a function of lumi section
        merged_df['Prescale'] = 1 / (merged_df['recorded(/fb)_trig'] / merged_df['recorded(/fb)_all'])
        return merged_df[['run:fill', 'LumiSection','Prescale']]

    def dump_to_csv(self, df):
        outdir = self.inputdir.replace('input','output')
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        outpath = pjoin(outdir, f'prescales_{self.trigger}.csv') 
        df.to_csv(outpath, index=False)

        print(f'Prescales saved at: {outpath}')

if __name__ == '__main__':
    p = Prescaler(
        trigger='HLT_PFJet40',
        year=2017
    )
    df = p.compute()
    p.dump_to_csv(df)