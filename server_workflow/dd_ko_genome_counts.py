 #!/Users/Dylan/anaconda3/bin/python
import pandas as pd
import sys
#-----------------------here is a script to compute counts of K0 terms per taxa after output from KoalaKO-----------------
#The output is in two files
#1) For possible downstream analyses in bash, python, or other pipelines. It is a pandas table with taxa, KO, protein # (from original AA conversion), and counts of KO terms within taxa
#2) For further analyses in R, a table that can be transformed with the reshape2 package

#Arguments are as follows:
#1) input user_ko.txt file
#2) output file 1
#3) output file 2

#You can do multiple files using echo parallel or other methods then combine outputs with double pipe in bashj
kofileout = str(sys.argv[1])

with open(kofileout,'r') as f:
	content = f.readlines()
	#only keep lines with K0 hits

res = [x for x in content if '\t' in x]
#remove new line character from strings
res2 = ([x.replace('\n','') for x in res])
#convert to dictionary (easier for making df)
resdict = dict(x.split('\t') for x in res2)
#make dataframe
df = pd.DataFrame(list(resdict.items()),columns = ['bacteria-proteinnum','K0'])
#split columns, taxa column and protein number column
df['protein_num'] = [x[-1] for x in df['bacteria-proteinnum'].str.split('-')]
df['taxa'] = ["-".join(str.split(x,"-")[0:-1]) for x in df['bacteria-proteinnum']]
#drop old combined column
df = df.drop('bacteria-proteinnum', 1)
#Calculate counts of unique KO
df['freq'] = df.groupby(['taxa','K0'])['K0'].transform('count')
df.to_csv(str(sys.argv[2]))

#Also write one for R where we can do this seperately using the reshape2 package
dfR = df.drop('freq', 1)
dfR = dfR.drop('protein_num', 1)
dfR.to_csv(str(sys.argv[3]))


