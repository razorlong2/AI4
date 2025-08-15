#!/usr/bin/env python3
# coding: utf-8
"""
EpiMind AI - IAAM Predictor cu Chat Conversational
UMF "Grigore T. Popa" Iași
Version: 3.0.0 - AI Conversational Integration

FUNCȚIONALITĂȚI:
- Chat AI conversational pentru introducerea datelor
- Predicție automată IAAM 
- Interfață chat inteligentă
- AI local cu Ollama

Instalare:
    pip install streamlit ollama pandas plotly
    # Instalează Ollama: https://ollama.ai/
    ollama pull llama2:7b

Rulează:
    streamlit run epimind_ai.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import requests
import time

# Configurare aplicație
st.set_page_config(
    page_title="EpiMind AI - IAAM Predictor", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS modern pentru chat
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    :root {
        --bg-primary: #0f1419;
        --bg-secondary: #1a1f2e;
        --bg-chat: #242936;
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --accent-blue: #3b82f6;
        --accent-green: #10b981;
        --accent-red: #ef4444;
        --accent-yellow: #f59e0b;
        --border: rgba(255,255,255,0.1);
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Chat Container */
    .chat-container {
        background: var(--bg-chat);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid var(--border);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    /* Messages */
    .message {
        margin: 15px 0;
        padding: 15px;
        border-radius: 12px;
        animation: fadeIn 0.3s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, var(--accent-blue), #1e40af);
        color: white;
        margin-left: 20%;
        text-align: right;
    }
    
    .ai-message {
        background: var(--bg-secondary);
        color: var(--text-primary);
        margin-right: 20%;
        border-left: 4px solid var(--accent-green);
    }
    
    .system-message {
        background: linear-gradient(135deg, var(--accent-yellow), #d97706);
        color: white;
        text-align: center;
        font-weight: 600;
    }
    
    /* Results */
    .risk-critical { 
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-weight: 700;
        box-shadow: 0 4px 20px rgba(220,38,38,0.3);
    }
    
    .risk-high { 
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-weight: 700;
        box-shadow: 0 4px 20px rgba(245,158,11,0.3);
    }
    
    .risk-moderate { 
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-weight: 700;
        box-shadow: 0 4px 20px rgba(59,130,246,0.3);
    }
    
    .risk-low { 
        background: linear-gradient(135deg, #10b981, #047857);
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-weight: 700;
        box-shadow: 0 4px 20px rgba(16,185,129,0.3);
    }
    
    /* Input */
    .chat-input {
        background: var(--bg-secondary);
        border: 2px solid var(--border);
        border-radius: 25px;
        padding: 15px 20px;
        color: var(--text-primary);
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .chat-input:focus {
        border-color: var(--accent-blue);
        box-shadow: 0 0 20px rgba(59,130,246,0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .typing {
        animation: pulse 1.5s infinite;
    }
    
    /* Metrics */
    .metric-card {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid var(--border);
        margin: 5px;
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        color: var(--accent-blue);
        margin: 10px 0;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CLASE AI ȘI LOGICĂ MEDICALĂ
# ============================================================================

class OllamaAI:
    """Client pentru Ollama AI local"""
    
    def __init__(self, model="llama2:7b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.available = self.check_availability()
        
    def check_availability(self) -> bool:
        """Verifică dacă Ollama este disponibil"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generează răspuns folosind Ollama"""
        if not self.available:
            return "❌ Ollama nu este disponibil. Instalează și pornește Ollama."
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "Eroare la generare")
            else:
                return f"Eroare HTTP: {response.status_code}"
                
        except Exception as e:
            return f"Eroare conexiune: {str(e)}"

