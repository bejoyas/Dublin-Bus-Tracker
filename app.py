from flask import Flask, render_template, request,jsonify, session
from bus_logic import getService, getStopId, list_out
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = "super-secret-key"
@app.after_request
def disable_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 🔹 Replace this with your existing logic
def get_bus_schedule(bus_stop_no: int) -> str:
    
    # Example output
    stop_id = getStopId(bus_stop_no)
    resp = getService (stop_id[0],stop_id[1])
    out = list_out (resp)
    return out
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    bus_stop_no = session.get("bus_stop_no")
    if request.method == "POST":
        try:
            bus_stop_no = int(request.form["bus_stop"])
            session["bus_stop_no"] = bus_stop_no
            result = get_bus_schedule(bus_stop_no)
        except ValueError:
            result = "Please enter a valid integer bus stop number."

    return render_template("index.html", result=result,bus_stop_no=bus_stop_no )

@app.route("/refresh", methods=["POST"])
def refresh():
    if "bus_stop_no" not in session:
        return jsonify({"error": "No stop selected"}), 400

    bus_stop_no = session["bus_stop_no"]
    result = get_bus_schedule(bus_stop_no)

    return jsonify({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "result": result
    })
if __name__ == "__main__":
    app.run(debug=True)
