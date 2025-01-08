import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
def graph_oregon_death_freq(data: pd.DataFrame) -> pd.DataFrame:
    """
    Produces a histogram of COVID-19 death frequencies in Oregon.
    Saves the histogram as 'oregon_death_freq.png'.

    Arguments:
    data -- Pandas DataFrame containing COVID data with 'submission_date' already converted to datetime.

    Returns:
    A Pandas DataFrame containing:
      - bin: Left endpoint of each bin
      - tot_death: Count of deaths in the bin starting at the left endpoint
    """
    # Filter for Oregon data
    oregon_data = data[data['state'] == 'OR']

    # Handle empty data case
    if oregon_data.empty:
        return pd.DataFrame(columns=['bin', 'tot_death'])

    # Define bins
    max_death = oregon_data['new_death'].max()
    bin_edges = [0, 1, 2, 5] + list(range(10, 121, 10))  # Ensure bins extend to 120

    # Calculate histogram
    counts, bins = np.histogram(oregon_data['new_death'], bins=bin_edges)

    # Create DataFrame
    freq_data = pd.DataFrame({
        'bin': bins[:-1],  # Left endpoints of bins
        'tot_death': counts.astype(int)  # Frequencies as integers
    })

    # Plot: Histogram
    plt.figure(figsize=(10, 6))
    plt.hist(oregon_data['new_death'], bins=bin_edges, edgecolor=None, color='#800000', alpha=1)
    plt.title("New Death Frequency (Daily): ['OR']", fontsize=16)
    plt.xlabel('New Deaths (Daily)', fontsize=12)
    plt.ylabel('New Death Frequency', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(False)  # Remove gridlines
    plt.tight_layout()
    plt.savefig('OR_death_freq.png')
    plt.close()

    return freq_data