class IAMPredictor:
    """Motor de predicție IAAM"""
    
    def __init__(self):
        self.device_weights = {
            "cateter_central": 20,
            "ventilatie_mecanica": 25,
            "sonda_urinara": 15,
            "traheostomie": 20,
            "drenaj": 10,
            "peg": 12
        }
        
        self.resistance_weights = {
            "ESBL": 15,
            "CRE": 25,
            "KPC": 30,
            "NDM": 35,
            "MRSA": 20,
            "VRE": 25,
            "XDR": 30,
            "PDR": 40
        }
    
    def calculate_sofa(self, data: Dict) -> int:
        """Calculează SOFA score"""
        score = 0
        
        # Respirator
        pao2_fio2 = data.get("pao2_fio2", 400)
        if pao2_fio2 < 400: score += 1
        if pao2_fio2 < 300: score += 1
        if pao2_fio2 < 200: score += 1
        if pao2_fio2 < 100: score += 1
        
        # Coagulare
        platelets = data.get("trombocite", 200)
        if platelets < 150: score += 1
        if platelets < 100: score += 1
        if platelets < 50: score += 1
        if platelets < 20: score += 1
        
        # Hepatic
        bilirubin = data.get("bilirubina", 1.0)
        if bilirubin >= 1.2: score += 1
        if bilirubin >= 2.0: score += 1
        if bilirubin >= 6.0: score += 1
        if bilirubin >= 12.0: score += 1
        
        # Cardiovascular
        if data.get("hipotensiune"): score += 2
        if data.get("vasopresoare"): score += 1
        
        # Neurologic
        glasgow = data.get("glasgow", 15)
        if glasgow < 15: score += 1
        if glasgow < 13: score += 1
        if glasgow < 10: score += 1
        if glasgow < 6: score += 1
        
        # Renal
        creatinine = data.get("creatinina", 1.0)
        if creatinine >= 1.2: score += 1
        if creatinine >= 2.0: score += 1
        if creatinine >= 3.5: score += 1
        if creatinine >= 5.0: score += 1
        
        return score
    
    def calculate_qsofa(self, data: Dict) -> int:
        """Calculează qSOFA score"""
        score = 0
        if data.get("tas", 120) < 100: score += 1
        if data.get("frecventa_respiratorie", 18) >= 22: score += 1
        if data.get("glasgow", 15) < 15: score += 1
        return score
    
    def evaluate_lab_markers(self, data: Dict) -> Tuple[int, List[str]]:
        """Evaluează markerii de laborator"""
        score = 0
        details = []
        
        # Leucocite
        wbc = data.get("leucocite")
        if wbc:
            if wbc >= 12 or wbc < 4:
                score += 10
                status = "leucocitoză" if wbc >= 12 else "leucopenie"
                details.append(f"WBC {wbc} - {status} (+10)")
        
        # CRP
        crp = data.get("crp")
        if crp:
            if crp >= 100:
                score += 15
                details.append(f"CRP {crp} mg/L - inflamație severă (+15)")
            elif crp >= 50:
                score += 8
                details.append(f"CRP {crp} mg/L - inflamație moderată (+8)")
        
        # Procalcitonina
        pct = data.get("procalcitonina")
        if pct:
            if pct >= 2.0:
                score += 20
                details.append(f"PCT {pct} ng/mL - risc sepsă (+20)")
            elif pct >= 0.5:
                score += 10
                details.append(f"PCT {pct} ng/mL - posibilă infecție (+10)")
        
        return score, details
    
    def predict_iaam_risk(self, data: Dict) -> Dict:
        """Calculează riscul IAAM complet"""
        score = 0
        details = []
        
        # Verificare criteriu temporal
        hours = data.get("ore_spitalizare", 0)
        if hours < 48:
            return {
                "score": 0,
                "level": "NU IAAM",
                "details": [f"Internare {hours}h < 48h - criteriu temporal negativ"],
                "recommendations": ["Monitorizare standard"],
                "is_iaam": False
            }
        
        # Timp spitalizare
        if 48 <= hours < 72:
            score += 5
            details.append(f"Spitalizare {hours}h (+5)")
        elif hours < 168:
            score += 10
            details.append(f"Spitalizare {hours}h (+10)")
        else:
            score += 15
            details.append(f"Spitalizare {hours}h (+15)")
        
        # Dispozitive invazive
        for device, weight in self.device_weights.items():
            if data.get(device):
                days = data.get(f"{device}_days", 0)
                extra = 10 if days > 7 else 5 if days > 3 else 0
                total = weight + extra
                score += total
                details.append(f"{device.replace('_', ' ').title()} {days} zile (+{total})")
        
        # Microbiologie
        if data.get("cultura_pozitiva"):
            score += 15
            bacteria = data.get("bacterie", "necunoscută")
            details.append(f"Cultură pozitivă: {bacteria} (+15)")
            
            # Rezistențe
            for resistance in data.get("rezistente", []):
                points = self.resistance_weights.get(resistance, 10)
                score += points
                details.append(f"Rezistență {resistance} (+{points})")
        
        # Scoruri severitate
        sofa_score = self.calculate_sofa(data)
        if sofa_score > 0:
            sofa_points = sofa_score * 3
            score += sofa_points
            details.append(f"SOFA {sofa_score} (+{sofa_points})")
        
        qsofa_score = self.calculate_qsofa(data)
        if qsofa_score >= 2:
            score += 15
            details.append(f"qSOFA {qsofa_score} (+15)")
        
        # Markeri laborator
        lab_score, lab_details = self.evaluate_lab_markers(data)
        score += lab_score
        details.extend(lab_details)
        
        # Determinare nivel risc
        if score >= 120:
            level = "CRITIC"
            recommendations = [
                "🚨 Izolare imediată și notificare CPIAAM",
                "📞 Consult infecționist URGENT",
                "🧪 Recoltare probe și ATB empirică largă",
                "💊 Considerare terapie suport intensivă"
            ]
        elif score >= 90:
            level = "FOARTE ÎNALT"
            recommendations = [
                "⚠️ Consult infecționist în 2 ore",
                "🧪 Recoltare culturi și antibiogramă", 
                "🛡️ Izolare preventivă"
            ]
        elif score >= 60:
            level = "ÎNALT"
            recommendations = [
                "👁️ Supraveghere activă IAAM",
                "🧪 Recoltare culturi țintite",
                "📊 Monitorizare parametri la 8h"
            ]
        elif score >= 35:
            level = "MODERAT"
            recommendations = [
                "📋 Monitorizare extinsă",
                "📝 Documentare completă"
            ]
        else:
            level = "SCĂZUT"
            recommendations = [
                "✅ Monitorizare standard",
                "🧤 Precauții standard"
            ]
        
        return {
            "score": int(score),
            "level": level,
            "details": details,
            "recommendations": recommendations,
            "is_iaam": True,
            "sofa_score": sofa_score,
            "qsofa_score": qsofa_score
        }

