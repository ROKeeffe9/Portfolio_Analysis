def validate_and_convert_input(input_data, field_name):
    try:
        val = float(input_data)
        
        # Check for Infinity/NaN 
        import math
        if not math.isfinite(val):
            return None,"error", f"*Invalid value in {field_name}: Infinity/NaN not allowed"

        # Context specific validation - ensure input makes sense for value it represents
        if field_name == "Correlation coefficient":
            if not -1 <= val <= 1:
                return None, "error", "*Correlation must be between -1 and 1"
        
        if field_name in ["Standard deviation of stock A", "Standard deviation of stock B"] and val < 0:
            return None, "error", "*Standard Deviation cannot be negative"

        # If successful
        return val, None, None

    except (ValueError, TypeError):
        return None, "error", f"*Invalid input in {field_name}: Must be a number"





def run_portfolio_logic(r1, r2, std1, std2, c, rfr):
    # Create array to control each point on graph
    allocations = [round(x, 2) for x in list(map(lambda x: x/100, range(1, 101)))]

    # Create empty lists to be populated and used in graph
    portfolio_returns = []
    portfolio_risks = []
    w1_array = []
    w2_array = []
    sharpe_array = []

    # Iterate through allocation to get figures for each point on graph and for calculation of table figures
    for allocation in allocations:
        w1 = allocation
        w2 = 1 - w1
        portfolio_return = w1 * r1 + w2 * r2
        portfolio_risk = (w1**2 * std1**2 + w2**2 * std2**2 + 2 * w1 * w2 * std1 * std2 * c)**0.5
        portfolio_returns.append(portfolio_return)
        portfolio_risks.append(portfolio_risk)
        w1_array.append(w1)
        w2_array.append(w2)

        # Ensure no divide by 0 error
        if portfolio_risk > 0:
            sharpe = (portfolio_return - rfr) / portfolio_risk
        else:
            sharpe = 0
        sharpe_array.append(sharpe)

    # Calculate max sharpe and minimum risk weightings
    max_sharpe = max(sharpe_array)
    max_sharpe_index = sharpe_array.index(max_sharpe)
    sharpe_w1 = round(w1_array[max_sharpe_index], 2)
    sharpe_w2 = round(w2_array[max_sharpe_index], 2)

    min_risk = min(portfolio_risks)
    min_risk_index = portfolio_risks.index(min_risk)
    min_risk_w1 = round(w1_array[min_risk_index], 2)
    min_risk_w2 = round(w2_array[min_risk_index], 2)

    return portfolio_returns, portfolio_risks, w1_array, w2_array, sharpe_w1, sharpe_w2, min_risk_w1, min_risk_w2
