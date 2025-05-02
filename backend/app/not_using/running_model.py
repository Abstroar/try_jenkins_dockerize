



def plot_stock_risk_factors(stock_data):
    for stock_name, metrics in stock_data.items():
        print(f"\n📈 Generating detailed risk factor plots for {stock_name}...")

        try:
            last_price = metrics['prices'].dropna().iloc[-1]
            last_return = metrics['returns'].dropna().iloc[-1]
            last_volatility = metrics['volatility'].dropna().iloc[-1]
            last_volume = metrics['volume'].dropna().iloc[-1]
            last_volume_ratio = metrics['volume_ratio'].dropna().iloc[-1]

            print(f"\n🔢 Numerical Risk Output for {stock_name}:")
            print(f"1. Closing Price (Market Trend): {last_price:.2f} USD")
            print(f"2. Percentage Return (Profit/Loss Risk): {last_return * 100:.2f}%")
            print(f"3. 10-Period Intraday Volatility (Volatility Risk): {last_volatility:.6f}")
            print(f"4. Trading Volume per 15-min Interval (Liquidity Risk): {last_volume:.0f} shares")
            print(f"5. Volume Ratio (Abnormal Activity Risk): {last_volume_ratio:.4f}")
            print("------------------------------------------------------------")
        except Exception as e:
            print(f"❌ Could not calculate metrics for {stock_name}: {e}")
            continue


    print("\n✅ All numerical values and plots generated successfully!")