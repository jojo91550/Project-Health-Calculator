from flask import Flask, request, jsonify, render_template_string
from health_utils import calculate_bmi, calculate_bmr

app = Flask(__name__)

# HTML template pour la page d'accueil
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculateur de Santé</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #2980b9;
            margin-top: 30px;
        }
        .calculator {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 16px;
        }
        button:hover {
            background-color: #2980b9;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-left: 4px solid #3498db;
            background-color: #eaf6ff;
            display: none;
        }
        code {
            background-color: #f1f1f1;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }
        pre {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .api-details {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Calculateur de Santé - API</h1>
    
    <p>Bienvenue sur l'API de Calculateur de Santé. Cette API fournit des calculs pour l'Indice de Masse Corporelle (IMC) et le Métabolisme de Base (MB).</p>
    
    <h2>Calculateur d'IMC</h2>
    <div class="calculator">
        <form id="bmi-form">
            <label for="height-bmi">Taille (en mètres):</label>
            <input type="number" id="height-bmi" step="0.01" min="0.5" max="2.5" placeholder="Exemple: 1.75" required>
            
            <label for="weight-bmi">Poids (en kg):</label>
            <input type="number" id="weight-bmi" step="0.1" min="20" max="300" placeholder="Exemple: 70" required>
            
            <button type="submit">Calculer l'IMC</button>
        </form>
        
        <div id="bmi-result" class="result"></div>
    </div>
    
    <h2>Calculateur de Métabolisme de Base</h2>
    <div class="calculator">
        <form id="bmr-form">
            <label for="height-bmr">Taille (en cm):</label>
            <input type="number" id="height-bmr" step="1" min="50" max="250" placeholder="Exemple: 175" required>
            
            <label for="weight-bmr">Poids (en kg):</label>
            <input type="number" id="weight-bmr" step="0.1" min="20" max="300" placeholder="Exemple: 70" required>
            
            <label for="age-bmr">Âge (en années):</label>
            <input type="number" id="age-bmr" step="1" min="1" max="120" placeholder="Exemple: 30" required>
            
            <label for="gender-bmr">Genre:</label>
            <select id="gender-bmr" required>
                <option value="male">Homme</option>
                <option value="female">Femme</option>
            </select>
            
            <button type="submit">Calculer le MB</button>
        </form>
        
        <div id="bmr-result" class="result"></div>
    </div>
    
    <h2>Détails de l'API</h2>
    <div class="api-details">
        <h3>Endpoint pour l'IMC</h3>
        <p>URL: <code>/bmi</code> (POST)</p>
        <p>Corps de la requête (JSON):</p>
        <pre>{
  "height": 1.75,  // taille en mètres
  "weight": 70    // poids en kg
}</pre>
        
        <h3>Endpoint pour le MB</h3>
        <p>URL: <code>/bmr</code> (POST)</p>
        <p>Corps de la requête (JSON):</p>
        <pre>{
  "height": 175,    // taille en cm
  "weight": 70,     // poids en kg
  "age": 30,        // âge en années
  "gender": "male"  // genre: "male" ou "female"
}</pre>
    </div>
    
    <script>
        document.getElementById('bmi-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const height = parseFloat(document.getElementById('height-bmi').value);
            const weight = parseFloat(document.getElementById('weight-bmi').value);
            
            fetch('/bmi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ height, weight })
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('bmi-result');
                if (data.error) {
                    resultDiv.innerHTML = `<p style="color: red">Erreur: ${data.error}</p>`;
                } else {
                    resultDiv.innerHTML = `
                        <p><strong>IMC:</strong> ${data.bmi}</p>
                        <p><strong>Catégorie:</strong> ${data.category}</p>
                    `;
                }
                resultDiv.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('bmi-result').innerHTML = '<p style="color: red">Une erreur est survenue lors du calcul.</p>';
                document.getElementById('bmi-result').style.display = 'block';
            });
        });
        
        document.getElementById('bmr-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const height = parseFloat(document.getElementById('height-bmr').value);
            const weight = parseFloat(document.getElementById('weight-bmr').value);
            const age = parseFloat(document.getElementById('age-bmr').value);
            const gender = document.getElementById('gender-bmr').value;
            
            fetch('/bmr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ height, weight, age, gender })
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('bmr-result');
                if (data.error) {
                    resultDiv.innerHTML = `<p style="color: red">Erreur: ${data.error}</p>`;
                } else {
                    resultDiv.innerHTML = `
                        <p><strong>Métabolisme de Base:</strong> ${data.bmr} ${data.unit}</p>
                        <p>C'est la quantité d'énergie dont votre corps a besoin au repos.</p>
                    `;
                }
                resultDiv.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('bmr-result').innerHTML = '<p style="color: red">Une erreur est survenue lors du calcul.</p>';
                document.getElementById('bmr-result').style.display = 'block';
            });
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    """Page d'accueil avec interface utilisateur HTML"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api', methods=['GET'])
def api_info():
    """Information API en format JSON"""
    return jsonify({
        'status': 'healthy',
        'service': 'Health Calculator API',
        'endpoints': {
            '/bmi': 'Calculate Body Mass Index (POST)',
            '/bmr': 'Calculate Basal Metabolic Rate (POST)'
        },
        'usage': {
            '/bmi': {
                'method': 'POST',
                'content-type': 'application/json',
                'body': {
                    'height': 'Height in meters (e.g., 1.75)',
                    'weight': 'Weight in kilograms (e.g., 70)'
                },
                'example': '{"height": 1.75, "weight": 70}'
            },
            '/bmr': {
                'method': 'POST',
                'content-type': 'application/json',
                'body': {
                    'height': 'Height in centimeters (e.g., 175)',
                    'weight': 'Weight in kilograms (e.g., 70)',
                    'age': 'Age in years (e.g., 30)',
                    'gender': 'Gender (male/female)'
                },
                'example': '{"height": 175, "weight": 70, "age": 30, "gender": "male"}'
            }
        }
    })

@app.route('/bmi', methods=['POST'])
def bmi():
    """
    Calculate BMI from height and weight
    Requires JSON input with 'height' (meters) and 'weight' (kg)
    """
    data = request.get_json()
    
    # Validate input
    if not data or 'height' not in data or 'weight' not in data:
        return jsonify({'error': 'Missing required parameters: height (meters) and weight (kg)'}), 400
    
    try:
        height = float(data['height'])
        weight = float(data['weight'])
        
        if height <= 0 or weight <= 0:
            return jsonify({'error': 'Height and weight must be positive values'}), 400
            
        bmi_value = calculate_bmi(height, weight)
        
        # Determine BMI category
        category = ""
        if bmi_value < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi_value < 25:
            category = "Normal weight"
        elif 25 <= bmi_value < 30:
            category = "Overweight"
        else:
            category = "Obesity"
            
        return jsonify({
            'bmi': round(bmi_value, 2),
            'category': category
        })
        
    except ValueError:
        return jsonify({'error': 'Height and weight must be numeric values'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bmr', methods=['POST'])
def bmr():
    """
    Calculate BMR from height, weight, age, and gender
    Requires JSON input with 'height' (cm), 'weight' (kg), 'age' (years), and 'gender' (male/female)
    """
    data = request.get_json()
    
    # Validate input
    required_params = ['height', 'weight', 'age', 'gender']
    if not data or not all(param in data for param in required_params):
        return jsonify({'error': f'Missing required parameters: {", ".join(required_params)}'}), 400
    
    try:
        height = float(data['height'])
        weight = float(data['weight'])
        age = float(data['age'])
        gender = data['gender'].lower()
        
        if height <= 0 or weight <= 0 or age <= 0:
            return jsonify({'error': 'Height, weight, and age must be positive values'}), 400
            
        if gender not in ['male', 'female']:
            return jsonify({'error': 'Gender must be "male" or "female"'}), 400
            
        bmr_value = calculate_bmr(height, weight, age, gender)
        
        return jsonify({
            'bmr': round(bmr_value, 2),
            'unit': 'calories/day'
        })
        
    except ValueError:
        return jsonify({'error': 'Height, weight, and age must be numeric values'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)