Module mergait.stats
====================
Statistics helper-functions

Functions
---------

    
`autocorrelate(data, unbiased=True)`
:   Compute the autocorrelation for given data.
    
    Parameters
    ----------
    data : list
        The data to compute the autocorrelation for
    unbiased : bool
        Whether the biased or unbiased autocorrelation should be computed.
        The biased version tapers off with lag, while the unbiased version does not.
    
    Returns
    -------
    list
        List of autocorrelation values with 0 and positive lags

    
`iqr(values, percentiles=[75, 25])`
:   Compute the inter-quartile range. This is the (default) window in which half of the datapoints reside.
    The iqr is to the median, what the standard deviation is to the mean.
    
    Parameters
    ----------
    values : list
        data to compute the iqr for
    percentiles : list
        2-list with the top and bottom percentile
    
    Returns
    -------
    float
        the iqr value for the given data

    
`mae(values, cmp=0)`
:   Mean Absolute Error-like value for a given fixed mean
    (often 0 if we compare the value to a desired symmetry value of 0)
    
    Parameters
    ----------
    values : list
        data
    cmp : float
        expected outcome value in the sample
    
    Returns
    -------
    float
        the error value

    
`rmse(values, cmp=0)`
:   Root Mean Square Error-like value for a given fixed mean
    (often 0 if we compare the value to a desired symmetry value of 0)
    
    Parameters
    ----------
    values : list
        data
    cmp : float
        expected outcome value in the sample
    
    Returns
    -------
    float
        the error value