# app.py
from flask import Flask, render_template, request, jsonify, url_for # Import url_for
import os
import time

# --- Matplotlib Backend Configuration ---
# IMPORTANT: Set the backend *before* importing pyplot or any module
# that might implicitly import it (like skfuzzy.control.view)
import matplotlib
matplotlib.use('Agg') # Use the Agg backend for non-interactive plotting

import matplotlib.pyplot as plt # Import pyplot AFTER setting backend

# --- Local Module Import ---
from fuzzy_controller import calculate_washing_time, dirtiness, load, time_output # Import necessary components

# --- Flask App Initialization ---
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Disable caching for static files during development

# --- Directory Setup ---
# Ensure the static/images directory exists on startup
img_dir = os.path.join('static', 'images')
os.makedirs(img_dir, exist_ok=True)

# --- Flask Routes ---
@app.route('/')
def index():
    """Renders the main page."""
    # You can set default values here if needed, or calculate them.
    # For simplicity, we'll just pass default slider values to the template.
    # initial_time, initial_plot = calculate_washing_time(60, 70) # Example if needed
    return render_template('index.html',
                           dirtiness_val=60, # Default slider position for dirtiness
                           load_val=70)      # Default slider position for load
                           # washing_time=initial_time, # Uncomment if calculating initial values
                           # plot_path=initial_plot)     # Uncomment if calculating initial values

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handles the AJAX request to calculate washing time."""
    try:
        data = request.get_json()
        if not data:
             return jsonify({'error': 'No input data received.'}), 400

        dirtiness_in = float(data.get('dirtiness', 60)) # Default to 60 if not provided
        load_in = float(data.get('load', 70))         # Default to 70 if not provided

        # Validate inputs (basic range check)
        if not (0 <= dirtiness_in <= 100 and 0 <= load_in <= 100):
             return jsonify({'error': 'Input values must be between 0 and 100.'}), 400

        # Calculate using the fuzzy controller module
        calculated_time, plot_path = calculate_washing_time(dirtiness_in, load_in)

        if calculated_time is None:
             # Log the error on the server side if needed
             print(f"Fuzzy calculation failed for inputs: dirtiness={dirtiness_in}, load={load_in}")
             return jsonify({'error': 'Fuzzy logic calculation failed on the server.'}), 500

        # Return result as JSON
        return jsonify({
            'washing_time': calculated_time,
            'plot_path': plot_path # Path relative to static folder (e.g., 'images/output_plot.png?v=123...')
        })

    except ValueError:
         return jsonify({'error': 'Invalid input data type. Ensure values are numeric.'}), 400
    except Exception as e:
        # Log the full error for debugging on the server
        print(f"Error in /calculate route: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'An internal server error occurred.'}), 500

# --- Route to serve membership function plots (Optional but nice for demo) ---
@app.route('/plot/<variable_name>')
def serve_plot(variable_name):
    """Generates and serves membership function plots as HTML img tags."""
    plot_dir = os.path.join('static', 'images')
    # No need to create dir here again, done at startup, but doesn't hurt

    plot_filename = f"mf_{variable_name}.png"
    absolute_plot_path = os.path.join(plot_dir, plot_filename)

    fig = None # Initialize fig to None to avoid potential UnboundLocalError

    try:
        # Create a new figure and axes for each plot request
        fig, ax = plt.subplots(figsize=(8, 3))

        if variable_name == 'dirtiness':
            dirtiness.view(ax=ax) # Use the imported fuzzy variable
            ax.set_title('Dirtiness Membership Functions') # Add title
        elif variable_name == 'load':
            load.view(ax=ax)      # Use the imported fuzzy variable
            ax.set_title('Load Size Membership Functions')
        elif variable_name == 'time':
            time_output.view(ax=ax) # Use the imported fuzzy variable
            ax.set_title('Washing Time Membership Functions')
        else:
            plt.close(fig) # Close the unnecessary figure
            return "Invalid variable name", 404

        # Customize plot appearance (optional)
        ax.set_ylabel('Membership Degree')
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout() # Adjust layout

        # Save the plot
        plt.savefig(absolute_plot_path)

        # IMPORTANT: Close the figure after saving to release memory
        plt.close(fig)

        # Add timestamp for cache busting in the URL
        timestamp = int(time.time())
        # Use url_for to generate the correct static URL
        image_url = url_for('static', filename=f'images/{plot_filename}')

        # Return an HTML img tag pointing to the generated plot
        return f'<img src="{image_url}?v={timestamp}" alt="{variable_name.capitalize()} membership functions" style="max-width: 100%; height: auto;">'

    except Exception as e:
        print(f"Error generating membership plot for {variable_name}: {e}")
        if fig: # Check if fig was created before trying to close it
            plt.close(fig)
        return f"Error generating plot for {variable_name}", 500


# --- Main Execution Block ---
if __name__ == '__main__':
    # Set port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Use host='0.0.0.0' to make the app accessible on your local network
    # Set debug=True for development (provides auto-reloading and detailed error pages)
    # Set debug=False for production deployment
    app.run(debug=True, host='0.0.0.0', port=port)