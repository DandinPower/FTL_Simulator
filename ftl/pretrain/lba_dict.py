import csv
import statistics
from dotenv import load_dotenv
import os
load_dotenv()

LBA_FREQ_PATH = os.getenv('LBA_FREQ_PATH')

# Define a function to standardize the frequency values
def standardize(frequency_values):
    mean = statistics.mean(frequency_values)
    stdev = statistics.stdev(frequency_values)
    standardized_values = [(x - mean) / stdev for x in frequency_values]
    return standardized_values

def GetLbaFreqDict():
    # Load the LBA frequency statistics from the CSV file
    lba_frequencies = {}
    with open(LBA_FREQ_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lba = row['LBA']
            frequency = int(row['Frequency'])
            lba_frequencies[lba] = frequency

    # Standardize the frequency values
    standardized_frequencies = standardize(list(lba_frequencies.values()))

    # Store the standardized frequency values in a dictionary with the LBA values as keys
    lba_standardized_frequencies = {}
    for i, lba in enumerate(lba_frequencies):
        frequency = standardized_frequencies[i]
        lba_standardized_frequencies[lba] = frequency
    return lba_standardized_frequencies