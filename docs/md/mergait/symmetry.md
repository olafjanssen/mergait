Module mergait.symmetry
=======================
Symmetry related functions

These functions analyse data for extracting symmetry information

Functions
---------

    
`append_symmetry_index(df, columns=None, compare_suffix=['_left', '_right'], method='wusi')`
:   Append a symmetry index column for all left/right columns given a particular symmetry index
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

    
`merge_left_right_data(df, foot_column='foot', feet=['left', 'right'], tolerance=Timedelta('0 days 00:00:01'), side='both')`
:   Merge left and right foot data into a single gait cycle dataset.
    
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