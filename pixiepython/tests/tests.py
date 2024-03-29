
# Testing pyqhtools
# By Chas Egan
from unittest import TestCase
import math
import datetime as dt
import pyqhtools as pqh

class TestTimeseries(TestCase):
    def test_timeseries_constructor_returns_something(self):
        '''
        Code tested:
            Timeseries.__init__()
        '''
        result = pqh.Timeseries()
        self.assertTrue(result != None)

    def test_start_end(self):
        '''
        Code tested:
            Timeseries.__get_end()
            Timeseries.get_start_end()
            Timeseries.start
            Timeseries.end
        '''
        result = pqh.load_csv(r".\pixiepython\tests\test_data\r040168.csv")
        start_end = result.get_start_end()
        self.assertTrue(start_end[0] == dt.datetime(1892, 11, 1))
        self.assertTrue(start_end[1] == dt.datetime(1980, 9, 30))

    def test_length_with_complete_dataset(self):
        '''
        Code tested:
            Timeseries.__get_count()
            Timeseries.__get_missing()
            Timeseries.__get_nonmissing()
            Timeseries.length
            Timeseries.count
            Timeseries.missing
            Timeseries.nonmissing
        '''
        result = pqh.load_csv(r".\pixiepython\tests\test_data\p040134.csv")
        self.assertTrue(result.length == 47463)
        self.assertTrue(result.count == 47463)
        self.assertTrue(result.missing == 0)
        self.assertTrue(result.nonmissing == 47463)

    def test_length_with_gappy_dataset(self):
        '''
        Code tested:
            As above
        '''
        result = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        self.assertTrue(result.length == 39271)
        self.assertTrue(result.count == 39271)
        self.assertTrue(result.missing == 784)
        self.assertTrue(result.nonmissing == 38487)

    def test_length_with_multiline_headder(self):
        '''
        Code tested:
            As above
        '''
        result = pqh.load_csv(r".\pixiepython\tests\test_data\p040850_headder_missing_start_end.csv")
        self.assertTrue(result.length == 47463)
        self.assertTrue(result.count == 47463)
        self.assertTrue(result.missing == 26671)
        self.assertTrue(result.nonmissing == 20792)

    def test_min_max_mean_std_with_gappy_dataset(self):
        '''
        Code tested:
            Timeseries.__get_min()
            Timeseries.__get_max()
            Timeseries.__get_mean()
            Timeseries.__get_std()
            Timeseries.min
            Timeseries.max
            Timeseries.mean
            Timeseries.std
        '''
        result = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        self.assertTrue(result.min == 0.0)
        self.assertTrue(result.max == 494.0)
        self.assertTrue(abs(result.mean - 5.19659885) < 0.01)
        self.assertTrue(abs(result.std - 16.8) < 0.1)

    def test_loading_data_twice_gives_same_timeseries(self):
        '''
        Code tested:
            Timeseries.source
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts3 = pqh.load_csv(r".\pixiepython\tests\test_data\p040168.csv")
        comparison_results = ts1.compare(ts2)
        self.assertTrue(comparison_results[0] == True)
        self.assertTrue(ts1.source == ts2.source)
        self.assertTrue(ts1.source != ts3.source)

    def test_clone_gives_same_timeseries(self):
        '''
        Code tested:
            Timeseries.clone()
        '''
        original = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        theclone = original.clone()
        #Clones should look the same
        comparison_results = original.compare(theclone)
        self.assertTrue(comparison_results[0] == True)
        #But should not be the same after I manually edit some data
        theclone.data[0] = 53.0
        comparison_results = original.compare(theclone)
        self.assertTrue(comparison_results[0] == False)

    def test_summary_has_no_errors(self):
        '''
        Code tested:
            Timeseries.summary()
        '''
        #emtpy_ts = pqh.Timeseries()
        #empty_ts.summary()
        loaded_ts = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        loaded_ts.summary()
        self.assertTrue(True)

    def test_scaling_dataset(self):
        '''
        Code tested:
            Timeseries.scale(value)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts1.scale(10.0) #apply some positive scaling
        self.assertTrue(ts1.min == 0.0)
        self.assertTrue(ts1.max == 4940.0)
        self.assertTrue(abs(ts1.mean - 51.9659885) < 0.01)
        self.assertTrue(abs(ts1.std - 168.0) < 1)
        ts1.scale(-0.01) #apply some negative scaling
        self.assertTrue(abs(ts1.min - (-49.4)) < 0.01)
        self.assertTrue(ts1.max == 0.0)
        self.assertTrue(abs(ts1.mean - (-0.519659885)) < 0.01)
        self.assertTrue(abs(ts1.std - 1.68) < 0.1)

    def test_add_radd_number(self):
        '''
        Code tested:
            Timeseries.__add__(value)
            Timeseries.__radd__(value)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2 = ts1 + 1.1
        ts3 = 1.1 + ts1
        self.assertTrue(abs(ts1.mean - 5.19659885) < 0.000001) #__add__ and __radd__ do not modify the original timeseries
        self.assertTrue(abs(ts2.mean - 6.29659885) < 0.000001)
        self.assertTrue(ts2.min == 1.1)
        self.assertTrue(ts2.max == 495.1)
        self.assertTrue(ts2.length == ts1.length)
        self.assertTrue(ts2.compare(ts3)[0]) #TS3 and TS2 should be identical

    def test_neg(self):
        '''
        Code tested:
            Timeseries.__neg__()
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2 = -ts1
        self.assertTrue(abs(ts1.mean - 5.19659885) < 0.000001) #__neg__ should not modify the original timeseries
        self.assertTrue(abs(ts2.mean + 5.19659885) < 0.000001)
        self.assertTrue(ts2.min == -494)
        self.assertTrue(ts2.max == 0.0)
        self.assertTrue(ts2.length == ts1.length)

    def test_pow_number(self):
        '''
        Code tested:
            Timeseries.__pow__(number)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2 = ts1**2
        self.assertTrue(abs(ts1.mean - 5.19659885) < 0.000001) #__neg__ should not modify the original timeseries
        self.assertTrue(abs(ts2.mean - 311.5936900771) < 0.000001)
        self.assertTrue(ts2.length == ts1.length)

    def test_add_radd_timeseries(self):
        '''
        Code tested:
            Timeseries.__add__(other)
            Timeseries.__radd__(other)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2 = pqh.load_csv(r".\pixiepython\tests\test_data\r040168.csv")
        ts3 = ts1 + ts2
        ts4 = ts2 + ts1
        self.assertTrue(abs(ts1.mean - 5.19659885) < 0.000001) #__add__ and __radd__ do not modify the original timeseries
        self.assertTrue(abs(ts2.mean - 4.453350651058) < 0.000001) #__add__ and __radd__ do not modify the original timeseries
        self.assertTrue(abs(ts3.mean - 9.56699353053) < 0.000001)
        self.assertTrue(ts3.length == 45691) #length should be the union of ts1 and ts2 (not the intersect)
        self.assertTrue(ts4.compare(ts3)[0]) #ts3 and ts4 should be identical
        pqh.save_csv(ts3, r".\pixiepython\tests\test_data\output\r040134_plus_r040168.csv")

    def test_div_number(self):
        '''
        Code tested:
            Timeseries.__div__(number)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2 = ts1 / ts1.mean
        self.assertTrue(abs(ts1.mean - 5.19659885) < 0.000001) #__add__ and __radd__ do not modify the original timeseries
        self.assertTrue(abs(ts2.mean - 1.0) < 0.000001) #normalized series should have mean=1
        self.assertTrue(ts2.length == ts1.length)

    def test_sub_rsub_number(self):
        '''
        Code tested:
            Timeseries.__sub__(value)
            Timeseries.__rsub__(value)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2 = ts1 - 1.1
        ts3 = 1.1 - ts1
        self.assertTrue(abs(ts1.mean - 5.19659885) < 0.000001) #__sub__ and __rsub__ do not modify the original timeseries
        self.assertTrue(abs(ts2.mean - 4.09659885) < 0.000001)
        self.assertTrue(ts2.min == -1.1)
        self.assertTrue(ts2.max == 492.9)
        self.assertTrue(ts2.length == ts1.length)
        self.assertTrue(ts3.length == ts1.length)
        self.assertTrue(abs(ts3.mean + 4.09659885) < 0.000001)
        pqh.save_csv(ts2, r".\pixiepython\tests\test_data\output\r040134_minus_1point1.csv")

    def test_mul_rmul_number(self):
        '''
        Code tested:
            Timeseries.__mul__(value)
            Timeseries.__rmul__(value)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2 = ts1 * 2.0
        ts3 = 2.0 * ts1
        self.assertTrue(abs(ts1.mean - 5.19659885) < 0.000001) #__mul__ and __rmul__ do not modify the original timeseries
        self.assertTrue(abs(ts2.mean - 10.3931977) < 0.000001)
        self.assertTrue(ts2.min == 0)
        self.assertTrue(ts2.max == 988)
        self.assertTrue(ts2.length == ts1.length)
        self.assertTrue(ts2.compare(ts3)[0])
        pqh.save_csv(ts2, r".\pixiepython\tests\test_data\output\r040134_mul_2.csv")

    def test_get_value(self):
        '''
        Code tested:
            Timeseries.get_value(year, month, day, date=None)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        #Value before ts
        value = ts1.get_value(1910, 5, 1)
        self.assertTrue(math.isnan(value))
        #Value at start of ts
        value = ts1.get_value(1910, 6, 1)
        self.assertTrue(value == 26.9)
        #Value inside ts
        value = ts1.get_value(1910, 6, 2)
        self.assertTrue(value == 204.2)
        #Value inside ts (using datetime)
        value = ts1.get_value(0, 0, 0, date=pqh.parse_date("02-06-1910"))
        self.assertTrue(value == 204.2)
        #Missing value inside ts
        value = ts1.get_value(2012, 6, 26)
        self.assertTrue(math.isnan(value))
        #Value at end of ts
        value = ts1.get_value(2017, 12, 6)
        self.assertTrue(value == 36.0)
        #Value after ts
        value = ts1.get_value(2017, 12, 7)
        self.assertTrue(math.isnan(value))

    def test_set_value(self):
        '''
        Code tested:
            Timeseries.set_value(value, year, month, day, date=None)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        #Value at start of ts
        ts1.set_value(99.9, 1910, 6, 1)
        self.assertTrue(ts1.get_value(1910, 6, 1) == 99.9)
        #Value inside ts
        ts1.set_value(99.9, 1910, 6, 2)
        self.assertTrue(ts1.get_value(1910, 6, 2) == 99.9)
        #Value at end of ts
        ts1.set_value(99.9, 2017, 12, 6)
        self.assertTrue(ts1.get_value(2017, 12, 6) == 99.9)

    def test_set_value_if_missing(self):
        '''
        Code tested:
            Timeseries.set_value(value, year, month, day, date=None)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        #Value 26.9 is not missing and should not be changed
        ts1.set_value_if_missing(99.9, 1910, 6, 1)
        self.assertTrue(ts1.get_value(1910, 6, 1) == 26.9)
        #Value for 2012, 6, 26 is missing and should be changed
        ts1.set_value_if_missing(99.9, 2012, 6, 26)
        self.assertTrue(ts1.get_value(2012, 6, 26) == 99.9)

    def test_get_dates(self):
        '''
        Code tested:
            Timeseries.get_dates()
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        dates = ts1.get_dates()
        self.assertTrue(len(dates) == 39271)
        self.assertTrue(len(dates) == len(ts1.data))
        self.assertTrue(dates[0] == pqh.parse_date("01/06/1910"))

    def test_set_start_end(self):
        '''
        Code tested:
            Timeseries.set_start_end(start_and_end)
            Timeseries.set_start(year, month, day)
            Timeseries.set_end(year, month, day)
        '''
        #Load some patched-point data
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\p040134.csv")
        ts1_start_end = ts1.get_start_end()
        #Load some raw data and check length is different to above
        ts2 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        self.assertTrue(ts1.length != ts2.length)
        self.assertTrue(ts2.get_value(1910, 6, 1) == 26.9)
        #Extend the dates to be same as above and check lengths are now same
        ts2.set_start_end(ts1_start_end)
        self.assertTrue(ts1.length == ts2.length)
        self.assertTrue(ts2.get_value(1910, 6, 1) == 26.9)
        #Save the result for visual inspection
        pqh.save_csv(ts2, r".\pixiepython\tests\test_data\output\r040134_redated.csv")

    def test_set_start_end2(self):
        '''
        Code tested:
            Timeseries.set_start_end(start_and_end)
            Timeseries.set_start(year, month, day)
            Timeseries.set_end(year, month, day)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\p040134.csv")
        ts2 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        ts2_start_end = ts2.get_start_end()
        self.assertTrue(ts1.length != ts2.length)
        self.assertTrue(ts1.get_value(1910, 6, 1) == 26.9)
        ts1.set_start_end(ts2_start_end)
        #Save the result for visual inspection
        pqh.save_csv(ts1, r".\pixiepython\tests\test_data\output\r040134_redated2.csv")
        #Assert expected results
        self.assertTrue(ts1.length == ts2.length)
        self.assertTrue(ts1.get_value(1910, 6, 1) == 26.9)

    def test_bias(self):
        '''
        Code tested:
            Timeseries.bias(other)
        '''
        #For cloned data the bias should be 1.0
        original = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        clone = original.clone()
        bias = clone.bias(original)
        self.assertTrue(abs(bias - 1.0) < 0.000000001)
        #Now scale ts2 up 40% and measure the bias again
        clone.scale(1.4)
        bias = clone.bias(original)
        self.assertTrue(abs(bias - 1.4) < 0.000000001)

    def test_nse(self):
        '''
        Code tested:
            Timeseries.nse(other)
        '''
        obs = pqh.load_csv(r".\pixiepython\tests\test_data\416020_100141.CSV")
        mod = pqh.load_csv(r".\pixiepython\tests\test_data\416020_rfadj3test_fors.csv")
        nse = mod.nse(obs)
        self.assertTrue(abs(nse - 0.725302706062934) < 0.000000001)

    def test_pearsons_r(self):
        '''
        Code tested:
            Timeseries.pearsons_r(other)
        '''
        obs = pqh.load_csv(r".\pixiepython\tests\test_data\416020_100141.CSV")
        mod = pqh.load_csv(r".\pixiepython\tests\test_data\416020_rfadj3test_fors.csv")
        nse = mod.pearsons_r(obs)
        self.assertTrue(abs(nse - 0.864668449962663) < 0.000000001)

    def test_date_of_first_last_data(self):
        '''
        Code tested:
            Timeseries.bias(other)
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\p040850_headder_missing_start_end.csv")
        first_data_date = ts1.date_of_first_data()
        self.assertTrue(first_data_date == pqh.parse_date("12/02/1913"))
        last_data_date = ts1.date_of_last_data()
        self.assertTrue(last_data_date == pqh.parse_date("15/01/1970"))
        #Do another one
        ts2 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        first_data_date = ts2.date_of_first_data()
        self.assertTrue(first_data_date == pqh.parse_date("01/06/1910"))
        last_data_date = ts2.date_of_last_data()
        self.assertTrue(last_data_date == pqh.parse_date("06/12/2017"))

    def test_infill_merge(self):
        '''
        Code tested:
            Timeseries.infill_merge(other)
        '''
        gappy_data = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        all_ones = pqh.load_csv(r".\pixiepython\tests\test_data\all_ones.csv")
        #infilling by infill_merge
        gappy_data.infill_merge(all_ones)
        #Check the results
        mean_after_infilling = gappy_data.mean
        self.assertTrue(abs(mean_after_infilling - 4.40295598676) < 0.00001)
        self.assertTrue(gappy_data.get_value(1910, 6, 1) == 26.9)
        self.assertTrue(gappy_data.missing == 0)

    def test_infill_scale_auto_factor(self):
        '''
        Code tested:
            Timeseries.infill_scale(other)
        '''
        gappy_data = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        all_ones = pqh.load_csv(r".\pixiepython\tests\test_data\all_ones.csv")
        mean_before_infilling = gappy_data.mean
        #infilling by infill_scale should preserve the mean
        gappy_data.infill_scale(all_ones)
        pqh.save_csv(gappy_data, r".\pixiepython\tests\test_data\output\r040134_infilled.csv")
        #Check the results
        mean_after_infilling = gappy_data.mean
        self.assertTrue(abs(mean_before_infilling - mean_after_infilling) < 0.00001)
        self.assertTrue(gappy_data.get_value(1910, 6, 1) == 26.9)
        self.assertTrue(gappy_data.missing == 0)

    def test_infill_scale_force_factor(self):
        '''
        Code tested:
            Timeseries.infill_scale(other, factor=None)
        '''
        gappy_data = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        all_ones = pqh.load_csv(r".\pixiepython\tests\test_data\all_ones.csv")
        gappy_data.infill_scale(all_ones, factor = 0.6666)
        pqh.save_csv(gappy_data, r".\pixiepython\tests\test_data\output\r040134_infilled2.csv")
        #Check the results
        self.assertTrue(abs(gappy_data.mean - 4.339904801) < 0.00001)

    def test_infill_scalemonthly(self):
        '''
        Code tested:
            Timeseries.infill_scalemonthly(other, factors=None)
        '''
        gappy_data = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        all_ones = pqh.load_csv(r".\pixiepython\tests\test_data\all_ones.csv")
        monthly_factors = [0.7, 0.9, 1.1, 1.3, 1.5, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.5]
        gappy_data.infill_scalemonthly(all_ones, factors=monthly_factors)
        pqh.save_csv(gappy_data, r".\pixiepython\tests\test_data\output\r040134_infilled3.csv")
        #Check the results
        self.assertTrue(abs(gappy_data.mean - 4.412548722) < 0.0001)

    def test_infill_scalemonthly_4factors(self):
        '''
        Code tested:
            Timeseries.infill_scalemonthly(other, factors=None)
        '''
        gappy_data = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        all_ones = pqh.load_csv(r".\pixiepython\tests\test_data\all_ones.csv")
        monthly_factors = [1.1, 1.2, 0.9, 0.8]
        gappy_data.infill_scalemonthly(all_ones, factors=monthly_factors)
        pqh.save_csv(gappy_data, r".\pixiepython\tests\test_data\output\r040134_infilled4.csv")
        #Check the results
        self.assertTrue(abs(gappy_data.mean - 4.4031751048) < 0.000001)

    def test_infill_scalemonthly_wt93b(self):
        '''
        Code tested:
            Timeseries.infill_scalemonthly(other)
        '''
        #This is the WT93b test
        gappy_data = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        original_length = gappy_data.length
        gappy_data.infill_scalemonthly(gappy_data.clone())
        self.assertTrue(gappy_data.length == original_length)

    def test_infill_scalemonthly_wt93b_2(self):
        '''
        Code tested:
            Timeseries.infill_scalemonthly(other)
        '''
        #This is the WT93b test
        gappy_data = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        all_ones = pqh.load_csv(r".\pixiepython\tests\test_data\all_ones.csv")
        gappy_data.infill_scalemonthly(all_ones)
        pqh.save_csv(gappy_data, r".\pixiepython\tests\test_data\output\r040134_infilled5_wt93b.csv")
        #Check the results
        self.assertTrue(abs(gappy_data.mean - 5.21500501) < 0.0001)

    def test_infill_wt93b(self):
        '''
        Code tested:
            Timeseries.infill_wt93b(others)
        '''
        r040134 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        #r040168 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040168.csv")
        p040850 = pqh.load_csv(r".\pixiepython\tests\test_data\p040850.csv")
        factors = r040134.get_wt93_factors(p040850)
        known_answers = [1.0412290338857493,
            1.0065128956703973,
            1.0598426339157894,
            1.0476595992884017,
            1.0548171248637521,
            1.0538393731635654,
            1.0441554098438972,
            1.0498160869346143,
            1.0296487322003494,
            1.0394039501112953,
            1.0631576523681232,
            1.0712720135216185]
        for i in range(12):
            self.assertTrue(abs(factors[i] - known_answers[i]) < 0.0000001)
        r040134.infill_wt93b([p040850])
        pqh.save_csv(r040134, r".\pixiepython\tests\test_data\output\r040134_p040850.csv")
        self.assertTrue(r040134.missing == 0)

    def test_infill_wt93b2(self):
        '''
        Code tested:
            Timeseries.infill_wt93b(others)
        '''
        r040134 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        r040168 = pqh.load_csv(r".\pixiepython\tests\test_data\r040168.csv")
        p040850 = pqh.load_csv(r".\pixiepython\tests\test_data\p040850.csv")
        r040134.infill_wt93b([r040168,p040850])
        pqh.save_csv(r040134, r".\pixiepython\tests\test_data\output\r040134_r040168_p040850.csv")
        self.assertTrue(r040134.missing == 0)

    def test_infill_wt93b3(self):
        '''
        Code tested:
            Timeseries.infill_wt93b(others)
        '''
        r040695 = pqh.load_csv(r".\pixiepython\tests\test_data\r040695.csv")
        r040547 = pqh.load_csv(r".\pixiepython\tests\test_data\r040547.csv")
        p040264 = pqh.load_csv(r".\pixiepython\tests\test_data\p040264.csv")
        r040695.infill_wt93b([r040547,p040264])
        pqh.save_csv(r040695, r".\pixiepython\tests\test_data\output\r040695_r040547_p040264.csv")
        self.assertTrue(abs(r040695.mean - 4.6781753769) < 0.0000001)





class TestUtils(TestCase):
    def test_is_a_digit(self):
        '''
        Code tested:
            is_a_digit(char)
        '''
        self.assertTrue(pqh.is_a_digit('0'))
        self.assertTrue(pqh.is_a_digit('1'))
        self.assertTrue(pqh.is_a_digit('2'))
        self.assertTrue(pqh.is_a_digit('3'))
        self.assertTrue(pqh.is_a_digit('4'))
        self.assertTrue(pqh.is_a_digit('5'))
        self.assertTrue(pqh.is_a_digit('6'))
        self.assertTrue(pqh.is_a_digit('7'))
        self.assertTrue(pqh.is_a_digit('8'))
        self.assertTrue(pqh.is_a_digit('9'))
        self.assertTrue(not pqh.is_a_digit(' '))
        self.assertTrue(not pqh.is_a_digit('.'))
        self.assertTrue(not pqh.is_a_digit('-'))
        self.assertTrue(not pqh.is_a_digit('+'))
        self.assertTrue(not pqh.is_a_digit('a'))
        self.assertTrue(not pqh.is_a_digit('A'))

    def test_first_non_digit(self):
        '''
        Code tested:
            first_non_digit(char)
        '''
        #Check empty string input
        result_1 = pqh.first_non_digit("")
        self.assertTrue(result_1[0] == -1)
        self.assertTrue(result_1[1] == ' ')
        #Check string with all digits
        result_2 = pqh.first_non_digit("123")
        self.assertTrue(result_2[0] == -1)
        self.assertTrue(result_2[1] == ' ')
        #Check string starting with non-digit
        result_3 = pqh.first_non_digit("Hello world")
        self.assertTrue(result_3[0] == 0)
        self.assertTrue(result_3[1] == 'H')
        #Check string starting with non-digit (whitespace)
        result_4 = pqh.first_non_digit(" Hello world")
        self.assertTrue(result_4[0] == 0)
        self.assertTrue(result_4[1] == ' ')
        #Check string with digits followed by non-digits
        result_5 = pqh.first_non_digit("123World")
        self.assertTrue(result_5[0] == 3)
        self.assertTrue(result_5[1] == 'W')

    def test_parse_date(self):
        '''
        Code tested:
            parse_date(datestring)
        '''
        date1_string = r"04_02_2017"
        date1 = pqh.parse_date(date1_string)
        date2_string = r"2017\02\04"
        date2 = pqh.parse_date(date2_string)
        self.assertTrue(date1 == date2)
        self.assertTrue(date1.year == 2017)
        self.assertTrue(date1.month == 2)
        self.assertTrue(date1.day == 4)

    def test_parse_value(self):
        '''
        Code tested:
            parse_value(valuestring)
        '''
        self.assertTrue(pqh.parse_value("0.123") == pqh.parse_value("  0.123    "))
        self.assertTrue(pqh.parse_value("-0.123") == pqh.parse_value("  -0.123    "))
        self.assertTrue(math.isnan(pqh.parse_value("")))
        self.assertTrue(math.isnan(pqh.parse_value(" ")))
        self.assertTrue(math.isnan(pqh.parse_value("nan")))
        self.assertTrue(math.isnan(pqh.parse_value("NAN")))

    def test_is_data_row(self):
        '''
        Code tested:
            is_data_row(row)
        '''
        self.assertTrue(pqh.is_data_row("2017_01_01, 0.01"))
        self.assertTrue(not pqh.is_data_row("Lorem ipsum"))
        self.assertTrue(not pqh.is_data_row("Date, Value"))

    def test_count_missing(self):
        '''
        Code tested:
            count_missing(data)
        '''
        self.assertTrue(pqh.count_missing([]) == 0)
        self.assertTrue(pqh.count_missing([1, 2, 3]) == 0)
        self.assertTrue(pqh.count_missing([1, math.nan, 3]) == 1)
        self.assertTrue(pqh.count_missing([math.nan, math.nan, math.nan]) == 3)

    def test_period_length(self):
        '''
        Code tested:
            period_length(start_datetime, end_datetime, interval)
        '''
        dt1 = dt.datetime(2017, 1, 1)
        dt2 = dt.datetime(2017, 1, 3)
        self.assertTrue(pqh.period_length(dt1, dt1) == 0)
        self.assertTrue(pqh.period_length(dt1, dt2) == 2)
        self.assertTrue(pqh.period_length(dt2, dt1) == -2)
        one_hour = dt.timedelta(seconds=3600)
        self.assertTrue(pqh.period_length(dt2, dt1, one_hour) == -2 * 24)

    def test_days_in_month(self):
        '''
        Code tested:
            days_in_month(year, month)
        '''
        self.assertTrue(pqh.days_in_month(2018,1) == 31)
        self.assertTrue(pqh.days_in_month(2018,2) == 28)
        self.assertTrue(pqh.days_in_month(2018,3) == 31)
        self.assertTrue(pqh.days_in_month(2018,4) == 30)
        self.assertTrue(pqh.days_in_month(2018,5) == 31)
        self.assertTrue(pqh.days_in_month(2018,6) == 30)
        self.assertTrue(pqh.days_in_month(2018,7) == 31)
        self.assertTrue(pqh.days_in_month(2018,8) == 31)
        self.assertTrue(pqh.days_in_month(2018,9) == 30)
        self.assertTrue(pqh.days_in_month(2018,10) == 31)
        self.assertTrue(pqh.days_in_month(2018,11) == 30)
        self.assertTrue(pqh.days_in_month(2018,12) == 31)
        self.assertTrue(pqh.days_in_month(1900,2) == 28)
        self.assertTrue(pqh.days_in_month(1996,2) == 29)
        self.assertTrue(pqh.days_in_month(2000,2) == 29)
        self.assertTrue(pqh.days_in_month(2004,2) == 29)

    def test_last_day_in_month(self):
        '''
        Code tested:
            last_day_in_month(date)
        '''
        self.assertTrue(pqh.last_day_in_month(dt.datetime(2018,1,1)) == dt.datetime(2018,1,31))
        self.assertTrue(pqh.last_day_in_month(dt.datetime(2018,1,31)) == dt.datetime(2018,1,31))
        self.assertTrue(pqh.last_day_in_month(dt.datetime(2000,2,29)) == dt.datetime(2000,2,29))





class TestFileio(TestCase):
    def test_load_save_load(self):
        '''
        Code tested:
            load_csv
            save_csv
        '''
        ts1 = pqh.load_csv(r".\pixiepython\tests\test_data\r040134.csv")
        pqh.save_csv(ts1, r".\pixiepython\tests\test_data\output\r040134_resaved.csv")
        ts2 = pqh.load_csv(r".\pixiepython\tests\test_data\output\r040134_resaved.csv")
        comparison_results = ts1.compare(ts2)
        self.assertTrue(comparison_results[0] == True)

    def test_read_write_read(self):
        '''
        Code tested:
            read_csv
            write_csv
        '''
        ts1 = pqh.read_csv(r".\pixiepython\tests\test_data\r040134.csv")
        pqh.write_csv(ts1, r".\pixiepython\tests\test_data\output\r040134_resaved.csv")
        ts2 = pqh.read_csv(r".\pixiepython\tests\test_data\output\r040134_resaved.csv")
        comparison_results = ts1.compare(ts2)
        self.assertTrue(comparison_results[0] == True)
