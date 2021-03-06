technical -- Technical indicators
=================================

.. module:: pyalgotrade.technical
.. autoclass:: pyalgotrade.technical.DataSeriesFilter
    :members: calculateValue, getDataSeries, getWindowSize

Example
-------

Creating a custom filter is easy: ::

    from pyalgotrade import dataseries
    from pyalgotrade import technical

    class Accumulator(technical.DataSeriesFilter):
        def __init__(self, dataSeries, windowSize):
            technical.DataSeriesFilter.__init__(self, dataSeries, windowSize)

        def calculateValue(self, firstPos, lastPos):
            accum = 0
            for i in range(firstPos, lastPos + 1):
                value = self.getDataSeries().getValueAbsolute(i)
                # If any value from the wrapped DataSeries is None then we abort calculation and return None.
                if value is None:
                    return None
                accum += value
            return accum

    # Build a sequence based DataSeries.
    ds = dataseries.SequenceDataSeries(range(0, 50))

    # Wrap it with a 3 element Accumulator filter.
    ds = Accumulator(ds, 3)

    # Get some values.
    print ds.getValueAbsolute(0) # Not enough values yet.
    print ds.getValueAbsolute(1) # Not enough values yet.
    print ds.getValueAbsolute(2) # Ok, now we should have at least 3 values.
    print ds.getValueAbsolute(3)

    # Get the last value, which should equals 49 + 48 + 47.
    print ds.getValue()

The output should be: ::

    None
    None
    3
    6
    144

Moving Averages
---------------

.. automodule:: pyalgotrade.technical.ma
    :members: SMA, EMA, WMA

Momentum Indicators
-------------------

.. automodule:: pyalgotrade.technical.rsi
    :members: RSI

.. automodule:: pyalgotrade.technical.stoch
    :members: StochasticOscillator

.. automodule:: pyalgotrade.technical.roc
    :members: RateOfChange

Other Indicators
----------------

.. automodule:: pyalgotrade.technical.trend
    :members: Slope

.. automodule:: pyalgotrade.technical.cross
    :members: CrossAbove, CrossBelow

