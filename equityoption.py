import streamlit as st
import pandas as pd
import numpy as np

# Set page title and configuration
st.set_page_config(page_title="Option Redemption Calculator", layout="wide")
st.title("Option Redemption Calculator")

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Get redemption percentage (0-10% in 1% increments)
redemption_percentage = st.sidebar.slider(
    "Redemption Percentage", 
    min_value=0, 
    max_value=10,
    value=5,
    step=1,
    help="Percentage of vested unsold shares to redeem each year"
) / 100

# Get PBT growth rate (0-20% in 1% increments)
pbt_growth_rate = st.sidebar.slider(
    "PBT Growth Rate", 
    min_value=0, 
    max_value=20,
    value=15,
    step=1,
    help="Annual growth rate of share price"
) / 100

# Get strike price - UPDATED DEFAULT TO £6.00
strike_price = st.sidebar.number_input(
    "Strike Price (£)",
    min_value=0.01,
    value=6.00,
    step=0.01,
    format="%.2f",
    help="Initial strike price of options"
)

# Get total grant shares
total_grant_shares = st.sidebar.number_input(
    "Total Grant Shares",
    min_value=1,
    value=10000,
    step=100,
    help="Total number of shares in the grant"
)

# Vesting schedule inputs
st.sidebar.header("Vesting Schedule")
vesting_method = st.sidebar.radio(
    "Vesting Method",
    ["Default Schedule", "Custom Vesting"],
    help="Choose default vesting schedule or set custom values"
)

# Initialize vested_shares_input dictionary
vested_shares_input = {}

if vesting_method == "Default Schedule":
    vested_shares_input = {
        2025: 6000,
        2026: 7000,
        2027: 8000,
        2028: 9000,
        2029: 10000,
        2030: 10000,
        2031: 10000,
        2032: 10000,
        2033: 10000,
        2034: 10000,
        2035: 10000
    }
    
    # Display the default schedule
    st.sidebar.write("Default vesting schedule:")
    default_schedule = pd.DataFrame({"Year": vested_shares_input.keys(), 
                                    "Vested Shares": vested_shares_input.values()})
    st.sidebar.dataframe(default_schedule, hide_index=True)
    
else:
    # Custom vesting inputs
    st.sidebar.write("Enter vested shares for each year:")
    
    # Use columns for more compact layout
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        vested_shares_input[2025] = st.number_input("2025", min_value=0, max_value=int(total_grant_shares), value=6000, step=100)
        vested_shares_input[2026] = st.number_input("2026", min_value=0, max_value=int(total_grant_shares), value=7000, step=100)
        vested_shares_input[2027] = st.number_input("2027", min_value=0, max_value=int(total_grant_shares), value=8000, step=100)
        vested_shares_input[2028] = st.number_input("2028", min_value=0, max_value=int(total_grant_shares), value=9000, step=100)
        vested_shares_input[2029] = st.number_input("2029", min_value=0, max_value=int(total_grant_shares), value=10000, step=100)
        vested_shares_input[2030] = st.number_input("2030", min_value=0, max_value=int(total_grant_shares), value=10000, step=100)
    
    with col2:
        vested_shares_input[2031] = st.number_input("2031", min_value=0, max_value=int(total_grant_shares), value=10000, step=100)
        vested_shares_input[2032] = st.number_input("2032", min_value=0, max_value=int(total_grant_shares), value=10000, step=100)
        vested_shares_input[2033] = st.number_input("2033", min_value=0, max_value=int(total_grant_shares), value=10000, step=100)
        vested_shares_input[2034] = st.number_input("2034", min_value=0, max_value=int(total_grant_shares), value=10000, step=100)
        vested_shares_input[2035] = st.number_input("2035", min_value=0, max_value=int(total_grant_shares), value=10000, step=100)

# Display the main parameters
st.write("### Parameters")
st.write(f"- **Redemption Rate**: {redemption_percentage*100:.0f}%")
st.write(f"- **PBT Growth Rate**: {pbt_growth_rate*100:.0f}%")
st.write(f"- **Strike Price**: £{strike_price:.2f}")
st.write(f"- **Total Grant Shares**: {total_grant_shares:,}")

