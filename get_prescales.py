#!/usr/bin/env python

import os
import sys
import re
import numpy as np
import pandas as pd

from tqdm import tqdm
from matplotlib import pyplot as plt

pjoin = os.path.join

def plot_prescales(trigger, year):
    df = pd.read_csv(f'./output/{year}/prescales_{trigger}.csv')
    prescales = df['Prescale']
    fig, ax = plt.subplots()
    ax.hist(prescales)

    ax.set_xlabel('Prescale')
    ax.set_ylabel('Lumi-section Counts')
    ax.set_title(trigger)
    
    ax.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    outdir = './plots'
    try:
        os.makedirs(outdir)
    except FileExistsError:
        pass
    
    outpath = pjoin(outdir, f'{trigger}.pdf')
    fig.savefig(outpath)
    plt.close(fig)

if __name__ == '__main__':
    trigger_list = [
        'HLT_PFJet40',
        'HLT_PFJet60',
        'HLT_PFJet80',
        'HLT_PFJet140',
    ]
    year=2017
    for trigger in tqdm(trigger_list):
        plot_prescales(trigger, year)
