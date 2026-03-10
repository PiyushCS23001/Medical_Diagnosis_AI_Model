# diagnosis_interface.py

from medical_expert_system import MedicalExpertSystem

class DiagnosisInterface:
    def __init__(self):
        self.es = MedicalExpertSystem()
        
    def display_welcome(self):
        print("\n" + "="*70)
        print("        MEDICAL DIAGNOSIS EXPERT SYSTEM")
        print("="*70)
        print("\n[INFO] This system diagnoses diseases based on your symptoms")
        print("[MEDS] Provides recommended medications for each condition")
        print("[WARNING] DISCLAIMER: For educational purposes only")
        print("   Always consult a healthcare professional")
        print("="*70)

    def display_available_symptoms(self):
        print("\n[SYMPTOMS] AVAILABLE SYMPTOMS (Enter numbers or names):")
        print("-" * 70)
        
        # Group symptoms by category for better organization
        categories = {
            'General': ['fever', 'fatigue', 'weight_loss', 'weight_gain', 'night_sweats', 'chills'],
            'Respiratory': ['cough', 'difficulty_breathing', 'shortness_breath', 'wheezing', 'sore_throat'],
            'Pain': ['headache', 'severe_headache', 'chest_pain', 'abdominal_pain', 'joint_pain', 'muscle_pain'],
            'Neurological': ['dizziness', 'confusion', 'seizures', 'sensitivity_to_light', 'stiff_neck'],
            'Gastrointestinal': ['nausea', 'vomiting', 'diarrhea', 'heartburn', 'bloody_stool', 'yellow_skin'],
            'Skin': ['rash', 'red_rash', 'itchy_skin', 'dry_skin', 'hives', 'skin_lesions'],
            'Urinary': ['burning_urination', 'frequent_urination', 'flank_pain'],
            'Other': ['rapid_heartbeat', 'swollen_lymph_nodes', 'red_eyes', 'cold_intolerance']
        }
        
        symptom_list = list(self.es.symptoms_db.keys())
        
        # Display symptoms with numbers
        for i, symptom in enumerate(symptom_list, 1):
            print(f"{i:3d}. {symptom.replace('_', ' ').title():30s} - {self.es.symptoms_db[symptom]}")
        
        print("-" * 70)
        print("[TIP] Enter numbers like: 1,2,3 or names like: fever,cough,headache")

    def get_user_symptoms(self):
        print("\n[INPUT] Enter your symptoms (comma-separated):")
        
        while True:
            user_input = input("Symptoms: ").strip().lower()
            
            if not user_input:
                print("[ERROR] Please enter at least one symptom")
                continue
            
            symptoms = []
            items = [item.strip() for item in user_input.split(',')]
            
            for item in items:
                if item.isdigit():
                    # Handle number input
                    symptom_list = list(self.es.symptoms_db.keys())
                    idx = int(item) - 1
                    if 0 <= idx < len(symptom_list):
                        symptoms.append(symptom_list[idx])
                    else:
                        print(f"[WARNING] Invalid number: {item} (please use 1-{len(symptom_list)})")
                else:
                    # Handle name input
                    if item in self.es.symptoms_db:
                        symptoms.append(item)
                    else:
                        print(f"[WARNING] Unknown symptom: '{item}'")
            
            if symptoms:
                for symptom in symptoms:
                    self.es.add_symptom(symptom)
                print(f"[SUCCESS] Added {len(symptoms)} symptom(s): {', '.join(symptoms)}")
                break
            else:
                print("[ERROR] No valid symptoms entered. Please try again.")

    def display_diagnosis(self, diagnosed_diseases):
        print("\n" + "="*70)
        print("[RESULTS] DIAGNOSIS RESULTS")
        print("="*70)
        
        if not diagnosed_diseases:
            print("\n[NO MATCH] No matching diseases found with current symptoms.")
            print("\n[SUGGESTIONS]")
            print("   • Add more symptoms")
            print("   • Check symptom spelling")
            print("   • Consult a healthcare professional")
            return
        
        print(f"\n[FOUND] Found {len(diagnosed_diseases)} possible condition(s):")
        print("-" * 70)
        
        for i, diagnosis in enumerate(diagnosed_diseases[:5], 1):  # Show top 5
            confidence_percent = diagnosis['probability'] * 100
            
            # Color code based on confidence (using text only)
            if confidence_percent >= 80:
                confidence_color = "HIGH"
            elif confidence_percent >= 50:
                confidence_color = "MEDIUM"
            else:
                confidence_color = "LOW"
            
            print(f"\n{i}. {diagnosis['disease']}")
            print(f"   [{confidence_color}] Confidence: {confidence_percent:.1f}%")
            print(f"   [INFO] Explanation: {diagnosis['explanation']}")
            print(f"   [MEDS] Recommended Medication: {diagnosis['medication']}")
            print(f"   [SYMPTOMS] Matched Symptoms: {', '.join(diagnosis['matched_symptoms'])}")
            
            # Add recommendation
            if confidence_percent >= 70:
                print("   [RECOMMENDATION] Consult a doctor soon")
            elif confidence_percent >= 40:
                print("   [RECOMMENDATION] Monitor symptoms")
            else:
                print("   [RECOMMENDATION] Consider other possibilities")

    def display_rule_trace(self):
        print("\n" + "="*70)
        print("[TRACE] INFERENCE TRACE (Forward Chaining Process)")
        print("="*70)
        
        if self.es.inference_trace:
            for trace in self.es.inference_trace:
                print(trace)
        else:
            print("No inference trace available")

    def suggest_next_steps(self, diagnosed_diseases):
        suggestions = self.es.suggest_additional_symptoms(diagnosed_diseases)
        
        if suggestions:
            print("\n" + "="*70)
            print("[SUGGESTIONS] ADDITIONAL SYMPTOMS TO CHECK")
            print("="*70)
            print("\nTo improve diagnosis accuracy, check for:")
            
            for suggestion in suggestions[:3]:
                print(f"• For {suggestion['disease']}: {suggestion['symptom'].replace('_', ' ').title()}")
                print(f"  ({suggestion['description']})")

    def run(self):
        while True:
            self.display_welcome()
            self.display_available_symptoms()
            self.get_user_symptoms()
            
            # Perform diagnosis
            diagnosed_diseases = self.es.forward_chaining()
            
            # Display results
            self.display_diagnosis(diagnosed_diseases)
            self.display_rule_trace()
            self.suggest_next_steps(diagnosed_diseases)
            
            # Ask for next action
            print("\n" + "="*70)
            print("What would you like to do next?")
            print("1. Start new diagnosis")
            print("2. Add more symptoms to current case")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self.es.reset_session()
                print("\n" + "="*70)
                print("           NEW DIAGNOSIS SESSION")
                print("="*70)
                continue
            elif choice == '2':
                print("\n[INFO] Adding more symptoms to current case...")
                continue  # Keep working memory
            elif choice == '3':
                print("\n" + "="*70)
                print("Thank you for using the Medical Diagnosis Expert System!")
                print("Remember: This is an educational tool.")
                print("Always consult healthcare professionals for medical advice.")
                print("="*70)
                break
            else:
                print("[ERROR] Invalid choice. Exiting...")
                break


# Run the application
if __name__ == "__main__":
    interface = DiagnosisInterface()
    interface.run()