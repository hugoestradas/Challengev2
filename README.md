# Solution for PythonPatentChallenge

## Installation
- Create an environment with the packages in 'requeriments.txt'.

## Usage
- Execute 'solution.py' (use relative paths from current working directory):

  ```python solution.py Data/inputfile.csv Data/outputfile.csv```

## Explanation of solution
- The suffixes list is static, as per the problem statement.
- Official names are extracted from the data.
- Official names are assumed to correspond to those with the most occurrences in the data.
- Official names are added to the mapper based on comparisons of the name, city, and country.
- Orthographic comparisons are calculated using the fuzzywuzzy library.
- The threshold was determined empirically.

## Ways to improve solution
- Do not assume that the correct names are those with the most occurrences. Instead, create functionality for names specified by the user.
- Do not set the threshold empirically. Instead, create a model that can tune itself.
- Do not assume that there are no different combinations of city, country, and company. Instead, expand the functionality to accept different variations.
