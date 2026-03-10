# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="MediDiagnose AI - Medical Expert System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Card styling */
    .diagnosis-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #2c3e50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .high-confidence {
        border-left-color: #dc3545;
    }
    
    .medium-confidence {
        border-left-color: #ffc107;
    }
    
    .low-confidence {
        border-left-color: #28a745;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Symptom button styling */
    .stButton > button {
        background-color: #e9ecef;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-size: 0.9rem;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #2c3e50;
        color: white;
    }
    
    /* Selected symptom pills */
    .symptom-pill {
        background-color: #2c3e50;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        font-size: 0.9rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
        }
        
        .diagnosis-card {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Import the MedicalExpertSystem class
from medical_expert_system import MedicalExpertSystem

# Initialize session state
if 'expert_system' not in st.session_state:
    st.session_state.expert_system = MedicalExpertSystem()
    st.session_state.diagnoses = []
    st.session_state.symptom_history = []
    st.session_state.current_page = "diagnosis"
    st.session_state.search_query = ""

class StreamlitInterface:
    def __init__(self):
        self.es = st.session_state.expert_system
        
    def render_header(self):
        """Render professional header"""
        st.markdown("""
        <div class="main-header">
            <h1>🏥 MediDiagnose AI</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">Advanced Medical Diagnosis Expert System</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">Powered by Forward Chaining & IF-THEN Rules</p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_sidebar(self):
        """Render sidebar with navigation and info"""
        with st.sidebar:
            st.markdown("## 🏥 MediDiagnose AI")
            st.markdown("---")
            
            # Navigation
            st.markdown("### Navigation")
            
            if st.button("🔍 Diagnosis", key="nav_diagnosis", use_container_width=True):
                st.session_state.current_page = "diagnosis"
                st.rerun()
            
            if st.button("📋 History", key="nav_history", use_container_width=True):
                st.session_state.current_page = "history"
                st.rerun()
            
            if st.button("ℹ️ About", key="nav_about", use_container_width=True):
                st.session_state.current_page = "about"
                st.rerun()
            
            st.markdown("---")
            
            # Quick stats
            st.markdown("### 📊 Quick Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Diseases", len(self.es.rules))
            with col2:
                st.metric("Symptoms", len(self.es.symptoms_db))
            
            st.markdown("---")
            
            # Current session info
            if st.session_state.expert_system.working_memory:
                st.markdown("### 📋 Current Symptoms")
                for symptom in st.session_state.expert_system.working_memory:
                    st.markdown(f"- {symptom.replace('_', ' ').title()}")
            
            st.markdown("---")
            
            # Disclaimer
            st.warning("""
            **⚠️ Medical Disclaimer**
            
            This system is for educational purposes only. Always consult with qualified healthcare professionals for medical advice.
            """)
    
    def render_symptom_selector(self):
        """Render symptom selection interface"""
        st.markdown("## 🔍 Select Your Symptoms")
        
        # Search bar
        search = st.text_input("🔎 Search symptoms", placeholder="Type to search...", key="symptom_search")
        
        # Get unique symptoms (avoid duplicates)
        all_symptoms = list(self.es.symptoms_db.keys())
        
        # Filter symptoms based on search
        if search:
            filtered_symptoms = [s for s in all_symptoms if search.lower() in s.replace('_', ' ')]
        else:
            filtered_symptoms = all_symptoms
        
        # Create categories for organization (for non-search mode)
        if not search:
            # Define categories with unique symptoms
            categories = {
                'General': ['fever', 'fatigue', 'chills', 'night_sweats'],
                'Respiratory': ['cough', 'difficulty_breathing', 'shortness_breath', 'wheezing', 'sore_throat'],
                'Pain': ['headache', 'severe_headache', 'chest_pain', 'abdominal_pain', 'joint_pain', 'muscle_pain'],
                'Neurological': ['dizziness', 'confusion', 'seizures', 'sensitivity_to_light', 'stiff_neck'],
                'Gastrointestinal': ['nausea', 'vomiting', 'diarrhea', 'heartburn', 'bloody_stool', 'yellow_skin'],
                'Skin': ['rash', 'red_rash', 'itchy_skin', 'dry_skin', 'hives', 'skin_lesions'],
                'Urinary': ['burning_urination', 'frequent_urination', 'excessive_thirst', 'flank_pain'],
                'Cardiovascular': ['rapid_heartbeat', 'dizziness', 'chest_pain'],
                'Mental': ['sadness', 'anxiety', 'loss_of_interest', 'sleep_disturbance', 'restlessness'],
                'Other': ['swollen_lymph_nodes', 'swollen_glands', 'red_eyes', 'cold_intolerance', 'sweating', 'weight_loss', 'weight_gain']
            }
            
            # Create tabs
            tabs = st.tabs(list(categories.keys()))
            
            for tab_idx, (category, symptom_list) in enumerate(zip(categories.keys(), categories.values())):
                with tabs[tab_idx]:
                    # Create rows of 3 columns
                    cols = st.columns(3)
                    for idx, symptom in enumerate(symptom_list):
                        if symptom in self.es.symptoms_db:
                            col_idx = idx % 3
                            with cols[col_idx]:
                                # Check if symptom is selected
                                is_selected = symptom in st.session_state.expert_system.working_memory
                                
                                # Create unique key using category and symptom
                                button_key = f"cat_{tab_idx}_{symptom}"
                                
                                if is_selected:
                                    if st.button(f"✅ {symptom.replace('_', ' ').title()}", key=button_key, use_container_width=True):
                                        st.session_state.expert_system.working_memory.remove(symptom)
                                        st.rerun()
                                else:
                                    if st.button(f"➕ {symptom.replace('_', ' ').title()}", key=button_key, use_container_width=True):
                                        self.es.add_symptom(symptom)
                                        st.rerun()
        else:
            # Show search results
            st.markdown("### Search Results")
            if filtered_symptoms:
                cols = st.columns(3)
                for idx, symptom in enumerate(filtered_symptoms[:18]):  # Limit to 18 results
                    col_idx = idx % 3
                    with cols[col_idx]:
                        is_selected = symptom in st.session_state.expert_system.working_memory
                        button_key = f"search_{symptom}_{idx}"
                        
                        if is_selected:
                            if st.button(f"✅ {symptom.replace('_', ' ').title()}", key=button_key, use_container_width=True):
                                st.session_state.expert_system.working_memory.remove(symptom)
                                st.rerun()
                        else:
                            if st.button(f"➕ {symptom.replace('_', ' ').title()}", key=button_key, use_container_width=True):
                                self.es.add_symptom(symptom)
                                st.rerun()
            else:
                st.info("No symptoms found matching your search.")
        
        # Selected symptoms display
        if st.session_state.expert_system.working_memory:
            st.markdown("### 📋 Selected Symptoms")
            selected_html = "<div style='display: flex; flex-wrap: wrap; gap: 5px;'>"
            for symptom in st.session_state.expert_system.working_memory:
                selected_html += f"<span class='symptom-pill'>{symptom.replace('_', ' ').title()}</span>"
            selected_html += "</div>"
            st.markdown(selected_html, unsafe_allow_html=True)
            
            # Clear all button
            if st.button("🗑️ Clear All Symptoms", key="clear_all_symptoms"):
                st.session_state.expert_system.working_memory.clear()
                st.rerun()
    
    def render_diagnosis_results(self):
        """Render diagnosis results"""
        st.markdown("## 📊 Diagnosis Results")
        
        if not st.session_state.expert_system.working_memory:
            st.info("👆 Please select at least one symptom to begin diagnosis")
            return
        
        # Perform diagnosis
        with st.spinner("Analyzing symptoms..."):
            diagnosed_diseases = self.es.forward_chaining()
        
        if not diagnosed_diseases:
            st.error("❌ No matching diseases found with current symptoms")
            
            # Show suggestions
            st.markdown("### 💡 Suggestions")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("Add more specific symptoms")
            with col2:
                st.info("Check symptom spelling")
            with col3:
                st.info("Consult a healthcare professional")
            return
        
        # Display confidence gauge for top result
        top_disease = diagnosed_diseases[0]
        confidence = top_disease['probability'] * 100
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Top Diagnosis Confidence", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "#2c3e50"},
                'steps': [
                    {'range': [0, 30], 'color': '#ffcccc'},
                    {'range': [30, 70], 'color': '#ffffcc'},
                    {'range': [70, 100], 'color': '#ccffcc'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(height=180, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        # Display all conditions
        st.markdown(f"### Found {len(diagnosed_diseases)} possible condition(s)")
        
        for i, diagnosis in enumerate(diagnosed_diseases[:5]):
            confidence_pct = diagnosis['probability'] * 100
            match_pct = diagnosis.get('match_percentage', confidence_pct)
            
            # Determine badge
            if confidence_pct >= 70:
                badge = "🔴 HIGH"
            elif confidence_pct >= 40:
                badge = "🟡 MEDIUM"
            else:
                badge = "🟢 LOW"
            
            with st.expander(f"{i+1}. {diagnosis['disease']} - {badge} ({confidence_pct:.1f}%)"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**📝 Explanation:** {diagnosis['explanation']}")
                    st.markdown(f"**💊 Medication:** {diagnosis['medication']}")
                    st.markdown(f"**✅ Matched Symptoms:** {', '.join(diagnosis['matched_symptoms'])}")
                    st.markdown(f"**📋 Required Symptoms:** {', '.join(diagnosis['all_required_symptoms'])}")
                    st.markdown(f"**📊 Match Rate:** {match_pct:.0f}% of required symptoms")
                
                with col2:
                    st.progress(confidence_pct/100)
                    if confidence_pct >= 70:
                        st.error("⚠️ Consult doctor soon")
                    elif confidence_pct >= 40:
                        st.warning("📝 Monitor symptoms")
                    else:
                        st.info("ℹ️ Consider other options")
        
        # Save to history
        if diagnosed_diseases:
            history_entry = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'symptoms': st.session_state.expert_system.working_memory.copy(),
                'diagnoses': diagnosed_diseases[:3]
            }
            st.session_state.symptom_history.append(history_entry)

    def render_inference_trace(self):
        """Render the inference trace - FIXED to avoid duplication"""
        with st.expander("🔍 View Inference Trace (Forward Chaining Process)"):
            if self.es.inference_trace:
                # Use a container to ensure unique display
                trace_container = st.container()
                with trace_container:
                    for trace in self.es.inference_trace:
                        st.code(trace)
            else:
                st.info("No inference trace available")
    
    def render_history_page(self):
        """Render history page"""
        st.markdown("## 📋 Diagnosis History")
        
        if not st.session_state.symptom_history:
            st.info("No diagnosis history yet. Start a new diagnosis to see history.")
            return
        
        # Clear history button
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.symptom_history = []
            st.rerun()
        
        for idx, entry in enumerate(reversed(st.session_state.symptom_history[-10:])):  # Show last 10
            with st.container():
                st.markdown(f"### 🕐 {entry['timestamp']}")
                st.markdown(f"**Symptoms:** {', '.join(entry['symptoms'])}")
                
                cols = st.columns(len(entry['diagnoses']))
                for d_idx, diagnosis in enumerate(entry['diagnoses']):
                    with cols[d_idx]:
                        confidence = diagnosis['probability'] * 100
                        if confidence >= 70:
                            st.error(f"**{diagnosis['disease']}**\n\n{confidence:.1f}%")
                        elif confidence >= 40:
                            st.warning(f"**{diagnosis['disease']}**\n\n{confidence:.1f}%")
                        else:
                            st.info(f"**{diagnosis['disease']}**\n\n{confidence:.1f}%")
                st.markdown("---")
    
    def render_about_page(self):
        """Render about page"""
        st.markdown("## ℹ️ About MediDiagnose AI")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 **Purpose**
            MediDiagnose AI is an educational expert system that demonstrates how rule-based systems work in medical diagnosis using forward chaining.
            
            ### 🔧 **Technology**
            - **AI Technique:** Forward Chaining
            - **Knowledge Representation:** IF-THEN Rules
            - **Frontend:** Streamlit
            - **Backend:** Python
            
            ### 📊 **Knowledge Base**
            - **Diseases Covered:** 29+
            - **Symptoms Database:** 50+
            - **Rules:** IF-THEN based matching
            """)
        
        with col2:
            st.markdown("""
            ### ⚕️ **How It Works**
            1. User selects symptoms
            2. System applies forward chaining
            3. Rules are evaluated
            4. Diagnoses are ranked by confidence
            5. Results displayed with recommendations
            
            ### ⚠️ **Important Notice**
            This system is for **educational purposes only**. Always consult healthcare professionals for actual medical advice.
            
            ### 📞 **Emergency**
            If you're experiencing a medical emergency, call emergency services immediately.
            """)
    
    def render_footer(self):
        """Render footer"""
        st.markdown("---")
        st.markdown("""
        <div class="footer">
            <p>🏥 MediDiagnose AI - Educational Medical Expert System</p>
            <p>© 2024 | For educational purposes only | Not for clinical use</p>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Main run method"""
        self.render_header()
        self.render_sidebar()
        
        # Main content area
        if st.session_state.current_page == "diagnosis":
            col1, col2 = st.columns([1, 1])
            
            with col1:
                self.render_symptom_selector()
            
            with col2:
                self.render_diagnosis_results()
                self.render_inference_trace()
                
                # Action buttons
                st.markdown("### 🎯 Actions")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("🔄 New Diagnosis", key="new_diagnosis", use_container_width=True):
                        st.session_state.expert_system.reset_session()
                        st.rerun()
                with col_b:
                    if st.button("📋 View History", key="view_history", use_container_width=True):
                        st.session_state.current_page = "history"
                        st.rerun()
        
        elif st.session_state.current_page == "history":
            self.render_history_page()
            if st.button("← Back to Diagnosis", key="back_to_diagnosis", use_container_width=True):
                st.session_state.current_page = "diagnosis"
                st.rerun()
        
        elif st.session_state.current_page == "about":
            self.render_about_page()
            if st.button("← Back to Diagnosis", key="back_from_about", use_container_width=True):
                st.session_state.current_page = "diagnosis"
                st.rerun()
        
        self.render_footer()

# Run the application
if __name__ == "__main__":
    app = StreamlitInterface()
    app.run()