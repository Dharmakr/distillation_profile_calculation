import numpy as np

from common_lib import commons
import argparse


def main(args):
    # Retrieve the distillation profile
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
    parser = argparse.ArgumentParser(description='Distillation parser argument parser')
    parser.add_argument('--crudeone', required=True, type=str, help='provide the name for crude one')
    parser.add_argument('--crudetwo', required=True, type=str, help='provide the name for crude two')
    parser.add_argument('--outfile', required=True, type=str, help='output file to write the distillation profile')
    args = parser.parse_args()

    main(args)
