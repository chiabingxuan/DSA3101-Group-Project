import sys
import os
from flask import Flask, request, render_template
from src.predict_disruption_impact import main


# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = Flask(__name__)
app.config.from_object("config.ProdConfig")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/initial-data-exploration-visualisations")
def initial_data_exploration_visualisations():
    return render_template("initial-data-exploration-visualisations.html")


@app.route("/drivers-of-satisfaction-visualisations")
def drivers_of_satisfaction_visualisations():
    return render_template("drivers-of-satisfaction-visualisations.html")


@app.route("/user-segmentation-visualisations")
def user_segmentation_visualisations():
    return render_template("user-segmentation-visualisations.html")


@app.route("/tableau-visualisations")
def tableau_visualisations():
    return render_template("tableau-visualisations.html")


@app.route("/folium-visualisations")
def folium_visualisations():
    return render_template("folium-visualisations.html")


@app.route("/kpi-dashboard")
def kpi_dashboard():
    return render_template("kpi-dashboard.html")


@app.route("/other-visualisations")
def other_visualisations():
    return render_template("other-visualisations.html")


@app.route("/route-optimisation-algo-and-simulation")
def route_optimisation_algo_and_simulation():
    return render_template("route-optimisation-algo-and-simulation.html")


@app.route("/disruption-impact-model", methods=["GET", "POST"])
def disruption_impact_model():
    if request.method == "GET":
        return render_template("disruption-impact-model.html")
    # POST request: Estimate impact of disruption
    bus_stop = request.form.get("bus-stop")
    delay = int(request.form.get("delay"))
    decay_factor = float(request.form.get("decay-factor"))
    max_depth = int(request.form.get("max-depth"))
    estimated_delays = main(start_node=bus_stop, initial_delay=delay, decay_factor=decay_factor, max_depth=max_depth)
    return render_template("disruption-impact-model-results.html", bus_stop=bus_stop, delay=delay, decay_factor=decay_factor, max_depth=max_depth, estimated_delays=estimated_delays)


# Routes for HTML visualisations timelapses
@app.route("/html-visualisations/<filename>")
def html_visualisations(filename):
    return render_template(f"{filename}.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)