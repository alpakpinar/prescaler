#!/usr/bin/env python

import os
import sys
import re
import csv
import numpy as np
import pandas as pd

from tqdm import tqdm
from matplotlib import pyplot as plt

pjoin = os.path.join

def compute_average_prescale(trigger, year, writer):
    '''Compute average prescale for each trigger.'''
    infile = f'./output/{year}/prescales_{trigger}.csv'
    df = pd.read_csv(infile)

    mean_ps = df['Prescale'].mean()

    writer.writerow([trigger, '{:.3f}'.format(mean_ps)])


if __name__ == '__main__':
    trigger_list = [
        'HLT_PFJet40',
        'HLT_PFJet60',
        'HLT_PFJet80',
        'HLT_PFJet140',
        'HLT_PFJet200',
        'HLT_PFJet260',
        'HLT_PFJet320',
        'HLT_PFJet400',
        'HLT_PFJet500',
        'HLT_PFJet550',
    ]
    year=2017

    outdir = f'./output/{year}'
    try:
        os.makedirs(outdir)
    except FileExistsError:
        pass

    outpath = pjoin(outdir, 'average_prescales.csv')
    with open(outpath, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['Trigger Name',  'Average Prescale'])
        for trigger in tqdm(trigger_list):
            compute_average_prescale(trigger, year, writer)
