from pyalgotrade.optimizer import worker
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi

class MyStrategy(strategy.Strategy):
    def __init__(self, feed, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold):
        strategy.Strategy.__init__(self, feed, 2000)
        ds = feed.getDataSeries("dia").getCloseDataSeries()
        self.__entrySMA = ma.SMA(ds, entrySMA)
        self.__exitSMA = ma.SMA(ds, exitSMA)
        self.__rsi = rsi.RSI(ds, rsiPeriod)
        self.__overBoughtThreshold = overBoughtThreshold
        self.__overSoldThreshold = overSoldThreshold
        self.__longPos = None
        self.__shortPos = None

    def onEnterOk(self, position):
        pass

    def onEnterCanceled(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitOk(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.exitPosition(position)

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__exitSMA.getValue() is None or self.__entrySMA.getValue() is None or self.__rsi.getValue() is None:
            return

        bar = bars.getBar("dia")
        if self.__longPos != None:
            if self.exitLongSignal(bar):
                self.exitPosition(self.__longPos)
        elif self.__shortPos != None:
            if self.exitShortSignal(bar):
                self.exitPosition(self.__shortPos)
        else:
            if self.enterLongSignal(bar):
                self.__longPos = self.enterLong("dia", 10, True)
            elif self.enterShortSignal(bar):
                self.__shortPos = self.enterShort("dia", 10, True)

    def enterLongSignal(self, bar):
        return bar.getClose() > self.__entrySMA.getValue() and self.__rsi.getValue() <= self.__overSoldThreshold

    def exitLongSignal(self, bar):
        return bar.getClose() > self.__exitSMA.getValue()

    def enterShortSignal(self, bar):
        return bar.getClose() < self.__entrySMA.getValue() and self.__rsi.getValue() >= self.__overBoughtThreshold

    def exitShortSignal(self, bar):
        return bar.getClose() < self.__exitSMA.getValue()

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    worker.run(MyStrategy, "localhost", 5000)

