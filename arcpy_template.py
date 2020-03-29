"""Module summary.

Description sentence(s).

Alphabetical list of ArcPy functions:
https://pro.arcgis.com/en/pro-app/arcpy/functions/alphabetical-list-of-arcpy-functions.htm

"""

import arcpy
import os
import sys
import time
import logging

# import fire # Uncomment to make this a CLI program.

logger = logging.getLogger(__name__)


def setup_logging(level='INFO'):
    r"""Configures the logger Level.

    Arguments:
        level: CRITICAL -> ERROR -> WARNING -> INFO -> DEBUG.

    Side effect:
        The minimum logging level is set.
    """
    ll = logging.getLevelName(level)
    logger = logging.getLogger()
    logger.handlers.clear()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(name)-12s %(levelname)-8s"
        "{'file': %(filename)s 'function': %(funcName)s 'line': %(lineno)s}\n"
        "message: %(message)s\n")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(ll)


def pwd():
    wd = sys.path[0]
    logger.info('wd: {0}'.format(wd))
    return wd


def ls_fc():
    featureclasses = arcpy.ListFeatureClasses()
    logger.info('featureclasses: {0}'.format(featureclasses))
    return featureclasses


def output_name(input_name, suffix):
    output_name = '{0}{1}'.format(input_name, suffix)
    logger.info('output_name: {0}'.format(output_name))
    return output_name


def set_path(wd, data_path):
    path_name = os.path.join(wd, data_path)
    logger.info('path_name: {0}'.format(path_name))
    return path_name


def import_spatial_reference(dataset):
    spatial_reference = arcpy.Describe(dataset).SpatialReference
    logger.info('spatial_reference: {0}'.format(spatial_reference.name))
    return spatial_reference


def setup_env(workspace_path, spatial_ref_dataset):
    # Set workspace path.
    arcpy.env.workspace = workspace_path
    logger.info('workspace(s): {}'.format(arcpy.env.workspace))

    # Set output overwrite option.
    arcpy.env.overwriteOutput = True
    logger.info('overwriteOutput: {}'.format(arcpy.env.overwriteOutput))

    # Set the output spatial reference.
    arcpy.env.outputCoordinateSystem = import_spatial_reference(
        spatial_ref_dataset)
    logger.info('outputCoordinateSystem: {}'.format(
        arcpy.env.outputCoordinateSystem.name))


def check_status(result):
    """Function summary.

    Description sentence(s).
    Understanding message types and severity:
    https://pro.arcgis.com/en/pro-app/arcpy/geoprocessing_and_python/message-types-and-severity.htm

    Arguments:
        arg 1: Description sentence.
        arg 2: Description sentence.

    Returns:
        Description sentence.

    Raises:
        Description sentence.
    """
    status_code = dict([(0, 'New'), (1, 'Submitted'), (2, 'Waiting'),
                        (3, 'Executing'), (4, 'Succeeded'), (5, 'Failed'),
                        (6, 'Timed Out'), (7, 'Canceling'), (8, 'Canceled'),
                        (9, 'Deleting'), (10, 'Deleted')])

    logger.info('current job status: {0}-{1}'.format(
        result.status, status_code[result.status]))
    # Wait until the tool completes
    while result.status < 4:
        logger.info('current job status (in while loop): {0}-{1}'.format(
            result.status, status_code[result.status]))
        time.sleep(0.2)
    messages = result.getMessages()
    logger.info('job messages: {0}'.format(messages))
    return messages


def run_model(spatial_ref_dataset, ll='INFO'):
    setup_logging(ll)
    wd = pwd()
    input_path = set_path(wd, 'db_name')
    output_path = None
    setup_env(input_path, spatial_ref_dataset)


# python-fire requires: sys.stdin must be a terminal input stream
# jupyter sys.stdin.isatty(), is a terminal, is False or None depending on implementation
# must comment out fire.Fire() when running in jupyter environment
# Uncomment to make this a CLI program.
# if __name__ == '__main__':
#     fire.Fire()
