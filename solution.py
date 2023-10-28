import argparse
import regex as re
import pandas as pd
from collections import Counter
from fuzzywuzzy import fuzz

#%% Constants
sfxList = [' INC', ' LLC', ' LTD', ' LLP', ' PC', ' KKC']#Only the ones in the data according to problem statement

#%% Defining functions
#Removing special characters
def cleanSC(x):
    x = x.strip()
    sc = r"[^A-Za-z0-9\s]"#Only alphanumeric and spaces
    x = re.sub(sc,"",x)
    multSpace = r"[\s]{2,}"
    x = re.sub(multSpace," ",x)#Removing multiple consecutive spaces
    return x

#Removing sufixes
def removeSufixes(x, sfxList):
    for s in sfxList:
        tpattern = r'({}$)'.format(s)#Remove sufixes only at the end
        x = re.sub(tpattern,"",x)
    return x

#Sorting by frequency
def mostRepeatedNames(names):
    print("Counting ocurrences...")
    freqs = Counter(names)
    mrNames = sorted(freqs.keys(), key=lambda x: freqs[x], reverse=True)
    return mrNames

def maperCreator(df, threshold):
    mrNames = mostRepeatedNames(df['fixed_name'])
    mapper = {}
    print("Creating mapper based on most repeated names and similarity threshold...")
    for name in mrNames:
        if name not in mapper:
            city_name = df[df['fixed_name']==name]['city'].value_counts().idxmax()#Getting most common city for current name
            country_name = df[df['fixed_name']==name]['country'].value_counts().idxmax()#Getting most common city for current name
            for index, row in df.iterrows():
                nameSimilarity = fuzz.ratio(name, row['fixed_name'])# Calculating orthographic similarity.
                citySimilarity = fuzz.ratio(city_name, row['city'])# Calculating orthographic similarity.
                if ((nameSimilarity > threshold) & (country_name==row['country']) & (citySimilarity >threshold)):#Comparing 3 interest columns
                    mapper[row['fixed_name']] = name
    return mapper

def cleaningCompanyN(df,threshold):
    #Basic cleaning of comany name
    df['fixed_name'] = df['organization'].apply(lambda x: cleanSC(x))
    df['fixed_name'] = df['fixed_name'].apply(lambda x: removeSufixes(x, sfxList))
    #Cleaning city column
    df['city'] = df['city'].fillna('')#Filling nans with empty string
    df['city'] = df['city'].apply(lambda x: cleanSC(x))
    #Creating maper from bad to correct names
    canonical_companies = maperCreator(df, threshold)
    print("Aplying mapper...")
    df['fixed_name'] = df['fixed_name'].map(canonical_companies)
    return df

def get_args():
    parser = argparse.ArgumentParser(description='Cleaning company names')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('output', help='Output file path')
    return parser.parse_args()

if __name__ == '__main__':
    threshold = 85#Threshold for similarity
    args = get_args()
    df = pd.read_csv(args.input)
    df = cleaningCompanyN(df, threshold)
    print("Unique company names after normalization:\n", df['fixed_name'].unique())
    df.to_csv(args.output, index=False)

