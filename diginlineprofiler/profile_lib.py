"""
Utility functions for calculating metadata from pandas dataframes
These are called from PythonExecutor.ts in the frontend
"""

import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_bool_dtype, is_categorical_dtype, is_datetime64_dtype


####### type checks #######
def isNumeric(colData: pd.Series):
    return is_numeric_dtype(colData)

def isTimestamp(colData: pd.Series):
    return is_datetime64_dtype(colData)

def isCategorical(colData: pd.Series):
    return is_categorical_dtype(colData) or is_string_dtype(colData)

def isBoolean(colData: pd.Series):
    return is_bool_dtype(colData)

######## Analysis functions #######
def getColumns(dfName: pd.DataFrame):
    typeDF = dfName.dtypes.reset_index().rename(columns={"index": "colName", 0: "type"})
    typeDF["isIndex"] = False
    if dfName.index.name:
        name = dfName.index.name
    else:
        name = ""
    indexDF = pd.DataFrame({"colName": [name], "type": [dfName.index.dtype]})
    indexDF["isIndex"] = True
    typeDF = pd.concat([indexDF, typeDF])
    return typeDF

def getShape(dfName: pd.DataFrame):
    return dfName.shape

def getQuantMeta(dfName: pd.DataFrame, colName: str, isIndex=False):
    if isIndex:
        colData = dfName.index.to_series()
    else:
        colData = dfName[colName]
    m = colData.describe()
    return m

def getColMeta(dfName: pd.DataFrame, colName: str, isIndex=False):
    if isIndex:
        colData = dfName.index.to_series()
    else:
        colData = dfName[colName]
    num_unique = colData.nunique()
    num_null = colData.isna().sum()

    return num_unique, num_null

def getValueCounts(dfName: pd.DataFrame, colName: str, n=10, isIndex=False):
    if isIndex:
        colData = dfName.index.to_series()
    else:
        colData = dfName[colName]
    vc = colData.value_counts().iloc[:n]
    return vc

def getQuantBinnedData(dfName: pd.DataFrame, colName: str, n=20, isIndex=False):
    if isIndex:
        colData = dfName.index.to_series()
    else:
        colData = dfName[colName]
    vc = colData.value_counts(bins=min(n, colData.nunique()), sort=False)
    return vc

def getTempBinnedData(dfName: pd.DataFrame, colName: str, n=200, isIndex=False):
    if isIndex:
        colData = dfName.index.to_series()
    else:
        colData = dfName[colName]
    vc = (colData.astype("int64")//1e9).value_counts(bins=min(n, colData.nunique()), sort=False)
    true_min = (colData.astype("int64")//1e9).min()
    return vc, true_min

def getTempInterval(dfName: pd.DataFrame, colName: str, isIndex=False):
    if isIndex:
        colData = dfName.index.to_series()
    else:
        colData = dfName[colName]
    timerange = colData.max() - colData.min()
    return timerange.days

# def getVariableNamesInPythonStr(codeString: str):
#     import tokenize, io
#     print(set([ t.string for t in tokenize.generate_tokens(io.StringIO(codeString).readline) if t.type == 1]))

def getStringStats(dfName: pd.DataFrame, colName: str):
    lengths = dfName[colName].str.len()
    return lengths.min(), lengths.max(), lengths.mean()
