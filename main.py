import sys

import numpy as np
import logging

from common_lib import commons
import argparse


def init_logger():
    logger = logging.getLogger('Distillationprofileapp')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def main(args):
    logger = init_logger()
    # Retrieve the distillation profile
    logger.info("Processing the Distillation profile calculation program")
    df_crude_one = commons.retrieve_distillation_profile(args.crudeone)
    df_crude_two = commons.retrieve_distillation_profile(args.crudetwo)

    # Replace missing values with NaN
    df_crude_one = df_crude_one.replace('-', np.nan)
    df_crude_two = df_crude_two.replace('-', np.nan)

    # process the distillation profile for mixture of crude
    # the calculate_distillation_profile function will return the distillation profile as dataframe
    df_crude_mixture = commons.calculate_distillation_profile(df_crude_one, df_crude_two)
    df_crude_mixture.to_csv(args.outfile, index=False)


if __name__ == '__main__':
    # Configure argument parser
    parser = argparse.ArgumentParser(description='Distillation parser argument parser')
    parser.add_argument('--crudeone', required=True, type=str, help='provide the name for crude one')
    parser.add_argument('--crudetwo', required=True, type=str, help='provide the name for crude two')
    parser.add_argument('--outfile', required=True, type=str, help='output file to write the distillation profile')
    args = parser.parse_args()

    main(args)
