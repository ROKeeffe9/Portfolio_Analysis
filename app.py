import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect 
from logic import validate_and_convert_input, run_portfolio_logic

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#CSRF Protection
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")

csrf = CSRFProtect(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    error_check = None
    error_message = None
    
    portfolio_returns = []
    portfolio_risks = []
    w1_array = []
    w2_array = []
    sharpe_w1 = ""
    sharpe_w2 = ""
    min_risk_w1 = ""
    min_risk_w2 = ""

    # Get raw data -> for validation + sticky numbers for input boxes
    raw_data = {
        "er_a": request.form.get("er_a", ""),
        "er_b": request.form.get("er_b", ""),
        "std_a": request.form.get("std_a", ""),
        "std_b": request.form.get("std_b", ""),
        "c": request.form.get("c", ""),
        "rfr": request.form.get("rfr", "")
    }

    if request.method == "POST":
        # Validate all inputs, and convert to right format
        r1, error_r1, error_msg_r1 = validate_and_convert_input(raw_data["er_a"].strip(), "Expected return of stock A")
        r2, error_r2, error_msg_r2 = validate_and_convert_input(raw_data["er_b"].strip(), "Expected return of stock B")
        std1, error_std1, error_msg_std1 = validate_and_convert_input(raw_data["std_a"].strip(), "Standard deviation of stock A")
        std2, error_std2, error_msg_std2 = validate_and_convert_input(raw_data["std_b"].strip(), "Standard deviation of stock B")
        c, error_c, error_msg_c = validate_and_convert_input(raw_data["c"].strip(), "Correlation coefficient")
        rfr, error_rfr, error_msg_rfr = validate_and_convert_input(raw_data["rfr"].strip(), "Risk free rate")

        # Create the complete error message from the individual error messages
        error_msg = [error_msg_r1, error_msg_r2, error_msg_std1, error_msg_std2, error_msg_c, error_msg_rfr]
        error_message = "\n".join(msg for msg in error_msg if msg is not None)
    

        # Check if an error occured i.e. an invalid input
        if any(value is not None for value in [error_r1, error_r2, error_std1, error_std2, error_c, error_rfr]):
            error_check="error"
        else:
            # Convert variables to float
            r1, r2, std1, std2, c, rfr = map(float, [r1, r2, std1, std2, c, rfr])

            # Call the logic file for calculations
            portfolio_returns, portfolio_risks, w1_array, w2_array, sharpe_w1, sharpe_w2, min_risk_w1, min_risk_w2 = run_portfolio_logic(r1, r2, std1, std2, c, rfr)


    return render_template("index.html", 
                           portfolio_returns=portfolio_returns, 
                           portfolio_risks=portfolio_risks,
                           w1_array=w1_array, 
                           w2_array=w2_array, 
                           error_check=error_check,
                           error_message=error_message,
                           sharpe_w1=sharpe_w1, 
                           sharpe_w2=sharpe_w2,
                           min_risk_w1=min_risk_w1, 
                           min_risk_w2=min_risk_w2,
                           # Sticky numbers for UI
                           r1=raw_data["er_a"],
                           r2=raw_data["er_b"],
                           std1=raw_data["std_a"],
                           std2=raw_data["std_b"],
                           c=raw_data["c"],
                           rfr=raw_data["rfr"])
                           

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
