# Fuzzy-Logic-For-Washing-Machine-Controller
Fuzzy logic-based washing machine controller using Mamdani inference. Determines washing time based on dirtiness and load size. Implements fuzzification, rule evaluation, aggregation, and defuzzification. Includes predefined membership functions and nine fuzzy rules for decision-making. Ideal for learning fuzzy systems and control applications.

# fuzzy_washer_ui

This project demonstrates a fuzzy logic controller for a washing machine, implemented using Python with the `scikit-fuzzy` library and presented through an interactive web interface built with Flask.

The controller takes two inputs:
*   **Degree of Dirtiness:** How dirty the clothes are (scale 0-100).
*   **Size of Load:** The amount of clothes in the machine (scale 0-100).

Based on these inputs and a set of fuzzy rules, it calculates the recommended **Washing Time** (scale 0-60 minutes, representing the fuzzy output range).

## Features

*   **Interactive UI:** Simple web interface built with Flask, HTML, CSS, and JavaScript.
*   **Slider Inputs:** Easy adjustment of Dirtiness and Load Size using sliders.
*   **Real-time Value Display:** See the current slider values update instantly.
*   **Fuzzy Logic Core:** Utilizes `scikit-fuzzy` for:
    *   Defining linguistic variables and membership functions (automatically generated trapezoidal/triangular).
    *   Implementing fuzzy IF-THEN rules.
    *   Performing Mamdani fuzzy inference.
    *   Defuzzification (using the Centroid method by default) to get a crisp output value.
*   **Dynamic Calculation:** Calculates washing time on demand via an AJAX request without full page reloads.
*   **Result Visualization:** Displays the calculated crisp washing time.
*   **Fuzzy Output Plot:** Shows the aggregated fuzzy output set and the defuzzified result graphically (generated using Matplotlib).
*   **Membership Function Display:** Shows the plots for the input (Dirtiness, Load) and output (Time) membership functions.

## How it Works

1.  **User Interface (HTML/CSS/JS):** The user interacts with sliders in the `index.html` page. JavaScript captures the slider values.
2.  **AJAX Request (JS):** When the "Calculate" button is pressed, JavaScript sends the current slider values (dirtiness, load) to the Flask backend via an asynchronous `fetch` request to the `/calculate` endpoint.
3.  **Flask Backend (`app.py`):**
    *   Receives the input values.
    *   Calls the `calculate_washing_time` function from the `fuzzy_controller.py` module.
4.  **Fuzzy Logic Controller (`fuzzy_controller.py`):**
    *   **Fuzzification:** The crisp input values (e.g., Dirtiness = 60) are mapped to the defined membership functions (SD, MD, LD) to determine their degree of membership.
    *   **Rule Evaluation:** The fuzzy rules (e.g., `IF Dirtiness is MD AND Load is LL THEN Time is L`) are evaluated based on the fuzzified inputs using fuzzy operators (AND typically uses `fmin`).
    *   **Aggregation:** The outputs of all triggered rules are combined (typically using `fmax`) to form a single fuzzy set for the output variable (Washing Time).
    *   **Defuzzification:** The aggregated fuzzy output set is converted back into a single crisp numerical value (e.g., 36.7 minutes) using a defuzzification method (like Centroid).
    *   **Plot Generation:** A plot visualizing the aggregated output fuzzy set and the defuzzified result is generated using Matplotlib and saved as an image file (`output_plot.png`).
5.  **Flask Response (`app.py`):** The Flask backend receives the calculated time and the path to the generated plot from the controller module. It sends this information back to the browser as a JSON response.
6.  **UI Update (JS):** The JavaScript in the browser receives the JSON response and updates the relevant sections of the HTML page to display the calculated washing time and the generated plot image.
7.  **Membership Function Plots:** Separate Flask routes (`/plot/...`) generate and serve images of the input and output membership functions, which are loaded by JavaScript when the page initially loads.

## Technologies Used

*   **Python:** Backend programming language.
*   **Flask:** Micro web framework for the backend server.
*   **scikit-fuzzy:** Python library for fuzzy logic operations.
*   **NumPy:** Required by scikit-fuzzy for numerical operations.
*   **Matplotlib:** Used by scikit-fuzzy (and directly) for generating plots.
*   **HTML:** Structure of the web page.
*   **CSS:** Styling the web page for a more realistic look.
*   **JavaScript:** Frontend interactivity (slider updates, AJAX requests, UI updates).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd fuzzy_washer_ui
    ```
2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install Flask scikit-fuzzy matplotlib numpy networkx scipy
    ```
    *(Alternatively, create a `requirements.txt` file with the above libraries listed and run `pip install -r requirements.txt`)*
4.  **Run the Flask application:**
    ```bash
    flask run
    ```
    *(Or `python app.py`)*

## Usage

1.  Open your web browser and navigate to the address provided by Flask (usually `http://127.0.0.1:5000` or `http://localhost:5000`).
2.  Adjust the "Dirtiness" and "Load Size" sliders to your desired input values.
3.  Click the "Calculate Wash Time" button.
4.  The "Recommended Wash Time" and the "Fuzzy Output Distribution" plot will update below the controls.
5.  Scroll down to view the predefined Membership Function plots.