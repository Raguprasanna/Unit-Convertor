from flask import Flask, render_template, request

app = Flask(__name__)

unit_groups = {
    "length": {
        "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
        "inch": 0.0254, "ft": 0.3048, "yard": 0.9144, "mile": 1609.34
    },
    "weight": {
        "mg": 0.000001, "g": 0.001, "kg": 1, "ton": 1000,
        "pound": 0.453592, "ounce": 0.0283495
    },
    "temperature": {
        "C": "C", "F": "F", "K": "K"
    }
}

def convert(value, from_u, to_u):
    if from_u in ["C", "F", "K"]:
        if from_u == "C": c = value
        elif from_u == "F": c = (value - 32) * 5 / 9
        elif from_u == "K": c = value - 273.15
        if to_u == "C": return c
        elif to_u == "F": return (c * 9 / 5) + 32
        elif to_u == "K": return c + 273.15
    for group, units in unit_groups.items():
        if from_u in units and to_u in units:
            return (value * units[from_u]) / units[to_u]
    raise ValueError(f"Cannot convert between {from_u} and {to_u}")

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    selected_category = "length"
    from_u = to_u = value = None
    if request.method == "POST":
        try:
            value = float(request.form["value"])
            from_u = request.form["from_unit"]
            to_u = request.form["to_unit"]
            selected_category = request.form.get("category", "length")
            result = convert(value, from_u, to_u)
        except Exception as e:
            error = str(e)
    return render_template("index.html", unit_groups=unit_groups, result=result,
                           error=error, selected_category=selected_category,
                           from_u=from_u, to_u=to_u, value=value)

if __name__ == "__main__":
    app.run(debug=True)