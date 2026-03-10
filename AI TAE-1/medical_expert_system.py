# medical_expert_system.py

class MedicalExpertSystem:
    def __init__(self):
        # Expanded Knowledge Base with more diseases
        self.rules = [
            # Respiratory Diseases
            {
                'id': 1,
                'conditions': ['fever', 'cough', 'fatigue'],
                'disease': 'Common Cold',
                'probability': 0.8,
                'medication': 'Acetaminophen, Decongestants, Rest',
                'explanation': 'Viral infection affecting upper respiratory tract'
            },
            {
                'id': 2,
                'conditions': ['fever', 'cough', 'difficulty_breathing'],
                'disease': 'Pneumonia',
                'probability': 0.85,
                'medication': 'Antibiotics (Amoxicillin), Antipyretics, Oxygen therapy',
                'explanation': 'Lung infection causing inflammation in air sacs'
            },
            {
                'id': 3,
                'conditions': ['cough', 'wheezing', 'shortness_breath'],
                'disease': 'Asthma',
                'probability': 0.9,
                'medication': 'Inhalers (Albuterol), Corticosteroids',
                'explanation': 'Chronic inflammatory disease of airways'
            },
            {
                'id': 4,
                'conditions': ['fever', 'cough', 'night_sweats', 'weight_loss'],
                'disease': 'Tuberculosis',
                'probability': 0.85,
                'medication': 'Rifampin, Isoniazid, Pyrazinamide',
                'explanation': 'Bacterial infection affecting lungs'
            },
            {
                'id': 5,
                'conditions': ['sore_throat', 'fever', 'swollen_lymph_nodes'],
                'disease': 'Strep Throat',
                'probability': 0.8,
                'medication': 'Penicillin, Amoxicillin, Pain relievers',
                'explanation': 'Bacterial infection causing throat inflammation'
            },
            
            # Cardiovascular Diseases
            {
                'id': 6,
                'conditions': ['chest_pain', 'shortness_breath', 'fatigue', 'nausea'],
                'disease': 'Heart Attack',
                'probability': 0.95,
                'medication': 'Aspirin, Nitroglycerin, Thrombolytics',
                'explanation': 'Blockage of blood flow to heart muscle'
            },
            {
                'id': 7,
                'conditions': ['chest_pain', 'fatigue', 'dizziness'],
                'disease': 'Angina',
                'probability': 0.8,
                'medication': 'Nitroglycerin, Beta-blockers, Calcium channel blockers',
                'explanation': 'Reduced blood flow to heart causing chest pain'
            },
            {
                'id': 8,
                'conditions': ['headache', 'dizziness', 'nausea', 'blurred_vision'],
                'disease': 'Hypertension',
                'probability': 0.75,
                'medication': 'Lisinopril, Amlodipine, Hydrochlorothiazide',
                'explanation': 'High blood pressure'
            },
            
            # Neurological Diseases
            {
                'id': 9,
                'conditions': ['severe_headache', 'nausea', 'sensitivity_to_light'],
                'disease': 'Migraine',
                'probability': 0.85,
                'medication': 'Sumatriptan, Ibuprofen, Beta-blockers',
                'explanation': 'Neurological condition causing severe headaches'
            },
            {
                'id': 10,
                'conditions': ['fever', 'severe_headache', 'stiff_neck'],
                'disease': 'Meningitis',
                'probability': 0.9,
                'medication': 'Ceftriaxone, Vancomycin, Dexamethasone',
                'explanation': 'Inflammation of protective membranes covering brain'
            },
            {
                'id': 11,
                'conditions': ['headache', 'confusion', 'fever', 'seizures'],
                'disease': 'Encephalitis',
                'probability': 0.85,
                'medication': 'Acyclovir, Anticonvulsants, Corticosteroids',
                'explanation': 'Inflammation of brain tissue'
            },
            
            # Gastrointestinal Diseases
            {
                'id': 12,
                'conditions': ['nausea', 'vomiting', 'diarrhea', 'abdominal_pain'],
                'disease': 'Gastroenteritis',
                'probability': 0.9,
                'medication': 'Oral rehydration salts, Ondansetron, Loperamide',
                'explanation': 'Inflammation of stomach and intestines'
            },
            {
                'id': 13,
                'conditions': ['abdominal_pain', 'heartburn', 'nausea'],
                'disease': 'GERD',
                'probability': 0.8,
                'medication': 'Omeprazole, Ranitidine, Antacids',
                'explanation': 'Gastroesophageal reflux disease'
            },
            {
                'id': 14,
                'conditions': ['abdominal_pain', 'bloody_stool', 'fatigue'],
                'disease': 'Ulcerative Colitis',
                'probability': 0.75,
                'medication': 'Mesalamine, Corticosteroids, Immunosuppressants',
                'explanation': 'Inflammatory bowel disease'
            },
            {
                'id': 15,
                'conditions': ['abdominal_pain', 'nausea', 'yellow_skin'],
                'disease': 'Hepatitis',
                'probability': 0.8,
                'medication': 'Antivirals, Interferon, Supportive care',
                'explanation': 'Liver inflammation'
            },
            
            # Infectious Diseases
            {
                'id': 16,
                'conditions': ['fever', 'rash', 'joint_pain', 'headache'],
                'disease': 'Dengue Fever',
                'probability': 0.85,
                'medication': 'Acetaminophen, Fluid replacement, Monitoring',
                'explanation': 'Mosquito-borne viral infection'
            },
            {
                'id': 17,
                'conditions': ['fever', 'rash', 'cough', 'red_eyes'],
                'disease': 'Measles',
                'probability': 0.9,
                'medication': 'Vitamin A, Antipyretics, Supportive care',
                'explanation': 'Highly contagious viral infection'
            },
            {
                'id': 18,
                'conditions': ['fever', 'rash', 'swollen_glands'],
                'disease': 'Rubella',
                'probability': 0.8,
                'medication': 'Acetaminophen, Rest, Fluids',
                'explanation': 'Viral infection causing red rash'
            },
            {
                'id': 19,
                'conditions': ['fever', 'fatigue', 'muscle_pain', 'rash'],
                'disease': 'Chikungunya',
                'probability': 0.8,
                'medication': 'NSAIDs, Acetaminophen, Fluid therapy',
                'explanation': 'Mosquito-borne viral disease'
            },
            {
                'id': 20,
                'conditions': ['fever', 'chills', 'sweating', 'headache'],
                'disease': 'Malaria',
                'probability': 0.85,
                'medication': 'Chloroquine, Artemisinin, Quinine',
                'explanation': 'Mosquito-borne parasitic infection'
            },
            
            # Urinary and Kidney Diseases
            {
                'id': 21,
                'conditions': ['burning_urination', 'frequent_urination', 'lower_abdominal_pain'],
                'disease': 'UTI',
                'probability': 0.9,
                'medication': 'Nitrofurantoin, Trimethoprim-sulfamethoxazole',
                'explanation': 'Urinary tract infection'
            },
            {
                'id': 22,
                'conditions': ['flank_pain', 'fever', 'burning_urination'],
                'disease': 'Kidney Infection',
                'probability': 0.85,
                'medication': 'Ciprofloxacin, Ceftriaxone, Pain relievers',
                'explanation': 'Pyelonephritis - kidney inflammation'
            },
            
            # Skin Diseases
            {
                'id': 23,
                'conditions': ['itchy_skin', 'red_rash', 'dry_skin'],
                'disease': 'Eczema',
                'probability': 0.8,
                'medication': 'Topical corticosteroids, Moisturizers, Antihistamines',
                'explanation': 'Atopic dermatitis - skin inflammation'
            },
            {
                'id': 24,
                'conditions': ['red_rash', 'itching', 'hives'],
                'disease': 'Urticaria',
                'probability': 0.85,
                'medication': 'Antihistamines (Cetirizine, Loratadine)',
                'explanation': 'Allergic reaction causing hives'
            },
            {
                'id': 25,
                'conditions': ['skin_lesions', 'fatigue', 'joint_pain'],
                'disease': 'Lupus',
                'probability': 0.7,
                'medication': 'Hydroxychloroquine, Corticosteroids, Immunosuppressants',
                'explanation': 'Autoimmune disease'
            },
            
            # Endocrine Diseases
            {
                'id': 26,
                'conditions': ['frequent_urination', 'excessive_thirst', 'fatigue', 'weight_loss'],
                'disease': 'Diabetes Type 2',
                'probability': 0.85,
                'medication': 'Metformin, Insulin, Sulfonylureas',
                'explanation': 'Metabolic disorder affecting blood sugar'
            },
            {
                'id': 27,
                'conditions': ['fatigue', 'weight_gain', 'cold_intolerance'],
                'disease': 'Hypothyroidism',
                'probability': 0.8,
                'medication': 'Levothyroxine',
                'explanation': 'Underactive thyroid gland'
            },
            
            # Mental Health
            {
                'id': 28,
                'conditions': ['sadness', 'loss_of_interest', 'fatigue', 'sleep_disturbance'],
                'disease': 'Depression',
                'probability': 0.85,
                'medication': 'SSRIs (Fluoxetine, Sertraline), Therapy',
                'explanation': 'Mood disorder affecting daily life'
            },
            {
                'id': 29,
                'conditions': ['anxiety', 'restlessness', 'rapid_heartbeat', 'sweating'],
                'disease': 'Anxiety Disorder',
                'probability': 0.8,
                'medication': 'Benzodiazepines, SSRIs, Therapy',
                'explanation': 'Excessive worry and fear response'
            }
        ]
        
        # Expanded Symptom database
        self.symptoms_db = {
            # General Symptoms
            'fever': 'Elevated body temperature',
            'fatigue': 'Extreme tiredness',
            'weight_loss': 'Unexplained weight reduction',
            'weight_gain': 'Unexplained weight increase',
            'night_sweats': 'Excessive sweating at night',
            'chills': 'Shivering and feeling cold',
            
            # Respiratory Symptoms
            'cough': 'Persistent coughing',
            'difficulty_breathing': 'Shortness of breath',
            'shortness_breath': 'Breathing difficulty',
            'wheezing': 'Whistling sound while breathing',
            'sore_throat': 'Pain in throat',
            
            # Pain Symptoms
            'headache': 'Pain in head',
            'severe_headache': 'Intense head pain',
            'chest_pain': 'Pain in chest area',
            'abdominal_pain': 'Pain in abdomen',
            'joint_pain': 'Pain in joints',
            'muscle_pain': 'Aching muscles',
            'flank_pain': 'Pain in side/back',
            'lower_abdominal_pain': 'Pain in lower belly',
            
            # Cardiovascular Symptoms
            'dizziness': 'Feeling lightheaded',
            'rapid_heartbeat': 'Fast heart rate',
            
            # Neurological Symptoms
            'confusion': 'Mental disorientation',
            'seizures': 'Uncontrolled convulsions',
            'sensitivity_to_light': 'Pain from bright light',
            'stiff_neck': 'Neck stiffness',
            'blurred_vision': 'Blurry eyesight',
            
            # Gastrointestinal Symptoms
            'nausea': 'Feeling of sickness',
            'vomiting': 'Expelling stomach contents',
            'diarrhea': 'Frequent loose stools',
            'heartburn': 'Burning chest sensation',
            'bloody_stool': 'Blood in feces',
            'yellow_skin': 'Jaundice - yellow discoloration',
            
            # Skin Symptoms
            'rash': 'Skin eruption',
            'red_rash': 'Red skin eruption',
            'itchy_skin': 'Skin itching',
            'dry_skin': 'Dry, flaky skin',
            'hives': 'Raised, itchy welts',
            'skin_lesions': 'Abnormal skin patches',
            'itching': 'Skin irritation',
            
            # Urinary Symptoms
            'burning_urination': 'Pain while urinating',
            'frequent_urination': 'Urinating often',
            'excessive_thirst': 'Constant thirst',
            
            # Other Symptoms
            'swollen_lymph_nodes': 'Enlarged lymph nodes',
            'swollen_glands': 'Swollen glands',
            'red_eyes': 'Eye redness',
            'cold_intolerance': 'Sensitivity to cold',
            'sleep_disturbance': 'Trouble sleeping',
            'loss_of_interest': 'No interest in activities',
            'sadness': 'Persistent sad mood',
            'anxiety': 'Excessive worry',
            'restlessness': 'Unable to relax',
            'sweating': 'Excessive perspiration'
        }
        
        self.working_memory = []
        self.inference_trace = []
        self.last_trace_count = 0

    def add_symptom(self, symptom):
        """Add symptom to working memory"""
        if symptom in self.symptoms_db:
            if symptom not in self.working_memory:  # Avoid duplicates
                self.working_memory.append(symptom)
                # Clear old trace and add new symptom
                self.inference_trace = [f"Added symptom: {symptom} - {self.symptoms_db[symptom]}"]
                self.last_trace_count = 1
            return True
        return False

    def forward_chaining(self):
        """Forward chaining inference engine - NOW WITH PARTIAL MATCHING"""
        # Clear previous trace but keep symptom addition messages
        new_trace = []
        for trace in self.inference_trace:
            if trace.startswith("Added symptom:"):
                new_trace.append(trace)
        
        new_trace.append("\nStarting Forward Chaining Diagnosis...")
        diagnosed_diseases = []
        
        # Check each rule - NOW USING PARTIAL MATCHING
        for rule in self.rules:
            # Calculate how many symptoms match
            matched_symptoms = [s for s in rule['conditions'] if s in self.working_memory]
            match_count = len(matched_symptoms)
            total_required = len(rule['conditions'])
            
            # Only consider if at least one symptom matches
            if match_count > 0:
                # Calculate confidence based on match percentage
                match_percentage = match_count / total_required
                
                # Base probability adjusted by match percentage
                adjusted_probability = rule['probability'] * match_percentage
                
                diagnosis = {
                    'disease': rule['disease'],
                    'probability': adjusted_probability,
                    'matched_symptoms': matched_symptoms,
                    'all_required_symptoms': rule['conditions'],
                    'medication': rule['medication'],
                    'explanation': rule['explanation'],
                    'rule_id': rule['id'],
                    'match_percentage': match_percentage * 100
                }
                
                diagnosed_diseases.append(diagnosis)
                
                new_trace.append(
                    f"Rule {rule['id']} FIRED: {', '.join(matched_symptoms)} ({match_count}/{total_required} symptoms) -> {rule['disease']} ({match_percentage*100:.0f}% match)"
                )
        
        # Sort by probability (highest first)
        diagnosed_diseases.sort(key=lambda x: x['probability'], reverse=True)
        
        new_trace.append(f"\nFound {len(diagnosed_diseases)} possible conditions\n")
        self.inference_trace = new_trace
        self.last_trace_count = len(new_trace)
        
        return diagnosed_diseases

    def calculate_confidence(self, rule):
        """Calculate confidence based on symptom overlap"""
        total_symptoms = len(rule['conditions'])
        matched_symptoms = sum(1 for s in rule['conditions'] if s in self.working_memory)
        return matched_symptoms / total_symptoms if total_symptoms > 0 else 0

    def suggest_additional_symptoms(self, diagnosed_diseases):
        """Suggest additional symptoms to check"""
        suggestions = []
        
        if diagnosed_diseases:
            for disease in diagnosed_diseases[:2]:  # Check top 2 diseases
                for rule in self.rules:
                    if rule['disease'] == disease['disease']:
                        missing_symptoms = [s for s in rule['conditions'] 
                                          if s not in self.working_memory]
                        for symptom in missing_symptoms[:2]:  # Suggest 2 missing symptoms
                            if symptom in self.symptoms_db:
                                suggestions.append({
                                    'disease': disease['disease'],
                                    'symptom': symptom,
                                    'description': self.symptoms_db[symptom]
                                })
        
        return suggestions

    def reset_session(self):
        """Reset working memory for new session"""
        self.working_memory = []
        self.inference_trace = []
        self.last_trace_count = 0