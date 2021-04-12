""" Symmetry related functions

These functions analyse data for extracting symmetry information
"""

import pandas as pd
import numpy as np
from mergait.bouts import *


def merge_left_right_data(df,
                          foot_column='foot',
                          feet=['left', 'right'],
                          tolerance=pd.Timedelta(1.0, unit='s'),
                          side='both'):
    '''
    Merge left and right foot data into a single gait cycle dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing data for both feet
    foot_column : str
        The column containing the foot
    feet : list
        Optional the two list indicating the label of the left and right foot in the data
    tolerance : pandas.Timedelta
        The optional maximum time between a step and the next step to be considered part of the same gait cycle
    side : str
        Whether to combine only the combination left-foot->right-foot 'left', right-foot->left-foot 'right', 
        or both sides of the gait cycle 'both'

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the merged left and right foot data
    '''
    df_left = df[df[foot_column] == feet[0]]
    df_right = df[df[foot_column] == feet[1]]

    df_merged = pd.DataFrame([])

    if side == 'left' or side == 'both':
        df_both = pd.merge_asof(df_left,
                                df_right,
                                on="t",
                                suffixes=['_left', '_right'],
                                tolerance=tolerance)
        df_both['initial_foot'] = feet[0]
        df_merged = df_merged.append(df_both)
    if side == 'right' or side == 'both':
        df_both = pd.merge_asof(df_right,
                                df_left,
                                on="t",
                                suffixes=['_right', '_left'],
                                tolerance=tolerance)
        df_both['initial_foot'] = feet[1]
        df_merged = df_merged.append(df_both)

    df_merged.sort_values(by='t', inplace=True)
    df_merged.reset_index(drop=True, inplace=True)
    df_merged.drop(columns=['foot_left', 'foot_right'], inplace=True)

    # annotate unusuable data
    df_merged['bad_half_step'] = df_merged.isna().any(axis=1)

    return df_merged


def append_symmetry_index(df,
                          columns=None,
                          compare_suffix=['_left', '_right'],
                          method='wusi'):
    '''
    Append a symmetry index column for all left/right columns given a particular symmetry index
    method as summarized in [Alves, 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7644861/).

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing columns with left and right data
    compare_suffix : list[str]
        Optional 2-list containing the suffix for the left and right data columns
    method : str
        One of the symmetry methods described in (Alves, 2020).
        'si' : Symmetry Index, is not officially defined for negative values
        'sa' : Symmetry Angle
        'usi' : Universal Symmetry Index, which does allow negative values
        'wusi' : Weighted Universal Symmetry Index, which corrects for the vanishing symmetry for small data values

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the appended symmetry columns suffixed by the method name

    '''
    df = df.copy()

    # detect columns to merge
    features = [
        c.replace(compare_suffix[0], '')
        for c in filter(lambda column: column.find(compare_suffix[0]) > -1,
                        df.columns.values)
    ]
    if not (columns is None):
        features = columns

    for a in features:
        L = df[a + compare_suffix[0]]
        R = df[a + compare_suffix[1]]

        phi = np.arctan2(1, L / R)

        if method == 'si':
            df[a + '_' + method] = (np.cos(phi) - np.sin(phi)) / (np.cos(phi) +
                                                                  np.sin(phi))
        elif method == 'sa':
            df[a + '_' + method] = [
                (1. / 2. - 2 / np.pi * phi_) if phi_ < 3. / 4. * np.pi else
                ((-1 + 2 / np.pi * phi_) if phi_ < 7. / 4. * np.pi else
                 (1 - 2 / np.pi * phi_)) for phi_ in phi
            ]
        elif method == 'usi':
            df[a + '_' + method] = np.cos(phi) - np.sin(phi)
        elif method == 'wusi':
            sigma = np.max([L.dropna().values.std(), R.dropna().values.std()])
            W = 1 - np.sqrt(2) * sigma / np.sqrt(2 * sigma**2 + L**2 + R**2)
            df[a + '_' + method] = W * (np.cos(phi) - np.sin(phi))

    return df
