""" Final Project - create a column schedule from a structural model with exported CSV """

# Import packages
import pandas as pd
import numpy as np
import math
import sqlite3
from openpyxl.styles import Alignment
import openpyxl

# SQL Query
conn = None
try:
    conn = sqlite3.connect("lateral_data_extractor.db") # TODO create prompt for this
except:
    print("error")

query = """
SELECT a.Column_Num, a.Story_Label, a.x1, a.y1, a.z1, a.Size, a.Grid_Label, b.Load_Case_Symbol, b.Axial1
FROM ColumnData AS a
JOIN MemberForcesTable AS b
ON a.Column_UID = b.Member_UID
AND a.Column_Num = b.Member_Num
ORDER BY Column_Num;
"""
df = pd.read_sql(query, conn)


# clean up raw dataframe
df.columns = ['col_num', 'story', 'x', 'y', 'z', 'size', 'coord', 'lc', 'axial']
df['axial'] = df['axial'].astype(float).round(decimals=1)
# df.head(15)


# gravity load combinations
grav_df = df.loc[(df.lc == "D") | (df.lc == "LP")]

pu_grav_df = grav_df.pivot_table(index=['story', 'col_num', 'coord', 'size'],
                                 columns='lc',
                                 values='axial').reset_index()
pu_grav_df['Pu'] = pu_grav_df.apply(lambda x: round(max(1.4 * x.D, 1.2 * x.D + 1.6 * x.LP ), 0), axis =1)
pu_grav_df = pu_grav_df.drop(['D', 'LP'], axis=1).sort_values(by=['coord', 'story'])
pu_grav_df.head()


# read in the columndesignsummary.csv
# this is kind of janky still b/c bentley's csv is not formatted correctly
# some manual adjustments were required on the raw csv file

# TODO create prompt for selecting csv file
cds = pd.read_csv('/Users/danki/edu/cs50/coldesignsummary.csv', sep=',', 
                  header=0, skiprows=2, error_bad_lines=False)
cds.dropna(axis=0, how='any',inplace=True)
cds.drop_duplicates(keep=False, inplace=True)
cds.drop(columns=['  Rho %', ' Ld/Cap', ' Transverse', '  Ld/Cap'], inplace=True)
cds = cds.rename(columns={' No.': 'col_num', '  Level': 'story', 
                    '  Section':'size', "  f'c": "f_c", ' Longitudinal':'rebar'})
cds = cds.astype({'col_num':'int64'})
cds.head()


# join pu_grav_df with cds on story and col_num
grav_sched = pu_grav_df.merge(cds, on=['story', 'col_num', 'size'])
#grav_sched.head()


# reshape to standard column schedule
grav_sched = grav_sched.pivot(index='story', columns='coord', values=['Pu','size','rebar'])

grav_sched = grav_sched.stack(level=[0]).sort_values(by='story', ascending=False).fillna('-')
grav_sched


# export to Excel

# prompt user for file name and path
filename = input("Enter File Name: ") # must include ".xlsx
filepath = input("Enter File Path: ") # e.g. /Users/danki/edu/cs50/

# write to excel
xlsx = grav_sched.to_excel(filepath+filename, sheet_name='Grav_Sched')

# center text in cell (NOT WORKING)
#wb = openpyxl.load_workbook(filepath+filename)
#lignment=Alignment(horizontal='center', vertical='center')

