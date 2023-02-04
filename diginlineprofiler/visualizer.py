#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Will Epperson.
# Distributed under the terms of the Modified BSD License.

"""
Visualizer module for widgets
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Integer, Dict, List
from ._frontend import module_name, module_version

import pandas as pd
from .profile_lib import isNumeric, isTimestamp, isCategorical, isBoolean, getColumns, getShape, \
    getQuantMeta, getColMeta, getValueCounts, getQuantBinnedData, getTempBinnedData, getTempInterval, \
    getStringStats

from .utils import convertVC, convertQMeta, convertBinned

class Visualizer(DOMWidget):
    # boilerplate for ipywidgets syncing
    _model_name = Unicode('VizualizerModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('VizualizerView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    # our synced traitlet state
    dfProfile = Dict({}).tag(sync=True)

    # python only state
    dataframe = None

    def __init__(self, dataframe, *args, **kwargs):
        super(Visualizer, self).__init__(*args, **kwargs)

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Dataframe must be a pandas DataFrame!")

        self.dataframe = dataframe
        self.calculateChartData()
    
    def calculateChartData(self):
        # get columns and check that all names are unique
        df = self.dataframe
                
        if df.columns.nunique() != len(df.columns):
            raise ValueError("Column names are not unique!")
        
        shape = getShape(self.dataframe)
        colProfiles = []

        # Get data for each column
        for cName in df.columns:
            vc = getValueCounts(df, cName, isIndex=False)
            num_unique, num_null = getColMeta(df, cName, isIndex=False)

            cd = {
                "name": cName,
                "type": str(df[cName].dtype),
                "isIndex": False,
                "summary": {
                    "cardinality": num_unique,
                    "topK": convertVC(vc, cName) # TODO this might not be right type
                },
                "nullCount": num_null,
                "example": vc.index[0]
            }


            if isNumeric(df[cName]):
                # get data
                chartData = getQuantBinnedData(df, cName, isIndex=False)
                statistics = getQuantMeta(df, cName, isIndex=False)
                # convert to JSON serializable
                statistics = convertQMeta(statistics)
                chartData = convertBinned(chartData, statistics["min"])

                cd["summary"]["statistics"] = statistics
                cd["summary"]["histogram"] = chartData
            elif isTimestamp(df[cName]):
                # get data
                vc, true_min = getTempBinnedData(df, cName, isIndex=False)
                interval = getTempInterval(df, cName, isIndex=False)

                # convert to JSON serializable
                histogram = convertBinned(vc, true_min)

                cd["summary"]["histogram"] = histogram
                cd["summary"]["timeInterval"] = interval

            elif isCategorical(df[cName]):
                minLength, maxLength, meanLength = getStringStats(df, cName)

                cd["summary"]["stringSummary"] = {
                    "minLength": minLength,
                    "maxLength": maxLength,
                    "meanLength": meanLength
                }
            
            colProfiles.append(cd)
    
        # This should be JSON serializable
        profile = {
            "profile": colProfiles,
            "shape": shape,
            "dfName": "testNameDude",
            "lastUpdatedTime": 0,
            "isPinned": False,
            "warnings": []
        }
        # TODO save profile to trailet to sync with frontend
        self.dfProfile = profile


        




