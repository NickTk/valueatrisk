from dataclasses import dataclass
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from statistics import NormalDist

@dataclass 
class VanillaOption:
    trade_date: str
    expiry_date: str
    spot_price: float
    strike_price: float
    risk_free_int: float
    dividends: float
    volatility: float

    @property
    def time_to_expiry(self) -> float:
        expiry = pd.to_datetime(self.expiry_date, format="%d.%m.%Y")
        trade = pd.to_datetime(self.trade_date, format="%d.%m.%Y")
        delta_days = (expiry - trade).days
        return delta_days / 365

    @property
    def risk_free_cont(self) -> float:
        return np.log(1 + self.risk_free_int)

class BlackScholes(ABC):
    def __init__(self, option: VanillaOption):
        self._option = option

    @property
    @abstractmethod
    def price(self) -> float:
        ...
    
    @property
    @abstractmethod
    def d1(self) -> float:
        """
        The probability-adjusted distance of the current asset price to the strike price
        """
        ...

    @property
    @abstractmethod
    def d2(self) -> float:
        """
        The likelihood that the option will expire in-the-money
        """
        ...

    @property
    @abstractmethod
    def call(self) -> float:
        """
        The call price of the option on non-dividend-paying stocks
        """
        ...

    @property
    @abstractmethod
    def put(self) -> float:
        """
        The put price of the option on non-dividend-paying stocks
        """
        ...
    
    @property
    @abstractmethod
    def put_from_parity(self) -> float:
        """
        The price of a call option, minus the price of a put option, 
        must be equal to the current asset price minus the current strike price
        """

class SpotPrice(BlackScholes):
    @property
    def price(self) -> float:
        return self._option.spot_price

    @property
    def d1(self) -> float:
        o = self._option
        d1 = ( np.log(self.price / o.strike_price) 
             + o.time_to_expiry * ( o.risk_free_cont + (o.volatility**2) / 2 )
        ) / ( o.volatility * np.sqrt(o.time_to_expiry) )
        return d1


    @property
    def d2(self) -> float:
        o = self._option
        d2 = self.d1 - o.volatility * np.sqrt(o.time_to_expiry)
        return d2

    @property
    def call(self) -> float:
        o = self._option
        norm = NormalDist()
        call = ( norm.cdf(self.d1) * self.price 
               - norm.cdf(self.d2) * o.strike_price * np.exp(-o.risk_free_cont * o.time_to_expiry)
        )
        return call

    @property
    def put(self) -> None:
        return

    @property
    def put_from_parity(self) -> None:
        return


class ForwardPrice(BlackScholes):
    @property
    def price(self) -> float:
        #without dividends
        o = self._option
        forward_price = o.spot_price * np.exp(o.risk_free_cont*o.time_to_expiry)
        return forward_price

    @property
    def d1(self) -> float:
        o = self._option
        d1 = ( np.log(self.price / o.strike_price) 
             + o.time_to_expiry * (o.volatility**2) / 2 
        ) / ( o.volatility * np.sqrt(o.time_to_expiry) ) 
        return d1

    @property
    def d2(self) -> float:
        o = self._option
        d2 = self.d1 - o.volatility * np.sqrt(o.time_to_expiry)
        return d2

    @property
    def call(self) -> float:
        o = self._option
        norm = NormalDist()
        call = ( norm.cdf(self.d1) * self.price
               - norm.cdf(self.d2) * o.strike_price) * np.exp(-o.risk_free_cont * o.time_to_expiry)
        return call

    @property
    def put(self) -> float:
        o = self._option
        norm = NormalDist()
        put = ( norm.cdf(-self.d2) * o.strike_price
              - norm.cdf(-self.d1) * self.price) * np.exp(-o.risk_free_cont * o.time_to_expiry)
        return put

    @property
    def put_from_parity(self) -> float:
        o = self._option
        put = self.call - o.spot_price + o.strike_price * np.exp(-o.risk_free_cont * o.time_to_expiry)
        return put