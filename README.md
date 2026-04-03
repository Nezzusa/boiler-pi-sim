# Water Boiler PI Control Simulation

Python-based thermal simulation of a closed boiler system. Features a discrete PI control algorithm and interactive dashboard powered by **Dash** and **Plotly**.

## About
The application allows visualization of the temperature change over time, based on selected parameters of the PI controller and boiler specifications (size and heater). Main purpose of the application is to show how the PI controller automatically regulates heating power, to keep flowing water at desired temperature.

### Main features:
* **Physics Simulation:** Accounts for water heat capacity, heater power, and fluid flow.
* **PI Controller:** Enables testing the impact of proportional gain ($K_p$) and integral time ($T_i$) on system stability.
* **Interactive Dashboard:** Temperature and power consumption charts generated using Plotly.

## Technologies
* **Python 3.14**
* **Dash 4.1.0** 
* **Plotly 6.6.0**

## How to run?
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nezzusa/boiler-pi-sim.git
   cd boiler-pi-sim
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the script**
   ```bash
   python main.py
   ```

