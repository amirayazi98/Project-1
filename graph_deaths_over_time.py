import pandas as pd
import matplotlib.pyplot as plt

#%%
def graph_deaths_over_time(data: pd.DataFrame) -> pd.DataFrame:
    """
    Produces an XY scatter diagram of COVID-19 deaths over time with rolling averages.
    Saves the diagram as 'deaths_over_time.png'.

    Arguments:
    data -- Pandas DataFrame containing COVID data with 'submission_date' already converted to datetime.

    Returns:
    A Pandas DataFrame containing:
      - submission_date: Datetime of submission
      - tot_death: Total deaths for all states on each submission date
    """
    # Group by submission_date and calculate total deaths
    daily_deaths = data.groupby('submission_date', as_index=False)['new_death'].sum()
    daily_deaths.rename(columns={'new_death': 'tot_death'}, inplace=True)

    # Compute rolling averages
    daily_deaths['7_day_avg'] = daily_deaths['tot_death'].rolling(window=7, min_periods=1).mean()
    daily_deaths['30_day_avg'] = daily_deaths['tot_death'].rolling(window=30, min_periods=1).mean()
    daily_deaths['90_day_avg'] = daily_deaths['tot_death'].rolling(window=90, min_periods=1).mean()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.scatter(daily_deaths['submission_date'], daily_deaths['tot_death'],
                color='orange', s=70, label='Actual')  # Bold yellow circles
    plt.plot(daily_deaths['submission_date'], daily_deaths['7_day_avg'],
             color='darkred', linewidth=2, label='7-Day Moving Average')
    plt.plot(daily_deaths['submission_date'], daily_deaths['30_day_avg'],
             color='blue', linewidth=2, label='30-Day Moving Average')
    plt.plot(daily_deaths['submission_date'], daily_deaths['90_day_avg'],
             color='green', linewidth=2, label='90-Day Moving Average', alpha=0.9)

    # Title and labels
    plt.title('Covid Deaths Over Time: 01/22/2020-01/16/2022', fontsize=16)  # Removed bolding
    plt.xlabel('Submission Date', fontsize=20)
    plt.ylabel('Total Deaths', fontsize=20)

    # Slanted x-axis labels for dates
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)

    # Legend box on the right side
    plt.legend(loc='upper right', fontsize=10, frameon=True)

    # Save the plot
    plt.tight_layout()
    plt.savefig('deaths_over_time.png')
    plt.close()

    return daily_deaths
