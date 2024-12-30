from flask import Flask, render_template, request, redirect, url_for
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///geological_units.db")

def load_geological_units():
    units = {}
    reader = db.execute("SELECT * FROM geological_units")

    for row in reader:
        formation_name = row["formation"].lower()

        thickness = None
        if row['thickness_min'] is not None and row['thickness_max'] is not None:
            thickness = f"{row['thickness_min']}-{row['thickness_max']}"

        TOC = None
        if row['TOC_min'] is not None and row['TOC_max'] is not None:
            TOC = f"{row['TOC_min']}-{row['TOC_max']}"

        units[formation_name] = {
            "thickness": thickness,
            "TOC": TOC,
            "age": row["age"],
            "lithology": row["lithology"],
            "porosity": row["porosity"],
            "permeability": row["permeability"],
            "structural_features": row["structural_features"],
            "hydrocarbon_potential": row["hydrocarbon_potential"],
            "paleoenvironment": row["paleoenvironment"]
        }

    return units

def load_bibliography():
    bibliography = {}
    results = db.execute("SELECT * FROM formation_bibliography")

    for row in results:
        bibliography[row["formation"].lower()] = row["bibliography"]
    return bibliography


geological_units = load_geological_units()
bibliography = load_bibliography()


def find_matching_units(units, user_unit):
    """
    Find geological units that match the user's input based on their properties.
    """
    matching_units = []

    for unit, properties in units.items():
        match = True
        for key, user_value in user_unit.items():
            if user_value is not None:
                key = key.strip()
                prop_value = properties.get(key)

                if not matches_property(key, user_value, prop_value):
                    match = False
                    break

        if match:
            matching_units.append(unit)

    return matching_units

def matches_property(key, user_value, prop_value):
    """
    Compare properties values of the CSV file with the user's input.
    Supports exact matches and range comparisons.
    """
    if prop_value is None:
        return False

    if key in ['thickness', 'TOC']:
        try:
            min_value, max_value = map(float, prop_value.split('-'))
        except ValueError:
            return False

        if isinstance(user_value, (int, float)):
            return min_value <= user_value <= max_value

        elif isinstance(user_value, str) and '-' in user_value:
            try:
                user_min, user_max = map(float, user_value.split('-'))
            except ValueError:
                return False

            return user_min <= max_value and user_max >= min_value

    if isinstance(prop_value, str):
        return user_value.lower() in prop_value.lower()

    return user_value == prop_value

def validate_numerical_input(key, value):
    try:
        if '-' in value:
            min_value, max_value = map(float, value.split('-'))
            if min_value < 0 or max_value < 0:
                return False  # Valores negativos no son válidos
            return min_value <= max_value
        else:
            value = float(value)
            return value >= 0  # Validación para números positivos
    except ValueError:
        return False  # Error de conversión a flotante

def sanitize_input(value):
    return ''.join(e for e in value if e.isalnum()).lower()  # Elimina caracteres no alfanuméricos y pasa a minúsculas


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/find_unit', methods=['GET', 'POST'])
def find_unit():
    prompts = {
        'age': 'Age',
        'lithology': 'Lithology',
        'porosity': 'Porosity',
        'permeability': 'Permeability',
        'thickness': 'Thickness',
        'structural_features': 'Structural Features',
        'hydrocarbon_potential': 'Hydrocarbon Potential',
        'TOC': 'TOC',
        'paleoenvironment': 'Paleoenvironment'
    }

    if request.method == 'POST':
        user_unit = {}

        for key in prompts.keys():
            user_input = request.form.get(key)
            if user_input:
                try:
                    if '-' in user_input:
                        user_unit[key] = user_input.strip()
                    else:
                        user_unit[key] = float(user_input)
                except ValueError:
                    user_unit[key] = user_input.strip().lower()

        matches = find_matching_units(geological_units, user_unit)

        capitalized_matches = [match.title() for match in matches]

        if capitalized_matches:
            return render_template("matching_units.html", matches=capitalized_matches, user_inputs=user_unit)
        else:
            return render_template("no_matches.html", user_inputs=user_unit)

    return render_template("find_unit.html", prompts=prompts)

@app.route('/view_properties', methods=['GET', 'POST'])
def view_properties():
    formations = db.execute("SELECT formation FROM geological_units")

    if request.method == 'POST':
        selected_formation = request.form.get('formation_name')

        if selected_formation is None:
            return "Formation name not provided", 400

        selected_formation = selected_formation.strip().lower()

        formation_properties = db.execute("SELECT * FROM geological_units WHERE LOWER(formation) = ?", (selected_formation,))

        if not formation_properties:
            return "Formation not found", 404

        formation_properties = formation_properties[0]
        del formation_properties['formation']

        bibliography_entry = db.execute("SELECT bibliography FROM formation_bibliography WHERE LOWER(formation) = ?", (selected_formation,))

        return render_template("properties.html", properties=formation_properties, formation_name=selected_formation, bibliography_entry=bibliography_entry[0]['bibliography'] if bibliography_entry else None)

    return render_template('view_properties.html', geological_units=[f['formation'] for f in formations])

@app.route('/properties/<formation_name>', methods=['GET', 'POST'])
def properties(formation_name):
    print(f"Recibido formation_name: {formation_name}")
    formation_name = formation_name.lower()

    properties = db.execute("SELECT * FROM geological_units WHERE LOWER(formation) = ?", (formation_name,))

    if not properties:
        return redirect(url_for('home'))

    formation_properties = properties[0]
    if 'formation' in formation_properties:
        del formation_properties['formation']

    bibliography_entry = db.execute("SELECT bibliography FROM formation_bibliography WHERE LOWER(formation) = ?", (formation_name,))

    return render_template('properties.html', properties=properties[0], formation_name=formation_name, bibliography_entry=bibliography_entry[0]['bibliography'] if bibliography_entry else None)

@app.route('/all_units')
def all_units():
    return render_template("all_units.html", units=geological_units)

@app.route('/interactive_map')
def interactive_map():
    return render_template("interactive_map.html")

@app.route('/outcrops')
def outcrops_map():
    return render_template("outcrops.html")

if __name__ == "__main__":
    app.run(debug=True)
