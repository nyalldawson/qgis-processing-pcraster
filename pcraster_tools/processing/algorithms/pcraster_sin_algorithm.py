# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRastersinAlgorithm(PCRasterAlgorithm):
    """
    Sine
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRastersinAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'sin'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('sin')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Mathematical operators')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'operators'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Sine

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_sin.html">PCRaster documentation</a>

            Parameters:

            * <b>Input raster</b> (required) - directional or scalar raster layer
            * <b>Output raster</b> (required) - sine result layer with data type of input raster
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Directional or Scalar Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output Sine layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                sin
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        sinLayer = sin(InputRaster)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(sinLayer, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