try:
    # Calculate values with specific redemption and growth rates WITHOUT ROUNDING
    def calculate_values(redemption_pct, growth_pct, vesting_input):
        # Initialize dataframe for years 2024-2035
        years = list(range(2024, 2036))
        df = pd.DataFrame(index=years)
        
        # Initialize columns
        df['Share Price'] = 0.0
        df['Vested Shares'] = 0
        df['Vested Unsold Shares'] = 0
        df['Redeemed Shares'] = 0
        df['Cumulative Redeemed'] = 0
        df['Unsold Shares'] = 0
        df['Redemption Value'] = 0.0
        df['Cumulative Redemption Value'] = 0.0
        df['Value of Unsold Shares'] = 0.0
        df['Total Grant Value'] = 0.0
        
        # Initial values for 2024
        df.loc[2024, 'Share Price'] = strike_price
        df.loc[2024, 'Vested Shares'] = 0
        df.loc[2024, 'Vested Unsold Shares'] = 0
        df.loc[2024, 'Redeemed Shares'] = 0
        df.loc[2024, 'Cumulative Redeemed'] = 0
        df.loc[2024, 'Unsold Shares'] = total_grant_shares
        df.loc[2024, 'Redemption Value'] = 0.0
        df.loc[2024, 'Cumulative Redemption Value'] = 0.0
        df.loc[2024, 'Value of Unsold Shares'] = 0.0
        df.loc[2024, 'Total Grant Value'] = 0.0
        
        # Year 2025 calculations (no redemption in first year)
        df.loc[2025, 'Share Price'] = df.loc[2024, 'Share Price'] * (1 + growth_pct)
        df.loc[2025, 'Vested Shares'] = vesting_input[2025]
        df.loc[2025, 'Redeemed Shares'] = 0
        df.loc[2025, 'Cumulative Redeemed'] = 0
        df.loc[2025, 'Vested Unsold Shares'] = df.loc[2025, 'Vested Shares'] - df.loc[2025, 'Cumulative Redeemed']
        df.loc[2025, 'Unsold Shares'] = df.loc[2024, 'Unsold Shares']
        share_price_diff = max(0, df.loc[2025, 'Share Price'] - strike_price)
        df.loc[2025, 'Redemption Value'] = 0.0
        df.loc[2025, 'Cumulative Redemption Value'] = 0.0
        df.loc[2025, 'Value of Unsold Shares'] = share_price_diff * df.loc[2025, 'Unsold Shares']
        df.loc[2025, 'Total Grant Value'] = df.loc[2025, 'Cumulative Redemption Value'] + df.loc[2025, 'Value of Unsold Shares']
        
        # Calculate for years 2026-2035
        for year in range(2026, 2036):
            # Share price calculation with growth rate (no rounding)
            df.loc[year, 'Share Price'] = df.loc[year-1, 'Share Price'] * (1 + growth_pct)
            
            # Vested shares from input
            df.loc[year, 'Vested Shares'] = vesting_input[year]
            
            # Redeemed shares (% of previous year's vested unsold shares) - no rounding
            df.loc[year, 'Redeemed Shares'] = df.loc[year-1, 'Vested Unsold Shares'] * redemption_pct
            
            # Cumulative redeemed - no rounding
            df.loc[year, 'Cumulative Redeemed'] = df.loc[year-1, 'Cumulative Redeemed'] + df.loc[year, 'Redeemed Shares']
            
            # Unsold shares = total shares minus cumulative redeemed
            df.loc[year, 'Unsold Shares'] = total_grant_shares - df.loc[year, 'Cumulative Redeemed']
            
            # Vested unsold shares = vested shares minus cumulative redeemed
            df.loc[year, 'Vested Unsold Shares'] = df.loc[year, 'Vested Shares'] - df.loc[year, 'Cumulative Redeemed']
            df.loc[year, 'Vested Unsold Shares'] = max(0, df.loc[year, 'Vested Unsold Shares'])
            
            # Redemption value = (share price - strike price) * redeemed shares
            share_price_diff = max(0, df.loc[year, 'Share Price'] - strike_price)
            df.loc[year, 'Redemption Value'] = share_price_diff * df.loc[year, 'Redeemed Shares']
            
            # Cumulative redemption value
            df.loc[year, 'Cumulative Redemption Value'] = df.loc[year-1, 'Cumulative Redemption Value'] + df.loc[year, 'Redemption Value']
            
            # Value of unsold shares = (share price - strike price) * unsold shares
            df.loc[year, 'Value of Unsold Shares'] = share_price_diff * df.loc[year, 'Unsold Shares']
            
            # Total grant value = cumulative redemption value + value of unsold shares
            df.loc[year, 'Total Grant Value'] = df.loc[year, 'Cumulative Redemption Value'] + df.loc[year, 'Value of Unsold Shares']
        
        return df

    # Main results with user-selected parameters
    results = calculate_values(redemption_percentage, pbt_growth_rate, vested_shares_input)
    
    # Display results table
    st.write("### Illustrative Grant Value Based on Customized Inputs")
    
    # Filter to only show 2025 onwards and selected columns
    filtered_results = results.loc[2025:, ['Share Price', 'Cumulative Redemption Value', 'Total Grant Value']]
    filtered_results = filtered_results.rename(columns={
        'Share Price': 'Share Repurchase Price (£)',
        'Cumulative Redemption Value': 'Proceeds from Share Redemption (£)',
        'Total Grant Value': 'Total Grant Value (£)'
    })
    
    # Format for display
    display_df = filtered_results.copy()
    
    # Format indices as strings ('2025', '2026', etc.)
    display_df.index = display_df.index.map(lambda x: f'{x}')
    
    # Format share price with 2 decimal places
    display_df['Share Repurchase Price (£)'] = display_df['Share Repurchase Price (£)'].apply(lambda x: f"£{x:.2f}")
    
    # Format other columns with NO decimal places, only thousands separator
    for col in ['Proceeds from Share Redemption (£)', 'Total Grant Value (£)']:
        display_df[col] = display_df[col].apply(lambda x: f"£{int(x):,}")
    
    # Display the results table
    st.dataframe(display_df, use_container_width=True)
    
    # Download button for results
    csv = filtered_results.to_csv(index=True)
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name="option_redemption_results.csv",
        mime="text/csv",
    )
    
    # CHART 1: PBT Growth fixed at 20%, varying redemption rates
    st.write("### Grant Value at Various Redemption Rates")
    st.write("*PBT Growth Rate fixed at 20%*")
    
    # Calculate data for different redemption rates using the user's vesting schedule
    chart1_data = pd.DataFrame(index=range(2025, 2036))
    
    # Add lines for different redemption rates
    redemption_rates = [0.0, 0.05, 0.10]
    for rate in redemption_rates:
        results_for_rate = calculate_values(rate, 0.20, vested_shares_input)
        chart1_data[f"{int(rate*100)}% Redemption"] = results_for_rate.loc[2025:2035, 'Total Grant Value']
    
    # Convert index to strings for better display
    chart1_data.index = chart1_data.index.map(str)
    
    # Display the chart
    st.line_chart(chart1_data)
    
    # Display 2035 values in a table for Chart 1
    st.write("**Final 2035 Values:**")
    final_values1 = pd.DataFrame({
        'Redemption Rate': [f"{int(rate*100)}%" for rate in redemption_rates],
        'Total Grant Value (£)': [f"£{int(calculate_values(rate, 0.20, vested_shares_input).loc[2035, 'Total Grant Value']):,}" for rate in redemption_rates]
    })
    st.table(final_values1)
    
    # CHART 2: Redemption rate fixed at 0%, varying PBT growth rates
    st.write("### Grant Value at Various PBT Growth Rates")
    st.write("*Redemption Rate fixed at 0%*")
    
    # Calculate data for different growth rates using the user's vesting schedule
    chart2_data = pd.DataFrame(index=range(2025, 2036))
    
    # Add lines for different growth rates
    growth_rates = [0.15, 0.20]
    for rate in growth_rates:
        results_for_growth = calculate_values(0.0, rate, vested_shares_input)
        chart2_data[f"{int(rate*100)}% Growth"] = results_for_growth.loc[2025:2035, 'Total Grant Value']
    
    # Convert index to strings for better display
    chart2_data.index = chart2_data.index.map(str)
    
    # Display the chart
    st.line_chart(chart2_data)
    
    # Display 2035 values in a table for Chart 2
    st.write("**Final 2035 Values:**")
    final_values2 = pd.DataFrame({
        'Growth Rate': [f"{int(rate*100)}%" for rate in growth_rates],
        'Total Grant Value (£)': [f"£{int(calculate_values(0.0, rate, vested_shares_input).loc[2035, 'Total Grant Value']):,}" for rate in growth_rates]
    })
    st.table(final_values2)

except Exception as e:
    st.error(f"An error occurred in the calculation: {str(e)}")
    st.write("Please check your inputs and try again.")

# Add a footer
st.markdown("---")
st.caption("Option Redemption Calculator © 2024")
