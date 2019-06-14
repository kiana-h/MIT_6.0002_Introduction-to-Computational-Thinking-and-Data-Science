# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import numpy
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""
#data = Climate("data.csv")

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    result = []
    for degree in degs:
        result.append(pylab.polyfit(x, y, degree))
    return result


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """        
    #R^2 = 1 - E (actual - estimate)^2 / E (actual - mean)^2        
    r_sq = 1 - pylab.sum((y - estimated)**2)/pylab.sum((y - pylab.mean(y))**2)        
    return r_sq

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        poly = pylab.poly1d(model)
        r_sq = r_squared(y, poly(x))
        pylab.figure()
        pylab.plot(x, y, "bo")
        pylab.plot(x, poly(x), "r-")
        pylab.xlabel("Year")
        pylab.ylabel("Temperature (Celsius)")
        if len(model) == 2:
            se = se_over_slope(x, y, poly(x), model)
            pylab.title("Degree of Fit: " + str(len(model)) + "\n R-Sqaured: " + str(round(r_sq , 2)) + "\n Ratio of Standard Error: " + str(round(se , 2)))
        else:
            pylab.title("Degree of Fit: " + str(len(model)) + "\n R-Sqaured: " + str(round(r_sq , 2)))       
        pylab.show()

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    result = []
    
    for year in years:
        year_temp = []
        for city in multi_cities:
            city_year_data = climate.get_yearly_temp(city , year)
            year_temp.append(city_year_data)
            city_temp = pylab.mean(city_year_data)
            year_temp.append(city_temp)
        year_avg_temp = pylab.mean(year_temp)
        result.append(year_avg_temp)
        
    return pylab.array(result)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    result = []
    for i in range(0 , window_length - 1):
        result.append(sum(y[0:i+1])/(i+1)) 
    for i in range(window_length - 1 , len(y)):
        result.append(sum(y[i-(window_length-1):i+1])/window_length) 
    
    return pylab.array(result)
       

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    ##rmse = sqrt(E(actual - estimate)^2)
    
    return numpy.sqrt(sum((y - estimated)**2)/len(y))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    result = []
    
    for year in years:
        year_temp = []
        for city in multi_cities:
            city_year_data = climate.get_yearly_temp(city , year)
            year_temp.append(city_year_data)
        day_temps = zip(*year_temp)
        day_avg = []
        for day in day_temps:
            day_avg.append(pylab.mean(day))
        year_std = pylab.std(day_avg)
        result.append(year_std)
        
    return pylab.array(result)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        poly = pylab.poly1d(model)
        pylab.figure()
        pylab.plot(x, y, "bo")
        pylab.plot(x, poly(x), "r-")
        pylab.xlabel("Year")
        pylab.ylabel("Temperature (Celsius)")
        pylab.title("Degree of Fit: " + str(len(model)) + "\n RMSE: " + str(round(rmse(y, poly(x)) , 2)))       
        pylab.show()

if __name__ == '__main__':
    data = Climate("data.csv")
    # Part A.4

## find trend using same day/month in a sample city throughtout years    
#    temps = []
#    for year in TRAINING_INTERVAL:
#        t = data.get_daily_temp("NEW YORK" , 1 , 10 , year)
#        temps.append(t)
#    model = generate_models(pylab.array(TRAINING_INTERVAL), pylab.array(temps), [1])
#    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), pylab.array(temps), model)
    
# find trend using annual average temperature in a sample city throughtout years     
#    temps = []
#    for year in TRAINING_INTERVAL:
#        year_temp = data.get_yearly_temp("NEW YORK" , year)
#        average_temp = sum(year_temp)/len(year_temp)
#        temps.append(average_temp)
#    model = generate_models(pylab.array(TRAINING_INTERVAL), pylab.array(temps), [1])
#    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), pylab.array(temps), model)   
        
    # Part B
#    temps = gen_cities_avg(data , CITIES , TRAINING_INTERVAL)
#    model = generate_models(pylab.array(TRAINING_INTERVAL), temps, [1])
#    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), temps, model)

    # Part C
#    temps = gen_cities_avg(data , CITIES , TRAINING_INTERVAL)
#    avg_temps = moving_average(temps , 5)
#    model = generate_models(pylab.array(TRAINING_INTERVAL), avg_temps, [1])
#    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), avg_temps, model)

    # Part D.2
#    temps = gen_cities_avg(data , CITIES , TRAINING_INTERVAL)
#    avg_temps = moving_average(temps , 5)
#    model = generate_models(pylab.array(TRAINING_INTERVAL), avg_temps, [1 , 2 , 20])
#    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), avg_temps, model)
    
#    temps = gen_cities_avg(data , CITIES , TESTING_INTERVAL)
#    avg_temps = moving_average(temps , 5)
#    evaluate_models_on_testing(pylab.array(TESTING_INTERVAL), avg_temps, model)

    # Part E
    stds = gen_std_devs(data, CITIES, TRAINING_INTERVAL)
    moving_stds = avg_temps = moving_average(stds , 5)
    model = generate_models(pylab.array(TRAINING_INTERVAL), moving_stds , [1])
    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), moving_stds , model)