class MedicalDataExtractor:
    """Extrage date medicale din text natural"""
    
    def __init__(self):
        self.patterns = {
            "leucocite": [r"(?:leucocite|wbc|gb)[\s:]*(\d+(?:\.\d+)?)", r"(\d+(?:\.\d+)?)\s*(?:x\s*)?10\^?3.*leucocite"],
            "crp": [r"crp[\s:]*(\d+(?:\.\d+)?)", r"proteina\s+c\s+reactiva[\s:]*(\d+(?:\.\d+)?)"],
            "procalcitonina": [r"(?:procalcitonina|pct)[\s:]*(\d+(?:\.\d+)?)"],
            "temperatura": [r"(?:temperatura|temp)[\s:]*(\d+(?:\.\d+)?)\s*°?c?"],
            "frecventa_cardiaca": [r"(?:puls|fc|hr)[\s:]*(\d+)"],
            "tas": [r"(?:ta|tensiune|pas)[\s:]*(\d+)/\d+", r"systolic[\s:]*(\d+)"],
            "tad": [r"(?:ta|tensiune|pad)[\s:]*\d+/(\d+)", r"diastolic[\s:]*(\d+)"],
            "frecventa_respiratorie": [r"(?:fr|resp)[\s:]*(\d+)"],
            "glasgow": [r"(?:glasgow|gcs)[\s:]*(\d+)"],
            "creatinina": [r"creatinina[\s:]*(\d+(?:\.\d+)?)"],
            "bilirubina": [r"bilirubina[\s:]*(\d+(?:\.\d+)?)"],
            "trombocite": [r"(?:trombocite|plt)[\s:]*(\d+(?:\.\d+)?)"],
            "ore_spitalizare": [r"(?:internare|spitalizare|zile)[\s:]*(\d+)"]
        }
        
        self.bacteria_patterns = [
            (r"escherichia\s+coli|e\.?\s*coli", "Escherichia coli"),
            (r"klebsiella\s+pneumoniae", "Klebsiella pneumoniae"),
            (r"pseudomonas\s+aeruginosa", "Pseudomonas aeruginosa"),
            (r"staphylococcus\s+aureus", "Staphylococcus aureus"),
            (r"acinetobacter\s+baumannii", "Acinetobacter baumannii"),
        ]
        
        self.resistance_patterns = [
            (r"esbl\+?|extended.spectrum", "ESBL"),
            (r"mrsa|methicillin.resistant", "MRSA"),
            (r"vre|vancomycin.resistant", "VRE"),
            (r"cre|carbapenem.resistant", "CRE"),
        ]
    
    def extract_from_text(self, text: str) -> Dict:
        """Extrage date medicale din text"""
        text_lower = text.lower()
        extracted = {}
        
        # Extrage valori numerice
        for key, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    try:
                        extracted[key] = float(match.group(1))
                        break
                    except:
                        continue
        
        # Extrage bacterii
        for pattern, name in self.bacteria_patterns:
            if re.search(pattern, text_lower):
                extracted["cultura_pozitiva"] = True
                extracted["bacterie"] = name
                break
        
        # Extrage rezistențe
        resistances = []
        for pattern, name in self.resistance_patterns:
            if re.search(pattern, text_lower):
                resistances.append(name)
        
        if resistances:
            extracted["rezistente"] = resistances
        
        # Detectează dispozitive
        device_keywords = {
            "cateter_central": ["cateter central", "cvc", "cateter venos"],
            "ventilatie_mecanica": ["ventilatie", "intubat", "respirator"],
            "sonda_urinara": ["sonda urinara", "cateter urinar", "foley"],
            "traheostomie": ["traheostomie", "canula"],
            "drenaj": ["dren", "drenaj"],
            "peg": ["peg", "gastrostomie"]
        }
        
        for device, keywords in device_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    extracted[device] = True
                    # Încearcă să găsească numărul de zile
                    days_pattern = rf"{keyword}.*?(\d+)\s*(?:zile|days)"
                    days_match = re.search(days_pattern, text_lower)
                    if days_match:
                        extracted[f"{device}_days"] = int(days_match.group(1))
                    break
        
        return extracted

