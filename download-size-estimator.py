import requests
import sys
from random import shuffle
import re

# copied from https://github.com/shawnohare/samplesize/blob/master/samplesize.py


def sampleSize(
    population_size,
    margin_error=.05,
    confidence_level=.95,
    sigma=1/2
):
    """
    Calculate the minimal sample size to use to achieve a certain
    margin of error and confidence level for a sample estimate
    of the population mean.
    Inputs
    -------
    population_size: integer
        Total size of the population that the sample is to be drawn from.
    margin_error: number
        Maximum expected difference between the true population parameter,
        such as the mean, and the sample estimate.
    confidence_level: number in the interval (0, 1)
        If we were to draw a large number of equal-size samples
        from the population, the true population parameter
        should lie within this percentage
        of the intervals (sample_parameter - e, sample_parameter + e)
        where e is the margin_error.
    sigma: number
        The standard deviation of the population.  For the case
        of estimating a parameter in the interval [0, 1], sigma=1/2
        should be sufficient.
    """
    alpha = 1 - (confidence_level)
    # dictionary of confidence levels and corresponding z-scores
    # computed via norm.ppf(1 - (alpha/2)), where norm is
    # a normal distribution object in scipy.stats.
    # Here, ppf is the percentile point function.
    zdict = {
        .90: 1.645,
        .91: 1.695,
        .99: 2.576,
        .97: 2.17,
        .94: 1.881,
        .93: 1.812,
        .95: 1.96,
        .98: 2.326,
        .96: 2.054,
        .92: 1.751
    }
    if confidence_level in zdict:
        z = zdict[confidence_level]
    else:
        from scipy.stats import norm
        z = norm.ppf(1 - (alpha/2))
    N = population_size
    M = margin_error
    numerator = z**2 * sigma**2 * (N / (N-1))
    denom = M**2 + ((z**2 * sigma**2)/(N-1))
    return numerator/denom


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


margin_error = 0.05
confidence_level = 0.95

# remove all lines that are just whitespace
urls = [line.strip() for line in filter(
    lambda x: not re.match(r'^\s*$', x), sys.stdin.readlines())]
sizes = []

shuffle(urls)
sample_size_needed = int(sampleSize(len(urls)))

i = 0
while (len(sizes) < sample_size_needed) and (i < len(urls)):
    url = urls[i]
    try:
        response = requests.head(url, allow_redirects=True)

        size = int(response.headers.get('content-length', -1))
        if (size >= 0):
            sizes.append(size)
        else:
            print("Warning: ignoring " + url +
                  " because it didn't have a content-length header")
    except requests.exceptions.RequestException as e:
        print("Warning: " + url + " couldn't be reached")
    finally:
        i = i + 1

if len(sizes) < sample_size_needed:
    print("The sample size was " + str(sample_size_needed) + ", but there were only " +
          str(len(sizes)) + " valid URLs with valid content-sizes or URLs that could be reached")
    exit(1)

avg = sum(sizes)/len(sizes)
print(sizeof_fmt(avg) + "±" + sizeof_fmt((avg * margin_error) / 2) + " (" +
      str(int(confidence_level * 100)) + "% conf., " + str(int(margin_error * 100)) + "% error)")
