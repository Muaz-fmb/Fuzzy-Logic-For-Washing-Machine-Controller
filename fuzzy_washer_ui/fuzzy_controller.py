# fuzzy_controller.py
import matplotlib
matplotlib.use('Agg') # SET BACKEND BEFORE IMPORTING PYPLOT
import warnings # Import warnings module

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt # Import pyplot AFTER setting backend
import os
import time

# --- Suppress Matplotlib Warning ---
warnings.filterwarnings("ignore", message="FigureCanvasAgg is non-interactive, and thus cannot be shown", category=UserWarning)


# --- Define Antecedents and Consequent (Global Scope for Reuse) ---
dirtiness = ctrl.Antecedent(np.arange(0, 101, 1), 'dirtiness')
load = ctrl.Antecedent(np.arange(0, 101, 1), 'load')
time_output = ctrl.Consequent(np.arange(0, 61, 1), 'time') # Renamed to avoid conflict

# --- Define Membership Functions ---
dirtiness.automf(3, names=['SD', 'MD', 'LD'])
load.automf(3, names=['SL', 'ML', 'LL'])
time_output.automf(5, names=['VS', 'S', 'M', 'L', 'VL'])

# --- Define the Rules ---
rule1 = ctrl.Rule(dirtiness['SD'] & load['SL'], time_output['VS'])
rule2 = ctrl.Rule(dirtiness['SD'] & load['ML'], time_output['M'])
rule3 = ctrl.Rule(dirtiness['SD'] & load['LL'], time_output['L'])
rule4 = ctrl.Rule(dirtiness['MD'] & load['SL'], time_output['S'])
rule5 = ctrl.Rule(dirtiness['MD'] & load['ML'], time_output['M'])
rule6 = ctrl.Rule(dirtiness['MD'] & load['LL'], time_output['L'])
rule7 = ctrl.Rule(dirtiness['LD'] & load['SL'], time_output['M'])
rule8 = ctrl.Rule(dirtiness['LD'] & load['ML'], time_output['L'])
rule9 = ctrl.Rule(dirtiness['LD'] & load['LL'], time_output['VL'])

# --- Create the Control System (Only needs to be created once) ---
rules_list = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]
if not rules_list:
    raise ValueError("Rules list is empty. Cannot create ControlSystem.")

washing_ctrl = ctrl.ControlSystem(rules_list)

# --- Function to Calculate Washing Time ---
def calculate_washing_time(dirtiness_input, load_input):
    """Calculates the washing time using the fuzzy control system."""
    try:
        washing_sim = ctrl.ControlSystemSimulation(washing_ctrl)

        washing_sim.input['dirtiness'] = float(dirtiness_input)
        washing_sim.input['load'] = float(load_input)

        washing_sim.compute()

        calculated_time = washing_sim.output['time']
        plot_path = generate_output_plot(washing_sim)

        return calculated_time, plot_path
    except Exception as e:
        print(f"Error during fuzzy calculation: {e}")
        return None, None

# --- Function to Generate and Save the Output Plot ---
def generate_output_plot(simulation_instance):
    """Generates and saves the fuzzy output plot."""
    try:
        img_dir = os.path.join('static', 'images')
        os.makedirs(img_dir, exist_ok=True)

        relative_plot_path = os.path.join('images', 'output_plot.png')
        absolute_plot_path = os.path.join('static', relative_plot_path)

        fig, ax = plt.subplots(figsize=(8, 3))
        time_output.view(sim=simulation_instance, ax=ax)
        ax.set_title('Output Washing Time Distribution')
        ax.set_xlabel('Washing Time (minutes)')
        ax.set_ylabel('Membership Degree')
        plt.tight_layout()

        plt.savefig(absolute_plot_path)
        plt.close(fig)

        timestamp = int(time.time())
        return f"{relative_plot_path}?v={timestamp}"

    except Exception as e:
        print(f"Error generating plot: {e}")
        plt.close()
        return None

# Example Usage (for testing the module directly)
if __name__ == '__main__':
    test_time, plot = calculate_washing_time(60, 70)
    if test_time is not None:
        print(f"Test Washing Time: {test_time}")
        print(f"Plot saved to: static/{plot.split('?')[0]}")

    test_time_2, plot_2 = calculate_washing_time(30, 20)
    if test_time_2 is not None:
        print(f"Test Washing Time 2: {test_time_2}")
        print(f"Plot saved to: static/{plot_2.split('?')[0]}")