# ============================================================================
# INTERFAȚĂ CHAT
# ============================================================================

class ChatInterface:
    """Interfață chat pentru interacțiunea cu AI"""
    
    def __init__(self):
        self.ai = OllamaAI()
        self.predictor = IAMPredictor()
        self.extractor = MedicalDataExtractor()
        
        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "patient_data" not in st.session_state:
            st.session_state.patient_data = {}
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
    
    def get_system_prompt(self) -> str:
        """Prompt-ul sistem pentru AI medical"""
        return """
        Ești un asistent medical AI specializat în evaluarea riscului de infecții asociate asistenței medicale (IAAM).

        MISIUNEA TA:
        1. Colectezi date medicale de la utilizator prin conversație naturală
        2. Extragi informații relevante pentru calculul riscului IAAM
        3. Ghidezi utilizatorul să furnizeze toate datele necesare
        4. Ești precis, profesional dar și empatic

        DATE NECESARE:
        - Timp spitalizare (ore)
        - Dispozitive invazive (CVC, ventilație, sondă urinară, etc.)
        - Parametri vitali (TA, FC, FR, temperatura)
        - Analize laborator (leucocite, CRP, procalcitonină)
        - Scoruri clinice (Glasgow)
        - Culturi microbiologice și rezistențe
        - Parametri SOFA (PaO2/FiO2, trombocite, bilirubină, creatinină)

        INSTRUCȚIUNI:
        - Pune întrebări clare și concise
        - Nu cere toate datele deodată
        - Adaptează-te la răspunsurile utilizatorului
        - Confirmă informațiile importante
        - Folosește terminologie medicală precisă
        - Răspunde DOAR în română
        - Fii concis (max 2-3 propoziții)

        IMPORTANT: Nu dai diagnoza finală - doar colectezi date pentru calculul riscului IAAM.
        """
    
    def process_user_input(self, user_input: str) -> str:
        """Procesează input-ul utilizatorului și generează răspuns"""
        
        # Extrage date medicale din input
        extracted_data = self.extractor.extract_from_text(user_input)
        
        # Actualizează datele pacientului
        if extracted_data:
            st.session_state.patient_data.update(extracted_data)
            
        # Pregătește context pentru AI
        current_data = st.session_state.patient_data
        data_summary = self.format_current_data(current_data)
        
        # Generează prompt pentru AI
        ai_prompt = f"""
        Utilizatorul a spus: "{user_input}"
        
        Date colectate până acum:
        {data_summary}
        
        Pe baza acestor informații, continuă conversația pentru a colecta datele lipsă.
        Dacă ai suficiente date pentru evaluarea IAAM, sugerează calcularea riscului.
        
        Răspuns (în română, concis):
        """
        
        # Obține răspuns de la AI
        ai_response = self.ai.generate(ai_prompt, self.get_system_prompt())
        
        return ai_response
    
    def format_current_data(self, data: Dict) -> str:
        """Formatează datele curente pentru AI"""
        if not data:
            return "Nu sunt date colectate încă."
        
        formatted = []
        for key, value in data.items():
            if isinstance(value, bool) and value:
                formatted.append(f"- {key}: Da")
            elif isinstance(value, (int, float)):
                formatted.append(f"- {key}: {value}")
            elif isinstance(value, str):
                formatted.append(f"- {key}: {value}")
            elif isinstance(value, list):
                formatted.append(f"- {key}: {', '.join(value)}")
        
        return "\n".join(formatted) if formatted else "Nu sunt date specifice."
    
    def can_calculate_risk(self) -> bool:
        """Verifică dacă avem suficiente date pentru calcul"""
        data = st.session_state.patient_data
        required_fields = ["ore_spitalizare"]
        return all(field in data for field in required_fields)
    
    def calculate_and_display_risk(self):
        """Calculează și afișează riscul IAAM"""
        if not self.can_calculate_risk():
            st.error("❌ Date insuficiente pentru calculul riscului IAAM!")
            return
        
        # Calculează riscul
        result = self.predictor.predict_iaam_risk(st.session_state.patient_data)
        
        # Afișează rezultatul
        self.display_risk_result(result)
        
        # Salvează în istoric
        st.session_state.chat_history.append({
            "timestamp": datetime.now(),
            "data": st.session_state.patient_data.copy(),
            "result": result
        })
    
    def display_risk_result(self, result: Dict):
        """Afișează rezultatul evaluării riscului"""
        level = result["level"]
        score = result["score"]
        
        # Selectează stilul pe baza nivelului
        if level == "CRITIC":
            css_class = "risk-critical"
        elif level == "FOARTE ÎNALT":
            css_class = "risk-high"
        elif level in ["ÎNALT", "MODERAT"]:
            css_class = "risk-moderate"
        else:
            css_class = "risk-low"
        
        # Afișează rezultatul principal
        st.markdown(f"""
        <div class="{css_class}">
            <h3>🎯 REZULTAT EVALUARE IAAM</h3>
            <h2>Scor: {score} | Nivel: {level}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Afișează metrici
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">SCOR TOTAL</div>
                <div class="metric-value">{score}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">SOFA</div>
                <div class="metric-value">{result.get('sofa_score', 0)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">qSOFA</div>
                <div class="metric-value">{result.get('qsofa_score', 0)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">RISC</div>
                <div class="metric-value" style="font-size: 1.2em;">{level}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Afișează detaliile
        if result["details"]:
            st.subheader("📋 Detalii calcul:")
            for detail in result["details"]:
                st.write(f"• {detail}")
        
        # Afișează recomandările
        if result["recommendations"]:
            st.subheader("💡 Recomandări:")
            for rec in result["recommendations"]:
                st.write(f"• {rec}")
        
        # Grafic de risc
        self.plot_risk_chart(result)
    
    def plot_risk_chart(self, result: Dict):
        """Creează grafic de risc"""
        fig = go.Figure()
        
        score = result["score"]
        level = result["level"]
        
        # Definește zonele de risc
        risk_zones = [
            {"name": "Scăzut", "min": 0, "max": 34, "color": "#10b981"},
            {"name": "Moderat", "min": 35, "max": 59, "color": "#3b82f6"},
            {"name": "Înalt", "min": 60, "max": 89, "color": "#f59e0b"},
            {"name": "Foarte Înalt", "min": 90, "max": 119, "color": "#f97316"},
            {"name": "Critic", "min": 120, "max": 200, "color": "#ef4444"}
        ]
        
        # Adaugă zonele de risc
        for zone in risk_zones:
            fig.add_shape(
                type="rect",
                x0=zone["min"], x1=zone["max"],
                y0=-0.5, y1=0.5,
                fillcolor=zone["color"],
                opacity=0.3,
                line=dict(width=0)
            )
        
        # Adaugă scorul actual
        fig.add_trace(go.Scatter(
            x=[score],
            y=[0],
            mode='markers',
            marker=dict(
                size=20,
                color='white',
                line=dict(color='black', width=2)
            ),
            name=f'Scor actual: {score}',
            hovertemplate=f'<b>Scor IAAM: {score}</b><br>Nivel: {level}<extra></extra>'
        ))
        
        # Configurează layout-ul
        fig.update_layout(
            title=f"Poziționare Risc IAAM - Scor: {score} ({level})",
            xaxis=dict(
                title="Scor IAAM",
                range=[-5, 205],
                showgrid=True
            ),
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                range=[-1, 1]
            ),
            height=200,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        # Adaugă etichete zone
        for zone in risk_zones:
            mid_point = (zone["min"] + zone["max"]) / 2
            fig.add_annotation(
                x=mid_point,
                y=0.3,
                text=zone["name"],
                showarrow=False,
                font=dict(color="white", size=10)
            )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Funcția principală a aplicației"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-bottom: 20px;">
        <h1>🤖 EpiMind AI - Predictor IAAM</h1>
        <h3>Chat Conversational pentru Evaluarea Riscului IAAM</h3>
        <p style="color: #a0aec0;">Vorbește natural cu AI-ul pentru a introduce datele pacientului</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inițializează chat interface
    chat = ChatInterface()
    
    # Verifică disponibilitatea AI
    if not chat.ai.available:
        st.error("""
        🚫 **Ollama nu este disponibil!**
        
        Pentru a folosi funcționalitatea AI:
        1. Instalează Ollama: https://ollama.ai/
        2. Rulează în terminal: `ollama pull llama2:7b`
        3. Pornește Ollama și încearcă din nou
        """)
        return
    
    # Layout principal
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Afișează istoricul conversației
        chat_container = st.container()
        
        with chat_container:
            # Mesaj inițial dacă nu există conversație
            if not st.session_state.messages:
                st.markdown("""
                <div class="message ai-message">
                    <strong>🤖 EpiMind AI:</strong><br>
                    Salut! Sunt asistentul tău AI pentru evaluarea riscului IAAM. 
                    Poți să-mi spui despre pacient în limba română, în mod natural.
                    <br><br>
                    <em>Exemple:</em><br>
                    • "Pacientul este internat de 5 zile, are CVC și ventilație mecanică"<br>
                    • "Leucocite 15.000, CRP 120, temperatură 38.5"<br>
                    • "Cultură pozitivă E.coli ESBL+"<br>
                </div>
                """, unsafe_allow_html=True)
            
            # Afișează toate mesajele
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="message user-message">
                        <strong>👤 Tu:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="message ai-message">
                        <strong>🤖 EpiMind AI:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input pentru conversație
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Scrie aici informațiile despre pacient...",
                placeholder="Ex: Pacientul are 72 ore de internare, CVC de 4 zile, leucocite 14000...",
                height=100,
                key="user_input"
            )
            
            col_send, col_calc, col_clear = st.columns([2, 2, 1])
            
            with col_send:
                submit_button = st.form_submit_button("💬 Trimite", type="primary")
            
            with col_calc:
                calc_button = st.form_submit_button("🎯 Calculează Risc")
            
            with col_clear:
                clear_button = st.form_submit_button("🗑️ Clear")
        
        # Procesează input-ul
        if submit_button and user_input:
            # Adaugă mesajul utilizatorului
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Procesează cu AI
            with st.spinner("🤖 AI procesează..."):
                ai_response = chat.process_user_input(user_input)
            
            # Adaugă răspunsul AI
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response
            })
            
            st.experimental_rerun()
        
        # Calculează riscul
        if calc_button:
            if chat.can_calculate_risk():
                chat.calculate_and_display_risk()
            else:
                st.error("❌ Date insuficiente! Cel puțin timpul de spitalizare este necesar.")
        
        # Clear chat
        if clear_button:
            st.session_state.messages = []
            st.session_state.patient_data = {}
            st.experimental_rerun()
    
    with col2:
        # Panou cu datele curente
        st.markdown("### 📊 Date Colectate")
        
        if st.session_state.patient_data:
            # Organizează datele pe categorii
            data_categories = {
                "🏥 Date generale": ["ore_spitalizare"],
                "🌡️ Parametri vitali": ["temperatura", "tas", "tad", "frecventa_cardiaca", "frecventa_respiratorie"],
                "🧪 Laborator": ["leucocite", "crp", "procalcitonina", "trombocite", "bilirubina", "creatinina"],
                "🏥 Dispozitive": ["cateter_central", "ventilatie_mecanica", "sonda_urinara", "traheostomie", "drenaj", "peg"],
                "🦠 Microbiologie": ["cultura_pozitiva", "bacterie", "rezistente"],
                "🧠 Neurologic": ["glasgow"],
                "💨 Respirator": ["pao2_fio2"],
                "💊 Cardiovascular": ["hipotensiune", "vasopresoare"]
            }
            
            for category, fields in data_categories.items():
                category_data = {k: v for k, v in st.session_state.patient_data.items() if k in fields}
                if category_data:
                    st.markdown(f"**{category}**")
                    for key, value in category_data.items():
                        display_key = key.replace("_", " ").title()
                        if isinstance(value, bool):
                            value_str = "✅ Da" if value else "❌ Nu"
                        elif isinstance(value, list):
                            value_str = ", ".join(value)
                        else:
                            value_str = str(value)
                        st.write(f"• {display_key}: {value_str}")
                    st.write("")
        else:
            st.info("💬 Începe conversația pentru a colecta date")
        
        # Progres completare
        st.markdown("### 📈 Progres Completare")
        essential_fields = [
            "ore_spitalizare", "leucocite", "crp", "temperatura",
            "tas", "frecventa_cardiaca", "glasgow"
        ]
        
        completed = sum(1 for field in essential_fields if field in st.session_state.patient_data)
        progress = completed / len(essential_fields)
        
        st.progress(progress)
        st.write(f"Completat: {completed}/{len(essential_fields)} câmpuri esențiale")
        
        # Istoricul evaluărilor
        if st.session_state.chat_history:
            st.markdown("### 📚 Istoric Evaluări")
            
            for i, entry in enumerate(reversed(st.session_state.chat_history[-5:])):
                with st.expander(f"Evaluare #{len(st.session_state.chat_history)-i}"):
                    st.write(f"⏰ {entry['timestamp'].strftime('%H:%M:%S')}")
                    st.write(f"🎯 Scor: {entry['result']['score']}")
                    st.write(f"📊 Nivel: {entry['result']['level']}")
                    
                    if st.button(f"📋 Vezi detalii", key=f"details_{i}"):
                        st.json(entry['result'])
        
        # Acțiuni rapide
        st.markdown("### ⚡ Acțiuni Rapide")
        
        if st.button("📝 Exemplu Pacient", key="example"):
            example_text = """
            Pacientul este internat de 96 ore în ATI. 
            Are cateter central de 5 zile și ventilație mecanică de 3 zile.
            Parametri vitali: TA 90/60, FC 110, FR 24, temperatură 38.8°C.
            Analize: leucocite 16.000, CRP 150, procalcitonină 3.2.
            Glasgow 12. Cultură pozitivă E.coli ESBL+.
            """
            
            # Simulează trimiterea exemplului
            st.session_state.messages.append({
                "role": "user",
                "content": example_text
            })
            
            # Extrage datele
            extracted = chat.extractor.extract_from_text(example_text)
            st.session_state.patient_data.update(extracted)
            
            # Răspuns AI
            ai_response = "Am înregistrat datele pacientului. Observ risc crescut: spitalizare >48h, dispozitive invazive multiple, markeri inflamatori foarte crescuți și cultură cu ESBL+. Să calculez riscul IAAM?"
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response
            })
            
            st.experimental_rerun()
        
        if st.button("🧹 Șterge Tot", key="clear_all"):
            for key in ["messages", "patient_data", "chat_history"]:
                st.session_state[key] = [] if key in ["messages", "chat_history"] else {}
            st.experimental_rerun()
        
        if st.button("💾 Exportă Date", key="export"):
            if st.session_state.patient_data:
                export_data = {
                    "timestamp": datetime.now().isoformat(),
                    "patient_data": st.session_state.patient_data,
                    "chat_history": st.session_state.chat_history
                }
                st.download_button(
                    "⬇️ Descarcă JSON",
                    data=json.dumps(export_data, indent=2, ensure_ascii=False),
                    file_name=f"epimind_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Footer cu informații
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0aec0; font-size: 0.9em;">
        <strong>EpiMind AI v3.0</strong> - Predictor IAAM cu AI Conversational<br>
        🏥 UMF "Grigore T. Popa" Iași | 🤖 Powered by Ollama | 📊 Scop educațional
    </div>
    """, unsafe_allow_html=True)

