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


class PCRasterAccutraveltimefluxAlgorithm(PCRasterAlgorithm):
    """
    Transports material downstream over a distance dependent on a given velocity.
    """

    INPUT_FLOWDIRECTION = 'INPUT'
    INPUT_MATERIAL = 'INPUT2'
    INPUT_VELOCITY = 'INPUT3'
    OUTPUT_FLUX = 'OUTPUT'
    OUTPUT_STATE = 'OUTPUT2'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAccutraveltimefluxAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'accutraveltimeflux'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('accutraveltimeflux and accutraveltimestate')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Transports material downstream over a distance dependent on a given velocity.

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_accutraveltime.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction in PCRaster LDD format (see lddcreate)
            * <b>Input material raster</b> (required) - Scalar raster with amount of material input (>= 0)
            * <b>Input velocity raster</b> (required) - Scalar raster with the distance per time step in map units (>=0)
            * <b>Output Flux raster</b> (required) - Scalar raster with result flux of material
            * <b>Output State raster</b> (required) - Scalar raster with result state of stored material
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_FLOWDIRECTION,
                self.tr('Input Flow Direction Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_MATERIAL,
                self.tr('Input Material Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_VELOCITY,
                self.tr('Input Velocity Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_FLUX,
                self.tr('Output Material Flux Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_STATE,
                self.tr('Output State Raster Layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                accutraveltimeflux,
                accutraveltimestate,
                report
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_flow_direction = self.parameterAsRasterLayer(parameters, self.INPUT_FLOWDIRECTION, context)
        input_material = self.parameterAsRasterLayer(parameters, self.INPUT_MATERIAL, context)
        input_velocity = self.parameterAsRasterLayer(parameters, self.INPUT_VELOCITY, context)
        setclone(input_flow_direction.dataProvider().dataSourceUri())
        ldd = readmap(input_flow_direction.dataProvider().dataSourceUri())
        material = readmap(input_material.dataProvider().dataSourceUri())
        transport_velocity = readmap(input_velocity.dataProvider().dataSourceUri())
        result_flux = accutraveltimeflux(ldd, material, transport_velocity)
        result_state = accutraveltimestate(ldd, material, transport_velocity)

        output_flux = self.parameterAsOutputLayer(parameters, self.OUTPUT_FLUX, context)
        output_state = self.parameterAsOutputLayer(parameters, self.OUTPUT_STATE, context)

        report(result_flux, output_flux)
        report(result_state, output_state)

        return {self.OUTPUT_FLUX: output_flux, self.OUTPUT_STATE: output_state}
