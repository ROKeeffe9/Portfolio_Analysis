# Portfolio Analysis

A Flask-based web application that visualises the efficient frontier for a two asset portfolio and calculates optimal portfolio allocations based on minimum variance and Sharpe ratio.

## Overview

This application allows users to input financial metrics for two assets and generates:

- The portfolio efficient frontier 
- Maximum Sharpe ratio allocation
- Minimum variance allocation

The results are displayed using an interactive scatter plot using Chart.js.

---

## Features

- Input validation (handles invalid, NaN, and infinite values)
- Efficient frontier calculation
- Maximum Sharpe ratio portfolio calculation
- Minimum variance portfolio calculation
- Interactive data visualisation
- CSRF protection 

---

## Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Libraries: Chart.js, Flask-WTF 

---

## Project Structure

project/
│ <br>
├── app.py # Flask application for routing and request handling <br>
├── logic.py # Portfolio calculations and input validation <br>
| <br>
├── templates/ <br>
│ └── index.html # UI <br>
│ <br>
├── static/ <br>
│ └── styles.css # Styling <br>

---

## Installation + Setup

### 1. Clone the repository



### 2. Install dependencies

pip install flask flask-wtf

### 3. Set environment variables

export SECRET_KEY=your_secret_key
export FLASK_DEBUG=1

### 4. Run the application

python app.py

Then open:
http://127.0.0.1:5000/

---

## How It Works

Upon loading the web page, the user is presented with six input fields:
- Expected returns for assets A and B
- Standard deviations for assets A and B
- Correlation coefficient
- Risk-free rate

Once inputs have been given, the application sends them to be validated server-side. If invalid, error message(s) are displayed. If valid, the inputs are sent to a logic function to be used in the calculations.

The application calculates portfolio metrics using standard portfolio theory. 

**Portfolio return:**

Rp = w1R1 + w2R2

**Portfolio risk:**

σp = √(w1²σ1² + w2²σ2² + 2w1w2σ1σ2ρ)

The application iterates through different asset weight combinations to construct the efficient frontier and identify:
- The minimum variance portfolio
- The maximum Sharpe ratio portfolio

Results are displayed as a risk-return chart and a table of optimal portfolio weightings.

---

## Future Improvements

- Support for more than two assets
- Real-time market data integration
- User account creation, login authentication and saved portfolios

---

## Author

Ronan O'Keeffe

