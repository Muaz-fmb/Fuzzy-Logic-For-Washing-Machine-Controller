// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const dirtinessSlider = document.getElementById('dirtiness');
    const loadSlider = document.getElementById('load');
    const dirtinessValueSpan = document.getElementById('dirtiness-value');
    const loadValueSpan = document.getElementById('load-value');
    const calculateBtn = document.getElementById('calculate-btn');
    const washTimeOutput = document.getElementById('wash-time-output');
    const plotContainer = document.getElementById('plot-container');
    const outputPlotImg = document.getElementById('output-plot');
    const plotPlaceholder = document.getElementById('plot-placeholder');

    // Function to update slider value display
    function updateSliderValue(slider, span) {
        span.textContent = slider.value;
    }

    // Initial display update
    updateSliderValue(dirtinessSlider, dirtinessValueSpan);
    updateSliderValue(loadSlider, loadValueSpan);

    // Event listeners for sliders
    dirtinessSlider.addEventListener('input', () => updateSliderValue(dirtinessSlider, dirtinessValueSpan));
    loadSlider.addEventListener('input', () => updateSliderValue(loadSlider, loadValueSpan));

    // Event listener for the calculate button (AJAX)
    calculateBtn.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent default form submission if it were a form

        const dirtiness = dirtinessSlider.value;
        const load = loadSlider.value;

        // Show loading state (optional)
        washTimeOutput.textContent = "Calculating...";
        outputPlotImg.style.display = 'none';
        plotPlaceholder.textContent = 'Calculating...';
        calculateBtn.disabled = true;
        calculateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculating...';


        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ dirtiness: dirtiness, load: load }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            // Update the UI with results
            washTimeOutput.textContent = `${result.washing_time.toFixed(1)} minutes`;

            if (result.plot_path) {
                outputPlotImg.src = `${window.location.origin}/static/${result.plot_path}`; // Construct full URL
                outputPlotImg.style.display = 'block';
                plotPlaceholder.style.display = 'none'; // Hide placeholder
                 // Force reload if src is the same but content changed (due to timestamp)
                outputPlotImg.onload = () => {}; // Clear previous onload if any
                outputPlotImg.onerror = () => { plotPlaceholder.textContent = 'Error loading plot.'; plotPlaceholder.style.display = 'block';};
            } else {
                 outputPlotImg.style.display = 'none';
                 plotPlaceholder.textContent = 'Plot not available.';
                 plotPlaceholder.style.display = 'block';
            }


        } catch (error) {
            console.error('Error:', error);
            washTimeOutput.textContent = "Error!";
            plotPlaceholder.textContent = `Error calculating: ${error.message}`;
            plotPlaceholder.style.display = 'block';
            outputPlotImg.style.display = 'none';
        } finally {
             // Restore button state
             calculateBtn.disabled = false;
             calculateBtn.innerHTML = '<i class="fas fa-calculator"></i> Calculate Wash Time';
        }
    });

    // --- Load Membership Function Plots ---
    async function loadMFPlot(variableName) {
        const container = document.getElementById(`mf-${variableName}`);
        if (!container) return;

        try {
            const response = await fetch(`/plot/${variableName}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const htmlContent = await response.text();
            container.innerHTML = htmlContent; // Insert the img tag returned by Flask
        } catch (error) {
            console.error(`Error loading MF plot for ${variableName}:`, error);
            container.textContent = `Error loading ${variableName} plot.`;
        }
    }

    loadMFPlot('dirtiness');
    loadMFPlot('load');
    loadMFPlot('time');

});