# Sidebar cu instrucțiuni
with st.sidebar:
    st.markdown("## 📖 Ghid Utilizare")
    
    st.markdown("""
    ### 🤖 Cum funcționează?
    1. **Vorbește natural** cu AI-ul în română
    2. **Menționează datele** medicale ale pacientului  
    3. **AI extrage automat** informațiile relevante
    4. **Calculează riscul** IAAM pe baza datelor
    
    ### 💬 Exemple de conversație:
    - "Pacientul are 72 ore, CVC de 4 zile"
    - "Leucocite 15000, CRP 120 mg/L"
    - "Cultură E.coli ESBL pozitiv"
    - "TA 85/50, FC 115, temp 38.9"
    
    ### ⚙️ Cerințe sistem:
    - **Ollama** instalat și rulând
    - Model **llama2:7b** descărcat
    - Conexiune internet pentru prima instalare
    """)
    
    st.markdown("### 🎯 Date necesare IAAM:")
    st.markdown("""
    - ⏰ Timp spitalizare (ore)
    - 🏥 Dispozitive invazive
    - 🌡️ Parametri vitali
    - 🧪 Analize laborator
    - 🦠 Culturi microbiologice
    - 🧠 Scor Glasgow
    - 💊 Status cardiovascular
    """)

if __name__ == "__main__":
    main()
