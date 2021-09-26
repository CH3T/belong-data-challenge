import sys
sys.path.append('.')
from ped_data import CsvAggr
import os.path


def test_calc_ped_data():

    csvAggr = CsvAggr()

    csvAggr.calc_ped_data('test/test_data.csv','test/test_daily_results.csv','test/test_monthly_results.csv')

    assert(os.path.isfile('test/test_daily_results.csv'))
    assert(os.path.isfile('test/test_monthly_results.csv'))
    
test_calc_ped_data()
    
