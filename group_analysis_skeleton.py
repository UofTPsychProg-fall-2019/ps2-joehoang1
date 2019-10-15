#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os 
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename

# get file path directory
os.getcwd() # '/Users/joe/Documents/GitHub/ps2-joehoang1'

# copy files from different directories and renaming them
filepathA = os.path.join('testingroomA','experiment_data.csv')
newpath = os.path.join('rawdata','experiment_dataroomA.csv')
shutil.copyfile(filepathA,newpath)

filepathB = os.path.join('testingroomB','experiment_data.csv')
newpath = os.path.join('rawdata','experiment_dataroomB.csv')
shutil.copyfile(filepathB,newpath)

filepathC = os.path.join('testingroomC','experiment_data.csv')
newpath = os.path.join('rawdata','experiment_dataroomC.csv')
shutil.copyfile(filepathC,newpath)

# change path directory
os.chdir('/Users/joe/Documents/GitHub/ps2-joehoang1/rawdata')

## See next chunk
##data = np.empty((0,5))
##testingrooms = ['A','B','C']
##for room in testingrooms:
    ##filename = 'experiment_dataroom'+room+'.csv'
    ##print(filename)
    ##tmp = sp.loadtxt(filename,delimiter=',')
    ##data = np.vstack([data,tmp])
    


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT

data = np.empty((0,5))
testingrooms = ['A','B','C']
for room in testingrooms:
    filename = 'experiment_dataroom'+room+'.csv'
    print(filename)
    tmp = sp.loadtxt(filename,delimiter=',')
    data = np.vstack([data,tmp])

# Importing panda to create column names 
## import pandas as pd
## data = pd.DataFrame(data, columns = ['Subject', 'Stimulus', 'Pairing', 'Accuracy', 'Median RT'])

    
#%%
# calculate overall average accuracy and average median RT

acc_avg = np.average(data[:,3]) # 91.48%
print(acc_avg) #0.9147865812499999
mrt_avg = np.average(data[:,4]) 
print(mrt_avg) #477.3369565217391


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)

# finding the mean for accuracy by splitting by stimulus(words)
mean_accuracy1=0
total_accuracy1=0
count_accuracy1=0
for i in range(len(data)):
    if data[i,1] ==1:
        total_accuracy1+= data[i,3]
        count_accuracy1+=1
    mean_accuracy1=total_accuracy1/count_accuracy1
print(mean_accuracy1) #0.8855632761304347

# finding the mean for accuracy by splitting by stimulus(faces)
idx_accuracy2 = data[:,1] == 2
mean_accuracy2 = np.mean(data[idx_accuracy2, 3])
print(mean_accuracy2) #0.9440098863695653

# finding the mean for RT by splitting by stimulus (words)
mean_RT1=0
total_RT1=0
count_RT1=0
for i in range(len(data)):
    if data[i,1] ==1:
        total_RT1+= data[i,4]
        count_RT1+=1
    mean_RT1=total_RT1/count_RT1
print(mean_RT1) #489.3695652173913

# finding the mean for RT by splitting by stimulus (faces)
idxRT2 = data[:,1] == 2
mean_RT2 = np.mean(data[idxRT2, 4])
print(mean_RT2) #465.30434782608694 

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)

# Using indexing and splicing to get the split between white pleasant 
# and black pleasant faces
wp = data[:,2]==1
bp = data[:,2]==2

# Using only one line of code to calculate average for accuracy and RT
acc_wp =  np.mean(data[wp,3])
print(acc_wp) # 94.01758767173912%
acc_bp = np.mean(data[bp,3])  
print(acc_bp) # 88.93972857826087%
mrt_wp = np.mean(data[wp,4])# 
print(mrt_wp) # 469.5869565217391 ms
mrt_bp = np.mean(data[bp,4])  
print(mrt_bp) # 485.0869565217391 ms 

#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)

#Creating new arrays based off conditions
#Words and White Pleasant
w_wp = data[(data[:,2]==1) & (data[:,1] ==1)]
#Faces and White Pleasant
f_wp = data[(data[:,2]==1) & (data[:,1] ==2)]
#Words and Black Pleasant
w_bp = data[(data[:,2]==2) & (data[:,1] ==1)]
#Faces and White Pleasant
f_bp = data[(data[:,2]==2) & (data[:,1] ==2)]

#Calculating RT for conditions
# words - black/pleasant: 478.4ms
words_wp =  np.mean(w_wp[:,4])
print(words_wp)
# words - black/pleasant: 500.3ms
words_bp =  np.mean(w_bp[:,4])
print(words_bp)
# faces - white/pleasant: 460.8ms
faces_wp =  np.mean(f_wp[:,4])
print(faces_wp)
# faces - black/pleasant: 469.9ms
faces_bp =  np.mean(f_bp[:,4])
print(faces_bp)

#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats as stats

#T-test for words and pairing
stats.ttest_rel((w_wp[:,4]),(w_bp[:,4]))
# words: t=-5.36, p=2.19e-5
#Ttest_relResult(statistic=-5.363765065207133, pvalue=2.1935732392766215e-05)

#T-test for faces and pairing
stats.ttest_rel((f_wp[:,4]),(f_bp[:,4]))
#Ttest_relResult(statistic=-2.835330734415269, pvalue=0.009629538957921187)
# faces: t=-2.84, p=0.0096

#For the print-out
test1 = stats.ttest_rel((w_wp[:,4]),(w_bp[:,4]))
test2 = stats.ttest_rel((f_wp[:,4]),(f_bp[:,4]))


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print('\nWORDS ACCURACY AVG: {:.2f}%'.format(100*mean_accuracy1))
print('\nFACES ACCURACY AVG: {:.2f}%'.format(100*mean_accuracy2))
print('\nWORDS RT AVG: {:.1f} ms'.format(mean_RT1))
print('\nFACES RT AVG: {:.1f} ms'.format(mean_RT1))
print('\nWHITE PLEASANT ACCURACY AVG: {:.2f}%'.format(100*acc_wp))
print('\nBLACK PLEASANT ACCURACY AVG: {:.2f}%'.format(100*acc_bp))
print('\nWHITE PLEASANT RT AVG: {:.1f} ms'.format(mrt_wp))
print('\nBLACK PLEASANT RT AVG: {:.1f} ms'.format(mrt_bp))
print('\nWORDS + WHITE PLEASANT CONDITION RT AVG: {:.1f} ms'.format(words_wp))
print('\nWORDS + BLACK PLEASANT CONDITION RT AVG: {:.1f} ms'.format(words_bp))
print('\nFACES + WHITE PLEASANT CONDITION RT AVG: {:.1f} ms'.format(faces_wp))
print('\nFACES + BLACK PLEASANT CONDITION RT AVG: {:.1f} ms'.format(faces_bp))
print('\nT-TEST FOR WORDS + WHITE/BLACK PLEASANT CONDITION : t = {:.2f} , p = {:.4f} '.format(-5.36, 2.19e-5))
print('\nT-TEST FOR FACES + WHITE/BLACK PLEASANT CONDITION : t = {:.2f} , p = {:.4f} '.format(-2.84, 0.0096))


#%%
