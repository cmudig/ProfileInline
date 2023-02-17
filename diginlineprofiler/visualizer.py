#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Will Epperson.
# Distributed under the terms of the Modified BSD License.

"""
Visualizer module for widgets
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Dict, observe
import pandas as pd
from varname import argname
from ipylab import JupyterFrontEnd

from ._frontend import module_name, module_version
from .profile_lib import isNumeric, isTimestamp, isCategorical, getShape, \
    getColMeta, getValueCounts, getQuantBinnedData, getTempBinnedData, getTempInterval, \
    getQuantMeta, getStringMeta, getTemporalMeta
from .utils import convertVC, convertBinned

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
    exportedCode = Unicode('').tag(sync=True)

    # python only state
    dataframe = None
    app = JupyterFrontEnd()
    

    def __init__(self, dataframe: pd.DataFrame, *args, **kwargs):
        super(Visualizer, self).__init__(*args, **kwargs)

        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("dataframe must be a pandas DataFrame!")

        self.dataframe = dataframe
        dfName = argname('dataframe')
        self.calculateChartData(dfName)
    
    def calculateChartData(self, dfName: str):
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
                chartData = convertBinned(chartData, statistics["min"])

                cd["summary"]["quantMeta"] = statistics
                cd["summary"]["histogram"] = chartData
            elif isTimestamp(df[cName]):
                # get data
                vc, true_min = getTempBinnedData(df, cName, isIndex=False)
                interval = getTempInterval(df, cName, isIndex=False)
                temporalMeta = getTemporalMeta(df, cName, isIndex=False)

                # convert to JSON serializable
                histogram = convertBinned(vc, true_min)

                cd["summary"]["histogram"] = histogram
                cd["summary"]["timeInterval"] = interval
                cd["summary"]["temporalMeta"] = temporalMeta

            elif isCategorical(df[cName]):
                stringMeta = getStringMeta(df, cName)

                cd["summary"]["stringMeta"] = stringMeta
            
            colProfiles.append(cd)
    
        # This should be JSON serializable
        profile = {
            "profile": colProfiles,
            "shape": shape,
            "dfName": dfName,
            "lastUpdatedTime": 0,
            "isPinned": False,
            "warnings": []
        }
        # save profile to trailet to sync with frontend
        self.dfProfile = profile

    @observe('exportedCode')
    def _observe_exported_code(self, change):
        """
        Called when the exportedCode traitlet is changed, we add new code cell on a change
        """
        self.addNewCell(change['new'])
        self.exportedCode = ''
    
    def addNewCell(self, codeText):
        if codeText == '':
            return
        self.app.commands.execute('notebook:insert-cell-below')
        self.app.commands.execute('notebook:replace-selection', {'text': codeText})
