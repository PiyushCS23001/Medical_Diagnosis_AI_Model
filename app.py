from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from medical_expert_system import MedicalExpertSystem
import json

app = Flask(__name__)
CORS(app)

# Initialize the expert system
expert_system = MedicalExpertSystem()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get all available symptoms"""
    symptoms = list(expert_system.symptoms_db.keys())
    return jsonify({
        'success': True,
        'symptoms': symptoms,
        'symptoms_info': expert_system.symptoms_db
    })

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """Perform diagnosis based on selected symptoms"""
    data = request.json
    selected_symptoms = data.get('symptoms', [])
    
    # Add symptoms to working memory
    expert_system.working_memory = selected_symptoms
    
    # Perform forward chaining
    diagnosed_diseases = expert_system.forward_chaining()
    
    # Format results for frontend
    results = []
    for disease in diagnosed_diseases[:10]:  # Top 10 results
        results.append({
            'name': disease['disease'],
            'confidence': round(disease['probability'] * 100, 1),
            'match_percentage': disease.get('match_percentage', disease['probability'] * 100),
            'matched_symptoms': disease['matched_symptoms'],
            'all_required_symptoms': disease.get('all_required_symptoms', []),
            'medication': disease['medication'],
            'explanation': disease['explanation']
        })
    
    return jsonify({
        'success': True,
        'diagnoses': results,
        'total_found': len(results)
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the expert system"""
    expert_system.reset_session()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)