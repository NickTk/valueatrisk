import pytest
import numpy as np
from models.models import VanillaOption, ForwardPrice

def right_part_parity(option: VanillaOption):
    parity = ( option.spot_price - option.strike_price * 
                np.exp(-option.risk_free_cont * option.time_to_expiry) )
    return parity

@pytest.fixture
def scenarios():
    scenarios = {
        'itm': VanillaOption('23.11.2022', '10.05.2023', 110, 100, 0.005, 0.0, 0.3),
        'atm': VanillaOption('23.11.2022', '10.05.2023', 100, 100, 0.005, 0.0, 0.3),
        'otm': VanillaOption('23.11.2022', '10.05.2023', 100, 110, 0.005, 0.0, 0.3)
        }
    return scenarios

def test_call_in_the_money(scenarios):
    """
    If the spot asset price exceeds the strike price,
    the call option is considered in-the-money, and the put option out-of-the-money.
    The distances d1 and d2 should be greater than zero.
    The call price must be greater than put price.
    At the same time, both prices should be greater than zero.
    The put-call parity must be in place.
    """
    option = scenarios.get('itm')
    model = ForwardPrice(option)
    call = model.call
    put = model.put
    left_part = call - put
    right_part = right_part_parity(option)
    parity = np.isclose(left_part, right_part, atol=1e-4)
    assert call > 0
    assert put > 0
    assert model.d1 > 0
    assert model.d2 > 0
    assert call > put
    assert parity == True, f"{call - put} not equals {right_part_parity(option)}"


def test_at_the_money(scenarios):
    """
    Neither call or put options have intrinsic value. 
    The distances d1 and d2, and in turn, the option's price 
    depend primarily on the time value and volatility. 
    Still both the call and put prices should be greater than zero.
    The put-call parity must be in place.
    """
    option = scenarios.get('atm')
    model = ForwardPrice(option)
    call = model.call
    put = model.put
    left_part = call - put
    right_part = right_part_parity(option)
    parity = np.isclose(left_part, right_part, atol=1e-4)
    assert call > 0
    assert put > 0
    assert parity == True


def test_call_out_of_the_money(scenarios):
    """
    If the spot asset price is lower than the strike price,
    the call option is considered out-the-money, and the put option in-the-money.
    Because of this, the call price must be lower than put price.
    At the same time, both prices should be greater than zero.
    """
    option = scenarios.get('otm')
    model = ForwardPrice(option)
    call = model.call
    put = model.put
    left_part = call - put
    right_part = right_part_parity(option)
    parity = np.isclose(left_part, right_part, atol=1e-4)
    assert call > 0
    assert put > 0
    assert put > call
    assert parity == True

def test_end_to_end(scenarios):
    for option in scenarios.values():
        model = ForwardPrice(option)
        call_price = model.call
        put_price = model.put

        assert call_price > 0
        assert put_price > 0

        if option.spot_price == option.strike_price:
            left_part = call_price - put_price
            right_part = right_part_parity(option)
            parity = np.isclose(left_part, right_part, atol=1e-4)
            assert parity == True
        elif option.spot_price > option.strike_price:
            assert call_price > put_price
        elif option.spot_price < option.strike_price:
            assert call_price < put_price
        
        







