from unittest import TestCase
from unittest import main

import shelve
import math
import os

from graph_deaths_by_state import graph_deaths_by_state
from graph_deaths_over_time import graph_deaths_over_time
from graph_oregon_death_freq import graph_oregon_death_freq
from test_utility_functions import *


class Test(TestCase):
    first_time = True

    def setUp(self):
        if self.__class__.first_time:
            print('Calling functions')
            self.__class__.db = shelve.open("expected_results")
            self.__class__.df = self.__class__.db['covid_data_frame']
            self.df = self.__class__.df

            #TODO put actual results in a dictionary
            self.__class__.act = dict()
            self.__class__.act['graph_deaths_by_state'] = graph_deaths_by_state(self.df)
            self.__class__.act['graph_deaths_over_time'] = graph_deaths_over_time(self.df)
            self.__class__.act['graph_oregon_death_freq'] = graph_oregon_death_freq(self.df)

            self.__class__.first_time = False

        self.act = self.__class__.act
        self.df = self.__class__.df
        self.db = self.__class__.db

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.first_time = True

    def test_by_state_hist(self):
        self.assertTrue(compDataFrame(self.db['graph_deaths_by_state'],
                                      self.act['graph_deaths_by_state']))

    def test_by_state_image(self):
        self.assertTrue(os.path.exists('deaths_by_state.png'))

    def test_over_time_totals(self):
        self.assertTrue(compDataFrame(self.db['graph_deaths_over_time'],
                                      self.act['graph_deaths_over_time']))

    def test_over_time_image(self):
        self.assertTrue(os.path.exists('deaths_over_time.png'))

    def test_oregon_freq_hist(self):
        self.assertTrue(compDataFrame(self.db['graph_oregon_death_freq'],
                                      self.act['graph_oregon_death_freq']))

    def test_oregon_freq_image(self):
        self.assertTrue(os.path.exists('OR_death_freq.png'))

if __name__ == '__main__':
    rslt = main(verbosity=2, exit=False)