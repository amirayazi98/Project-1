import pandas as pd
import matplotlib.pyplot as plt

#%%
def graph_deaths_by_state(data: pd.DataFrame) -> pd.DataFrame:
    """
    Summarizes and visualizes total COVID-19 deaths by state.

    This function takes a DataFrame containing COVID-19 data, aggregates
    the total number of deaths for each state, and generates a bar chart
    representing the total deaths by state. The bar chart is saved as
    'deaths_by_state.png'.

    Args:
        data (pd.DataFrame): A DataFrame containing at least the following columns:
            - 'state': The state name or code.
            - 'new_death': The number of new deaths reported.

    Returns:
        pd.DataFrame: A DataFrame containing:
            - 'state': The state name or code.
            - 'tot_death': The total number of deaths for each state.
    """
    # Summarize total deaths by state
    deaths_by_state = data.groupby('state', as_index=False)['new_death'].sum()
    deaths_by_state.rename(columns={'new_death': 'tot_death'}, inplace=True)

    # Plot: Total deaths by state
    plt.figure(figsize=(15, 8))
    plt.bar(deaths_by_state['state'], deaths_by_state['tot_death'], color='blue', alpha=0.7)
    plt.title('Total Deaths by State', fontsize=16)
    plt.xlabel('State', fontsize=14)
    plt.ylabel('Total Deaths', fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('deaths_by_state.png')
    plt.close()

    return deaths_by_state