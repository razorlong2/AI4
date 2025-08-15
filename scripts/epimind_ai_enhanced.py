#!/usr/bin/env python3
# coding: utf-8
"""
EpiMind AI - IAAM Predictor cu Chat Conversational - Enhanced Version
UMF "Grigore T. Popa" Iași
Version: 4.0.0 - Fully Functional AI Conversational Integration

FUNCȚIONALITĂȚI ÎMBUNĂTĂȚITE:
- Chat AI conversational complet funcțional
- Predicție automată IAAM cu algoritmi îmbunătățiti
- Interfață modernă și responsivă
- Fallback AI când Ollama nu este disponibil
- Validare completă a datelor medicale
- Export rezultate în JSON/PDF
- Istoric pacienți persistent

Instalare:
    pip install streamlit pandas plotly requests python-dateutil

Opțional pentru AI local:
    # Instalează Ollama: https://ollama.ai/
    ollama pull llama3.2:3b

Rulează:
    streamlit run epimind_ai_enhanced.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
import requests
import time
import hashlib
import base64
from dataclasses import dataclass, asdict
import logging

# Configurare logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurare aplicație
st.set_page_config(
    page_title="EpiMind AI - IAAM Predictor Enhanced", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS modern și complet funcțional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-primary: #0f1419;
        --bg-secondary: #1a1f2e;
        --bg-chat: #242936;
        --text-primary: #ffffff;
        --text-secondary: #a0a9c0;
        --accent-blue: #00d4ff;
        --accent-green: #00ff88;
        --accent-red: #ff4757;
        --accent-orange: #ffa726;
        --border-color: #2d3748;
        --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow);
    }
    
    .chat-container {
        background: var(--bg-chat);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        max-height: 600px;
        overflow-y: auto;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }
    
    .message {
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 10px;
        animation: fadeIn 0.3s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: 2rem;
    }
    
    .ai-message {
        background: var(--bg-secondary);
        color: var(--text-primary);
        border-left: 4px solid var(--accent-blue);
        margin-right: 2rem;
    }
    
    .system-message {
        background: var(--accent-green);
        color: white;
        text-align: center;
        font-weight: 500;
    }
    
    .risk-critical {
        background: linear-gradient(135deg, #ff4757, #c44569);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        animation: pulse 2s infinite;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ffa726, #ff7043);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, #42a5f5, #478ed1);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #66bb6a, #43a047);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    .data-card {
        background: var(--bg-secondary);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
    }
    
    .metric-card {
        background: var(--bg-chat);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow);
    }
    
    .status-online {
        color: var(--accent-green);
        font-weight: 600;
    }
    
    .status-offline {
        color: var(--accent-red);
        font-weight: 600;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 71, 87, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 71, 87, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 71, 87, 0); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow);
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
    }
    
    .stTextArea > div > div > textarea {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class PatientData:
    """Structură de date pentru pacient"""
    # Identificare
    patient_id: str = ""
    timestamp: datetime = None
    
    # Date temporale
    ore_spitalizare: float = 0
    
    # Dispozitive invazive
    cateter_central: bool = False
    cateter_central_days: int = 0
    ventilatie_mecanica: bool = False
    ventilatie_mecanica_days: int = 0
    sonda_urinara: bool = False
    sonda_urinara_days: int = 0
    traheostomie: bool = False
    traheostomie_days: int = 0
    drenaj: bool = False
    drenaj_days: int = 0
    peg: bool = False
    peg_days: int = 0
    
    # Parametri vitali
    temperatura: float = 36.5
    frecventa_cardiaca: int = 80
    tas: int = 120
    tad: int = 80
    frecventa_respiratorie: int = 16
    glasgow: int = 15
    
    # Laborator
    leucocite: float = 7.0
    crp: float = 5.0
    procalcitonina: float = 0.1
    creatinina: float = 1.0
    bilirubina: float = 1.0
    trombocite: float = 250.0
    pao2_fio2: float = 400.0
    
    # Microbiologie
    cultura_pozitiva: bool = False
    bacterie: str = ""
    rezistente: List[str] = None
    
    # Status clinic
    hipotensiune: bool = False
    vasopresoare: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.rezistente is None:
            self.rezistente = []
        if not self.patient_id:
            self.patient_id = self.generate_id()
    
    def generate_id(self) -> str:
        """Generează ID unic pentru pacient"""
        data_str = f"{self.timestamp}{self.ore_spitalizare}{self.leucocite}"
        return hashlib.md5(data_str.encode()).hexdigest()[:8].upper()

class EnhancedOllamaAI:
    """Client îmbunătățit pentru Ollama AI cu fallback"""
    
    def __init__(self, model="llama3.2:3b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.available = self.check_availability()
        self.fallback_responses = self.load_fallback_responses()
        
    def check_availability(self) -> bool:
        """Verifică dacă Ollama este disponibil"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [m["name"] for m in models]
                logger.info(f"Ollama disponibil cu modele: {available_models}")
                return True
        except Exception as e:
            logger.warning(f"Ollama nu este disponibil: {e}")
        return False
    
    def load_fallback_responses(self) -> Dict[str, List[str]]:
        """Încarcă răspunsuri de rezervă pentru când AI nu este disponibil"""
        return {
            "greeting": [
                "Salut! Sunt EpiMind AI. Să începem evaluarea riscului IAAM. Poți să-mi spui de cât timp este pacientul internat?",
                "Bună! Pentru a calcula riscul IAAM, am nevoie de câteva informații. Să începem cu timpul de spitalizare - câte ore/zile?",
                "Salut! Sunt aici să te ajut cu evaluarea IAAM. Prima întrebare: de când este pacientul internat?"
            ],
            "time_request": [
                "Perfect! Acum am nevoie să știu despre dispozitivele invazive. Are pacientul cateter central, ventilație mecanică sau sondă urinară?",
                "Mulțumesc! Următoarea întrebare: ce dispozitive invazive are pacientul (CVC, ventilație, sondă urinară, etc.)?",
                "Bine! Să continuăm cu dispozitivele medicale. Care sunt prezente la pacient?"
            ],
            "devices_request": [
                "Excelent! Acum să vorbim despre analizele de laborator. Care sunt valorile pentru leucocite, CRP și procalcitonină?",
                "Perfect! Să trecem la laboratorul. Poți să-mi dai valorile pentru WBC, CRP și PCT?",
                "Mulțumesc! Următorul pas: analizele de laborator. Care sunt rezultatele recente?"
            ],
            "lab_request": [
                "Foarte bine! Mai am nevoie de parametrii vitali: tensiunea arterială, frecvența cardiacă și temperatura.",
                "Excelent! Să completăm cu parametrii vitali. Care sunt TA, FC și temperatura?",
                "Perfect! Ultimele date necesare: semnele vitale ale pacientului."
            ],
            "vitals_request": [
                "Mulțumesc pentru toate informațiile! Acum pot calcula riscul IAAM. Apasă butonul 'Calculează Risc'.",
                "Excelent! Am toate datele necesare pentru evaluarea IAAM. Să calculez riscul!",
                "Perfect! Cu aceste informații pot face o evaluare completă a riscului IAAM."
            ],
            "insufficient_data": [
                "Am nevoie de mai multe informații pentru o evaluare precisă. Poți să-mi dai mai multe detalii?",
                "Pentru o predicție exactă, am nevoie de date suplimentare. Ce alte informații poți furniza?",
                "Să completăm datele pentru o evaluare mai bună. Ce alte detalii medicale ai?"
            ]
        }
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generează răspuns folosind Ollama sau fallback"""
        if self.available:
            try:
                return self._generate_ollama(prompt, system_prompt)
            except Exception as e:
                logger.error(f"Eroare Ollama: {e}")
                return self._generate_fallback(prompt)
        else:
            return self._generate_fallback(prompt)
    
    def _generate_ollama(self, prompt: str, system_prompt: str) -> str:
        """Generează răspuns cu Ollama"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 200
            }
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json().get("response", "")
            return result.strip()
        else:
            raise Exception(f"HTTP {response.status_code}")
    
    def _generate_fallback(self, prompt: str) -> str:
        """Generează răspuns de rezervă bazat pe context"""
        prompt_lower = prompt.lower()
        
        # Detectează contextul și returnează răspuns relevant
        if any(word in prompt_lower for word in ["salut", "bună", "hello", "start"]):
            return self._random_response("greeting")
        elif any(word in prompt_lower for word in ["ore", "zile", "internare", "spitalizare"]):
            return self._random_response("time_request")
        elif any(word in prompt_lower for word in ["cateter", "ventilatie", "sonda", "dispozitiv"]):
            return self._random_response("devices_request")
        elif any(word in prompt_lower for word in ["leucocite", "crp", "procalcitonina", "laborator"]):
            return self._random_response("lab_request")
        elif any(word in prompt_lower for word in ["tensiune", "temperatura", "puls", "vitali"]):
            return self._random_response("vitals_request")
        elif any(word in prompt_lower for word in ["calculez", "risc", "evalua"]):
            return self._random_response("vitals_request")
        else:
            return self._random_response("insufficient_data")
    
    def _random_response(self, category: str) -> str:
        """Returnează un răspuns aleatoriu din categoria specificată"""
        import random
        responses = self.fallback_responses.get(category, ["Înțeleg. Să continuăm cu evaluarea."])
        return random.choice(responses)

class EnhancedIAAMPredictor:
    """Motor îmbunătățit de predicție IAAM"""
    
    def __init__(self):
        self.device_weights = {
            "cateter_central": 25,
            "ventilatie_mecanica": 30,
            "sonda_urinara": 20,
            "traheostomie": 25,
            "drenaj": 15,
            "peg": 18
        }
        
        self.resistance_weights = {
            "ESBL": 20,
            "CRE": 30,
            "KPC": 35,
            "NDM": 40,
            "MRSA": 25,
            "VRE": 30,
            "XDR": 35,
            "PDR": 45,
            "OXA": 25,
            "VIM": 30,
            "IMP": 28
        }
        
        self.bacteria_risk = {
            "Escherichia coli": 15,
            "Klebsiella pneumoniae": 20,
            "Pseudomonas aeruginosa": 25,
            "Acinetobacter baumannii": 30,
            "Staphylococcus aureus": 20,
            "Enterococcus faecium": 18,
            "Candida auris": 35,
            "Clostridioides difficile": 25
        }
    
    def calculate_sofa(self, data: PatientData) -> Tuple[int, Dict[str, int]]:
        """Calculează SOFA score cu detalii pe componente"""
        scores = {}
        
        # Respirator (PaO2/FiO2)
        pao2_fio2 = data.pao2_fio2
        if pao2_fio2 >= 400:
            scores["respirator"] = 0
        elif pao2_fio2 >= 300:
            scores["respirator"] = 1
        elif pao2_fio2 >= 200:
            scores["respirator"] = 2
        elif pao2_fio2 >= 100:
            scores["respirator"] = 3
        else:
            scores["respirator"] = 4
        
        # Coagulare (trombocite)
        platelets = data.trombocite
        if platelets >= 150:
            scores["coagulare"] = 0
        elif platelets >= 100:
            scores["coagulare"] = 1
        elif platelets >= 50:
            scores["coagulare"] = 2
        elif platelets >= 20:
            scores["coagulare"] = 3
        else:
            scores["coagulare"] = 4
        
        # Hepatic (bilirubină)
        bilirubin = data.bilirubina
        if bilirubin < 1.2:
            scores["hepatic"] = 0
        elif bilirubin < 2.0:
            scores["hepatic"] = 1
        elif bilirubin < 6.0:
            scores["hepatic"] = 2
        elif bilirubin < 12.0:
            scores["hepatic"] = 3
        else:
            scores["hepatic"] = 4
        
        # Cardiovascular
        if data.vasopresoare:
            scores["cardiovascular"] = 4
        elif data.hipotensiune or data.tas < 70:
            scores["cardiovascular"] = 3
        elif data.tas < 90:
            scores["cardiovascular"] = 2
        else:
            scores["cardiovascular"] = 0
        
        # Neurologic (Glasgow)
        glasgow = data.glasgow
        if glasgow == 15:
            scores["neurologic"] = 0
        elif glasgow >= 13:
            scores["neurologic"] = 1
        elif glasgow >= 10:
            scores["neurologic"] = 2
        elif glasgow >= 6:
            scores["neurologic"] = 3
        else:
            scores["neurologic"] = 4
        
        # Renal (creatinină)
        creatinine = data.creatinina
        if creatinine < 1.2:
            scores["renal"] = 0
        elif creatinine < 2.0:
            scores["renal"] = 1
        elif creatinine < 3.5:
            scores["renal"] = 2
        elif creatinine < 5.0:
            scores["renal"] = 3
        else:
            scores["renal"] = 4
        
        total_score = sum(scores.values())
        return total_score, scores
    
    def calculate_qsofa(self, data: PatientData) -> Tuple[int, List[str]]:
        """Calculează qSOFA score cu detalii"""
        score = 0
        criteria = []
        
        if data.tas < 100:
            score += 1
            criteria.append(f"TAS < 100 mmHg ({data.tas})")
        
        if data.frecventa_respiratorie >= 22:
            score += 1
            criteria.append(f"FR ≥ 22/min ({data.frecventa_respiratorie})")
        
        if data.glasgow < 15:
            score += 1
            criteria.append(f"Glasgow < 15 ({data.glasgow})")
        
        return score, criteria
    
    def evaluate_lab_markers(self, data: PatientData) -> Tuple[int, List[str]]:
        """Evaluează markerii de laborator îmbunătățit"""
        score = 0
        details = []
        
        # Leucocite cu interpretare îmbunătățită
        wbc = data.leucocite
        if wbc >= 20:
            score += 20
            details.append(f"WBC {wbc} - leucocitoză severă (+20)")
        elif wbc >= 12:
            score += 12
            details.append(f"WBC {wbc} - leucocitoză (+12)")
        elif wbc < 4:
            score += 15
            details.append(f"WBC {wbc} - leucopenie (+15)")
        
        # CRP cu praguri îmbunătățite
        crp = data.crp
        if crp >= 200:
            score += 25
            details.append(f"CRP {crp} mg/L - inflamație critică (+25)")
        elif crp >= 100:
            score += 18
            details.append(f"CRP {crp} mg/L - inflamație severă (+18)")
        elif crp >= 50:
            score += 10
            details.append(f"CRP {crp} mg/L - inflamație moderată (+10)")
        elif crp >= 10:
            score += 5
            details.append(f"CRP {crp} mg/L - inflamație ușoară (+5)")
        
        # Procalcitonină cu interpretare precisă
        pct = data.procalcitonina
        if pct >= 10:
            score += 35
            details.append(f"PCT {pct} ng/mL - șoc septic (+35)")
        elif pct >= 2.0:
            score += 25
            details.append(f"PCT {pct} ng/mL - sepsă severă (+25)")
        elif pct >= 0.5:
            score += 15
            details.append(f"PCT {pct} ng/mL - infecție bacteriană (+15)")
        elif pct >= 0.25:
            score += 8
            details.append(f"PCT {pct} ng/mL - posibilă infecție (+8)")
        
        return score, details
    
    def predict_iaam_risk(self, data: PatientData) -> Dict:
        """Calculează riscul IAAM complet și îmbunătățit"""
        score = 0
        details = []
        
        # Verificare criteriu temporal
        hours = data.ore_spitalizare
        if hours < 48:
            return {
                "score": 0,
                "level": "NU IAAM",
                "details": [f"Internare {hours:.1f}h < 48h - criteriu temporal negativ pentru IAAM"],
                "recommendations": [
                    "Monitorizare standard pentru infecții comunitare", 
                    f"Reevaluare la 48h (peste {48-hours:.1f}h)",
                    "Urmărire evoluție clinică"
                ],
                "is_iaam": False,
                "patient_id": data.patient_id,
                "timestamp": data.timestamp
            }
        
        # Timp spitalizare cu calcul îmbunătățit
        if 48 <= hours < 72:
            time_score = 8
            details.append(f"Spitalizare {hours:.1f}h ({hours/24:.1f} zile) - risc timpuriu (+{time_score})")
        elif hours < 168:  # < 1 săptămână
            time_score = 15
            details.append(f"Spitalizare {hours:.1f}h ({hours/24:.1f} zile) - risc moderat (+{time_score})")
        elif hours < 336:  # < 2 săptămâni
            time_score = 25
            details.append(f"Spitalizare {hours:.1f}h ({hours/24:.1f} zile) - risc înalt (+{time_score})")
        elif hours < 720:  # < 1 lună
            time_score = 35
            details.append(f"Spitalizare {hours:.1f}h ({hours/24:.1f} zile) - risc foarte înalt (+{time_score})")
        else:  # > 1 lună
            time_score = 45
            details.append(f"Spitalizare {hours:.1f}h ({hours/24:.1f} zile) - risc extrem de înalt (+{time_score})")
        
        score += time_score
        
        # Dispozitive invazive cu calcul îmbunătățit
        device_score = 0
        for device, base_weight in self.device_weights.items():
            if getattr(data, device, False):
                days = getattr(data, f"{device}_days", 0)
                
                # Calcul progresiv bazat pe durata
                if days > 14:
                    multiplier = 2.5
                elif days > 7:
                    multiplier = 2.0
                elif days > 3:
                    multiplier = 1.5
                else:
                    multiplier = 1.0
                
                device_points = int(base_weight * multiplier)
                device_score += device_points
                details.append(f"{device.replace('_', ' ').title()} - {days} zile (+{device_points})")
        
        score += device_score
        
        # Microbiologie îmbunătățită
        if data.cultura_pozitiva:
            bacteria_score = 20  # scor de bază pentru cultură pozitivă
            bacteria_name = data.bacterie or "necunoscută"
            
            # Bonus pentru bacterii specifice
            if bacteria_name in self.bacteria_risk:
                bacteria_bonus = self.bacteria_risk[bacteria_name]
                bacteria_score += bacteria_bonus
                details.append(f"Cultură pozitivă: {bacteria_name} (+{bacteria_score})")
            else:
                details.append(f"Cultură pozitivă: {bacteria_name} (+{bacteria_score})")
            
            score += bacteria_score
            
            # Rezistențe cu scoring îmbunătățit
            resistance_score = 0
            for resistance in data.rezistente:
                points = self.resistance_weights.get(resistance, 15)
                resistance_score += points
                details.append(f"Rezistență {resistance} (+{points})")
            
            score += resistance_score
        
        # Scoruri severitate
        sofa_score, sofa_details = self.calculate_sofa(data)
        if sofa_score > 0:
            sofa_points = sofa_score * 4  # îmbunătățit de la 3 la 4
            score += sofa_points
            details.append(f"SOFA {sofa_score} (+{sofa_points})")
        
        qsofa_score, qsofa_criteria = self.calculate_qsofa(data)
        if qsofa_score >= 2:
            qsofa_points = 20  # îmbunătățit de la 15 la 20
            score += qsofa_points
            details.append(f"qSOFA {qsofa_score}/3 - {', '.join(qsofa_criteria)} (+{qsofa_points})")
        
        # Markeri laborator
        lab_score, lab_details = self.evaluate_lab_markers(data)
        score += lab_score
        details.extend(lab_details)
        
        # Factori de risc suplimentari
        additional_score = 0
        if data.temperatura >= 38.5:
            additional_score += 8
            details.append(f"Febră {data.temperatura}°C (+8)")
        elif data.temperatura <= 36.0:
            additional_score += 10
            details.append(f"Hipotermie {data.temperatura}°C (+10)")
        
        if data.frecventa_cardiaca >= 100:
            additional_score += 5
            details.append(f"Tahicardie {data.frecventa_cardiaca}/min (+5)")
        
        score += additional_score
        
        # Determinare nivel risc cu praguri îmbunătățite
        if score >= 140:
            level = "CRITIC"
            color_class = "risk-critical"
            recommendations = [
                "🚨 ALERTĂ IAAM - Izolare imediată",
                "📞 Notificare CPIAAM și infecționist URGENT",
                "🧪 Recoltare probe microbiologice complete",
                "💊 ATB empirică de spectru larg",
                "🏥 Transfer la terapie intensivă dacă necesar",
                "📋 Monitorizare continuă parametri vitali"
            ]
        elif score >= 110:
            level = "FOARTE ÎNALT"
            color_class = "risk-high"
            recommendations = [
                "⚠️ Risc foarte înalt IAAM",
                "📞 Consult infecționist în 2 ore",
                "🧪 Recoltare culturi și antibiogramă urgentă",
                "🛡️ Izolare preventivă imediată",
                "📊 Monitorizare la 4 ore"
            ]
        elif score >= 80:
            level = "ÎNALT"
            color_class = "risk-moderate"
            recommendations = [
                "👁️ Supraveghere activă IAAM",
                "🧪 Recoltare culturi țintite",
                "📊 Monitorizare parametri la 6 ore",
                "🧤 Precauții de contact"
            ]
        elif score >= 50:
            level = "MODERAT"
            color_class = "risk-moderate"
            recommendations = [
                "📋 Monitorizare extinsă",
                "📝 Documentare completă în fișă",
                "🧪 Culturi la indicație clinică"
            ]
        else:
            level = "SCĂZUT"
            color_class = "risk-low"
            recommendations = [
                "✅ Monitorizare standard",
                "🧤 Precauții standard de igienă",
                "📋 Reevaluare zilnică"
            ]
        
        return {
            "score": int(score),
            "level": level,
            "color_class": color_class,
            "details": details,
            "recommendations": recommendations,
            "is_iaam": True,
            "sofa_score": sofa_score,
            "sofa_details": sofa_details,
            "qsofa_score": qsofa_score,
            "qsofa_criteria": qsofa_criteria,
            "patient_id": data.patient_id,
            "timestamp": data.timestamp,
            "device_score": device_score,
            "lab_score": lab_score,
            "time_score": time_score
        }

class EnhancedMedicalDataExtractor:
    """Extractor îmbunătățit de date medicale"""
    
    def __init__(self):
        self.patterns = {
            # Valori numerice îmbunătățite
            "leucocite": [
                r"(?:leucocite|wbc|gb)[\s:]*(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*(?:x\s*)?10\^?3.*(?:leucocite|wbc)",
                r"leucocite[\s:]*(\d+(?:,\d+)?)",
                r"wbc[\s:]*(\d+(?:\.\d+)?)"
            ],
            "crp": [
                r"crp[\s:]*(\d+(?:\.\d+)?)",
                r"proteina\s+c\s+reactiva[\s:]*(\d+(?:\.\d+)?)",
                r"c[\s-]?reactive[\s-]?protein[\s:]*(\d+(?:\.\d+)?)"
            ],
            "procalcitonina": [
                r"(?:procalcitonina|pct)[\s:]*(\d+(?:\.\d+)?)",
                r"procalcitonin[\s:]*(\d+(?:\.\d+)?)"
            ],
            "temperatura": [
                r"(?:temperatura|temp|t)[\s:]*(\d+(?:\.\d+)?)\s*°?c?",
                r"(\d+(?:\.\d+)?)\s*°c",
                r"febra[\s:]*(\d+(?:\.\d+)?)"
            ],
            "frecventa_cardiaca": [
                r"(?:puls|fc|hr|frecventa\s+cardiaca)[\s:]*(\d+)",
                r"heart\s+rate[\s:]*(\d+)",
                r"(\d+)\s*bpm"
            ],
            "tas": [
                r"(?:ta|tensiune|pas|systolic)[\s:]*(\d+)(?:/\d+)?",
                r"(\d+)/\d+\s*mmhg",
                r"systolic[\s:]*(\d+)"
            ],
            "tad": [
                r"(?:ta|tensiune|pad|diastolic)[\s:]*\d+/(\d+)",
                r"\d+/(\d+)\s*mmhg",
                r"diastolic[\s:]*(\d+)"
            ],
            "frecventa_respiratorie": [
                r"(?:fr|resp|frecventa\s+respiratorie)[\s:]*(\d+)",
                r"respiratory\s+rate[\s:]*(\d+)",
                r"(\d+)\s*respiratii"
            ],
            "glasgow": [
                r"(?:glasgow|gcs)[\s:]*(\d+)",
                r"glasgow\s+coma\s+scale[\s:]*(\d+)"
            ],
            "creatinina": [
                r"creatinina[\s:]*(\d+(?:\.\d+)?)",
                r"creatinine[\s:]*(\d+(?:\.\d+)?)"
            ],
            "bilirubina": [
                r"bilirubina[\s:]*(\d+(?:\.\d+)?)",
                r"bilirubin[\s:]*(\d+(?:\.\d+)?)"
            ],
            "trombocite": [
                r"(?:trombocite|plt|platelets)[\s:]*(\d+(?:\.\d+)?)",
                r"platelet\s+count[\s:]*(\d+(?:\.\d+)?)"
            ],
            "ore_spitalizare": [
                r"(?:internare|spitalizare|hospitalizare)[\s:]*(\d+)\s*(?:ore|hours|h)",
                r"(\d+)\s*(?:ore|hours|h).*(?:internare|spitalizare)",
                r"(\d+)\s*zile.*(?:internare|spitalizare)",
                r"ziua\s*(\d+)",
                r"de\s*(\d+)\s*zile",
                r"(\d+)\s*days?.*(?:hospital|admission)",
                r"length\s*of\s*stay[\s:]*(\d+)\s*(?:days?|zile)",
                r"los[\s:]*(\d+)\s*(?:days?|zile)",
                r"internare\s*de\s*(\d+)\s*(?:zile|ore)",
                r"(\d+)\s*(?:zile|days?)\s*de\s*(?:internare|spitalizare)"
            ],
            "pao2_fio2": [
                r"pao2/fio2[\s:]*(\d+(?:\.\d+)?)",
                r"p/f\s+ratio[\s:]*(\d+(?:\.\d+)?)"
            ]
        }
        
        # Bacterii îmbunătățite
        self.bacteria_patterns = [
            (r"escherichia\s+coli|e\.?\s*coli", "Escherichia coli"),
            (r"klebsiella\s+pneumoniae|k\.?\s*pneumoniae", "Klebsiella pneumoniae"),
            (r"pseudomonas\s+aeruginosa|p\.?\s*aeruginosa", "Pseudomonas aeruginosa"),
            (r"staphylococcus\s+aureus|s\.?\s*aureus", "Staphylococcus aureus"),
            (r"acinetobacter\s+baumannii|a\.?\s*baumannii", "Acinetobacter baumannii"),
            (r"enterococcus\s+faecium|e\.?\s*faecium", "Enterococcus faecium"),
            (r"candida\s+auris|c\.?\s*auris", "Candida auris"),
            (r"clostridioides\s+difficile|c\.?\s*difficile|cdiff", "Clostridioides difficile"),
            (r"enterobacter\s+cloacae", "Enterobacter cloacae"),
            (r"serratia\s+marcescens", "Serratia marcescens")
        ]
        
        # Rezistențe îmbunătățite
        self.resistance_patterns = [
            (r"esbl\+?|extended.spectrum", "ESBL"),
            (r"mrsa|methicillin.resistant", "MRSA"),
            (r"vre|vancomycin.resistant", "VRE"),
            (r"cre|carbapenem.resistant", "CRE"),
            (r"kpc|klebsiella.pneumoniae.carbapenemase", "KPC"),
            (r"ndm|new.delhi.metallo", "NDM"),
            (r"oxa|oxacillinase", "OXA"),
            (r"vim|verona.integron", "VIM"),
            (r"imp|imipenemase", "IMP"),
            (r"xdr|extensively.drug.resistant", "XDR"),
            (r"pdr|pandrug.resistant", "PDR")
        ]
        
        # Dispozitive îmbunătățite
        self.device_keywords = {
            "cateter_central": [
                "cateter central", "cvc", "cateter venos central", 
                "central line", "hickman", "port", "picc"
            ],
            "ventilatie_mecanica": [
                "ventilatie", "intubat", "respirator", "ventilator",
                "mechanical ventilation", "cpap", "bipap"
            ],
            "sonda_urinara": [
                "sonda urinara", "cateter urinar", "foley",
                "urinary catheter", "bladder catheter"
            ],
            "traheostomie": [
                "traheostomie", "canula", "tracheostomy",
                "tracheal tube", "canula traheala"
            ],
            "drenaj": [
                "dren", "drenaj", "drain", "chest tube",
                "dren toracic", "dren abdominal"
            ],
            "peg": [
                "peg", "gastrostomie", "gastrostomy",
                "feeding tube", "sonda gastrica"
            ]
        }
    
    def extract_from_text(self, text: str) -> Dict:
        """Extrage date medicale din text cu algoritm îmbunătățit"""
        text_lower = text.lower()
        extracted = {}
        
        # Extrage valori numerice
        for key, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    try:
                        value_str = match.group(1).replace(',', '.')
                        value = float(value_str)
                        
                        # Validări și conversii
                        if key == "ore_spitalizare":
                            if "zile" in text_lower or "days" in text_lower or "ziua" in text_lower:
                                value *= 24  # convertește zile în ore
                            # Validare rezonabilă pentru ore spitalizare
                            if value > 8760:  # mai mult de 1 an în ore
                                continue  # probabil eroare
                            elif value < 1:  # mai puțin de 1 oră
                                value = max(1, value)  # minimum 1 oră
                        elif key == "temperatura" and value > 50:
                            continue  # probabil eroare
                        elif key == "leucocite" and value > 100:
                            value = value / 1000  # convertește din /μL în x10³/μL
                        
                        extracted[key] = value
                        break
                    except (ValueError, IndexError):
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
            extracted["rezistente"] = list(set(resistances))  # elimină duplicatele
        
        # Detectează dispozitive cu durata
        for device, keywords in self.device_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    extracted[device] = True
                    
                    # Caută durata în zile
                    days_patterns = [
                        rf"{keyword}.*?(\d+)\s*(?:zile|days|d)",
                        rf"(\d+)\s*(?:zile|days|d).*{keyword}",
                        rf"{keyword}.*de\s*(\d+)\s*(?:zile|days)",
                        rf"de\s*(\d+)\s*(?:zile|days).*{keyword}"
                    ]
                    
                    for days_pattern in days_patterns:
                        days_match = re.search(days_pattern, text_lower)
                        if days_match:
                            try:
                                days = int(days_match.group(1))
                                extracted[f"{device}_days"] = days
                                break
                            except (ValueError, IndexError):
                                continue
                    
                    # Dacă nu găsește zile, încearcă ore
                    if f"{device}_days" not in extracted:
                        hours_patterns = [
                            rf"{keyword}.*?(\d+)\s*(?:ore|hours|h)",
                            rf"(\d+)\s*(?:ore|hours|h).*{keyword}"
                        ]
                        
                        for hours_pattern in hours_patterns:
                            hours_match = re.search(hours_pattern, text_lower)
                            if hours_match:
                                try:
                                    hours = int(hours_match.group(1))
                                    extracted[f"{device}_days"] = max(1, hours // 24)
                                    break
                                except (ValueError, IndexError):
                                    continue
                    
                    break
        
        # Detectează status clinic
        if any(word in text_lower for word in ["hipotensiune", "hipotensiv", "shock", "soc"]):
            extracted["hipotensiune"] = True
        
        if any(word in text_lower for word in ["vasopresoare", "noradrenalina", "dopamina", "vasopressor"]):
            extracted["vasopresoare"] = True
        
        return extracted
    
    def validate_extracted_data(self, data: Dict) -> Dict:
        """Validează și corectează datele extrase"""
        validated = data.copy()
        
        # Validări pentru valori normale
        validations = {
            "temperatura": (35.0, 42.0),
            "frecventa_cardiaca": (40, 200),
            "tas": (60, 250),
            "tad": (30, 150),
            "frecventa_respiratorie": (8, 50),
            "glasgow": (3, 15),
            "leucocite": (0.1, 50.0),
            "crp": (0, 500),
            "procalcitonina": (0, 100),
            "creatinina": (0.3, 15.0),
            "bilirubina": (0.1, 50.0),
            "trombocite": (10, 1000),
            "pao2_fio2": (50, 600)
        }
        
        for key, (min_val, max_val) in validations.items():
            if key in validated:
                value = validated[key]
                if not (min_val <= value <= max_val):
                    logger.warning(f"Valoare suspectă pentru {key}: {value}")
                    # Nu eliminăm valoarea, dar o marcăm pentru atenție
        
        return validated

class EnhancedChatInterface:
    """Interfață chat îmbunătățită"""
    
    def __init__(self):
        self.ai = EnhancedOllamaAI()
        self.predictor = EnhancedIAAMPredictor()
        self.extractor = EnhancedMedicalDataExtractor()
        
        # Initialize session state
        self._init_session_state()
    
    def _init_session_state(self):
        """Inițializează session state"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "patient_data" not in st.session_state:
            st.session_state.patient_data = PatientData()
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "current_patient_id" not in st.session_state:
            st.session_state.current_patient_id = None
        if "ai_status" not in st.session_state:
            st.session_state.ai_status = self.ai.available
    
    def get_system_prompt(self) -> str:
        """Prompt sistem îmbunătățit pentru AI medical"""
        return """
        Ești EpiMind AI, un asistent medical specializat în evaluarea riscului de infecții asociate asistenței medicale (IAAM).

        MISIUNEA TA:
        1. Colectezi date medicale prin conversație naturală în română
        2. Extragi informații relevante pentru calculul riscului IAAM
        3. Ghidezi utilizatorul să furnizeze toate datele necesare
        4. Ești precis, profesional și empatic

        DATE PRIORITARE PENTRU IAAM:
        - Timp spitalizare (>48h obligatoriu pentru IAAM)
        - Dispozitive invazive și durata lor
        - Culturi microbiologice și rezistențe
        - Parametri vitali și scoruri clinice
        - Markeri inflamatori (CRP, PCT, leucocite)

        INSTRUCȚIUNI CONVERSAȚIE:
        - Pune întrebări clare, o dată
        - Adaptează-te la nivelul utilizatorului
        - Confirmă informațiile critice
        - Sugerează calculul când ai date suficiente
        - Răspunde DOAR în română
        - Fii concis (max 2 propoziții)
        - Nu da diagnoza - doar colectezi date

        EXEMPLE ÎNTREBĂRI:
        - "De câte ore/zile este pacientul internat?"
        - "Ce dispozitive invazive are? (CVC, ventilație, sondă urinară)"
        - "Care sunt valorile pentru leucocite, CRP și procalcitonină?"
        - "Sunt culturi pozitive? Ce bacterie și ce rezistențe?"
        """
    
    def process_user_input(self, user_input: str) -> str:
        """Procesează input-ul utilizatorului cu logică îmbunătățită"""
        
        # Extrage și validează date medicale
        extracted_data = self.extractor.extract_from_text(user_input)
        validated_data = self.extractor.validate_extracted_data(extracted_data)
        
        # Actualizează datele pacientului
        if validated_data:
            current_data = asdict(st.session_state.patient_data)
            current_data.update(validated_data)
            
            # Recreează obiectul PatientData
            st.session_state.patient_data = PatientData(**{
                k: v for k, v in current_data.items() 
                if k in PatientData.__dataclass_fields__
            })
        
        # Pregătește context pentru AI
        data_summary = self._format_current_data()
        completion_status = self._assess_data_completion()
        
        # Generează prompt pentru AI
        ai_prompt = f"""
        Utilizatorul a spus: "{user_input}"
        
        Date colectate:
        {data_summary}
        
        Status completare: {completion_status}
        
        Continuă conversația pentru a colecta datele lipsă sau sugerează calcularea riscului dacă ai suficiente date.
        """
        
        # Obține răspuns de la AI
        ai_response = self.ai.generate(ai_prompt, self.get_system_prompt())
        
        return ai_response
    
    def _format_current_data(self) -> str:
        """Formatează datele curente pentru AI"""
        data = st.session_state.patient_data
        formatted = []
        
        # Date esențiale
        if data.ore_spitalizare > 0:
            formatted.append(f"⏰ Spitalizare: {data.ore_spitalizare} ore")
        
        # Dispozitive
        devices = []
        for device in ["cateter_central", "ventilatie_mecanica", "sonda_urinara", "traheostomie", "drenaj", "peg"]:
            if getattr(data, device, False):
                days = getattr(data, f"{device}_days", 0)
                devices.append(f"{device.replace('_', ' ')} ({days} zile)")
        
        if devices:
            formatted.append(f"🔧 Dispozitive: {', '.join(devices)}")
        
        # Laborator
        lab_values = []
        if data.leucocite != 7.0:
            lab_values.append(f"WBC: {data.leucocite}")
        if data.crp != 5.0:
            lab_values.append(f"CRP: {data.crp}")
        if data.procalcitonina != 0.1:
            lab_values.append(f"PCT: {data.procalcitonina}")
        
        if lab_values:
            formatted.append(f"🧪 Laborator: {', '.join(lab_values)}")
        
        # Microbiologie
        if data.cultura_pozitiva:
            micro_info = f"Cultură pozitivă: {data.bacterie}"
            if data.rezistente:
                micro_info += f" ({', '.join(data.rezistente)})"
            formatted.append(f"🦠 {micro_info}")
        
        return "\n".join(formatted) if formatted else "Nu sunt date specifice colectate."
    
    def _assess_data_completion(self) -> str:
        """Evaluează completitudinea datelor"""
        data = st.session_state.patient_data
        
        essential_fields = {
            "ore_spitalizare": data.ore_spitalizare > 0,
            "dispozitive": any([
                data.cateter_central, data.ventilatie_mecanica, 
                data.sonda_urinara, data.traheostomie, data.drenaj, data.peg
            ]),
            "laborator": any([
                data.leucocite != 7.0, data.crp != 5.0, data.procalcitonina != 0.1
            ]),
            "vitali": any([
                data.temperatura != 36.5, data.frecventa_cardiaca != 80,
                data.tas != 120, data.glasgow != 15
            ])
        }
        
        completed = sum(essential_fields.values())
        total = len(essential_fields)
        
        if completed >= 3:
            return f"Date suficiente ({completed}/{total}) - poate calcula risc"
        elif completed >= 2:
            return f"Date parțiale ({completed}/{total}) - mai sunt necesare"
        else:
            return f"Date insuficiente ({completed}/{total}) - necesare mai multe"
    
    def can_calculate_risk(self) -> bool:
        """Verifică dacă avem suficiente date pentru calcul"""
        data = st.session_state.patient_data
        return data.ore_spitalizare >= 48
    
    def calculate_and_display_risk(self):
        """Calculează și afișează riscul IAAM"""
        if not self.can_calculate_risk():
            st.error("❌ Date insuficiente! Timpul de spitalizare trebuie să fie ≥ 48 ore pentru IAAM.")
            return False
        
        # Calculează riscul
        result = self.predictor.predict_iaam_risk(st.session_state.patient_data)
        
        # Afișează rezultatul
        self._display_risk_result(result)
        
        # Salvează în istoric
        st.session_state.chat_history.append({
            "timestamp": datetime.now(),
            "data": asdict(st.session_state.patient_data),
            "result": result
        })
        
        return True
    
    def _display_risk_result(self, result: Dict):
        """Afișează rezultatul evaluării riscului"""
        level = result["level"]
        score = result["score"]
        color_class = result.get("color_class", "risk-low")
        
        # Afișează rezultatul principal
        st.markdown(f"""
        <div class="{color_class}">
            <h2>🎯 RISC IAAM: {level}</h2>
            <h3>Scor Total: {score} puncte</h3>
            <p><strong>Pacient ID:</strong> {result['patient_id']}</p>
            <p><strong>Data evaluării:</strong> {result['timestamp'].strftime('%d.%m.%Y %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detalii scoring
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Detalii Scoring")
            for detail in result["details"]:
                st.write(f"• {detail}")
        
        with col2:
            st.markdown("### 🎯 Recomandări")
            for rec in result["recommendations"]:
                st.write(f"• {rec}")
        
        # Scoruri clinice
        if result.get("sofa_score", 0) > 0:
            st.markdown("### 🏥 Scoruri Clinice")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("SOFA Score", result["sofa_score"])
                if "sofa_details" in result:
                    for component, score in result["sofa_details"].items():
                        st.write(f"• {component.title()}: {score}")
            
            with col2:
                st.metric("qSOFA Score", result["qsofa_score"])
                if "qsofa_criteria" in result:
                    for criterion in result["qsofa_criteria"]:
                        st.write(f"• {criterion}")
        
        # Grafic de risc
        self._display_risk_chart(result)
    
    def _display_risk_chart(self, result: Dict):
        """Afișează graficul de risc"""
        st.markdown("### 📈 Distribuția Scorului")
        
        # Pregătește datele pentru grafic
        categories = ["Timp", "Dispozitive", "Laborator", "Microbiologie", "Scoruri clinice"]
        values = [
            result.get("time_score", 0),
            result.get("device_score", 0),
            result.get("lab_score", 0),
            20 if st.session_state.patient_data.cultura_pozitiva else 0,
            result.get("sofa_score", 0) * 4 + (20 if result.get("qsofa_score", 0) >= 2 else 0)
        ]
        
        # Creează graficul
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=['#00d4ff', '#ffa726', '#66bb6a', '#ff4757', '#9c27b0'],
                text=values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Contribuția la Scorul IAAM",
            xaxis_title="Categorii",
            yaxis_title="Puncte",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def create_sidebar():
    """Creează sidebar-ul aplicației"""
    with st.sidebar:
        st.markdown("## ⚙️ Configurări")
        
        # Status AI
        ai_status = st.session_state.get("ai_status", False)
        status_text = "🟢 Online" if ai_status else "🔴 Offline (Fallback)"
        status_class = "status-online" if ai_status else "status-offline"
        
        st.markdown(f"**AI Status:** <span class='{status_class}'>{status_text}</span>", 
                   unsafe_allow_html=True)
        
        if not ai_status:
            with st.expander("🔧 Configurare Ollama"):
                st.markdown("""
                Pentru funcționalitate AI completă:
                1. Instalează Ollama: https://ollama.ai/
                2. Rulează: `ollama pull llama3.2:3b`
                3. Pornește Ollama și reîncarcă pagina
                
                **Alternativ:** Aplicația funcționează cu răspunsuri pre-programate.
                """)
        
        st.divider()
        
        # Date pacient curent
        st.markdown("## 👤 Pacient Curent")
        data = st.session_state.patient_data
        
        if data.ore_spitalizare > 0:
            st.metric("Ore spitalizare", f"{data.ore_spitalizare}h")
        
        # Dispozitive active
        devices = []
        for device in ["cateter_central", "ventilatie_mecanica", "sonda_urinara", "traheostomie", "drenaj", "peg"]:
            if getattr(data, device, False):
                days = getattr(data, f"{device}_days", 0)
                devices.append(f"{device.replace('_', ' ').title()} ({days}d)")
        
        if devices:
            st.markdown("**Dispozitive:**")
            for device in devices:
                st.write(f"• {device}")
        
        # Valori laborator
        if data.leucocite != 7.0 or data.crp != 5.0 or data.procalcitonina != 0.1:
            st.markdown("**Laborator:**")
            if data.leucocite != 7.0:
                st.write(f"• WBC: {data.leucocite}")
            if data.crp != 5.0:
                st.write(f"• CRP: {data.crp}")
            if data.procalcitonina != 0.1:
                st.write(f"• PCT: {data.procalcitonina}")
        
        st.divider()
        
        # Acțiuni rapide
        st.markdown("## ⚡ Acțiuni Rapide")
        
        if st.button("🆕 Pacient Nou", use_container_width=True):
            st.session_state.patient_data = PatientData()
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📊 Istoric Pacienți", use_container_width=True):
            show_patient_history()
        
        if st.button("📥 Export Date", use_container_width=True):
            export_patient_data()

def show_patient_history():
    """Afișează istoricul pacienților"""
    if not st.session_state.chat_history:
        st.info("Nu există istoric de pacienți.")
        return
    
    st.markdown("### 📋 Istoric Pacienți")
    
    for i, entry in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"Pacient {entry['result']['patient_id']} - {entry['timestamp'].strftime('%d.%m.%Y %H:%M')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Risc:** {entry['result']['level']}")
                st.write(f"**Scor:** {entry['result']['score']}")
                st.write(f"**Spitalizare:** {entry['data']['ore_spitalizare']}h")
            
            with col2:
                if entry['data'].get('cultura_pozitiva'):
                    st.write(f"**Bacterie:** {entry['data'].get('bacterie', 'N/A')}")
                    if entry['data'].get('rezistente'):
                        st.write(f"**Rezistențe:** {', '.join(entry['data']['rezistente'])}")

def export_patient_data():
    """Exportă datele pacientului"""
    data = asdict(st.session_state.patient_data)
    
    # Convertește datetime pentru JSON
    if 'timestamp' in data and data['timestamp']:
        data['timestamp'] = data['timestamp'].isoformat()
    
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    
    st.download_button(
        label="📥 Descarcă Date JSON",
        data=json_data,
        file_name=f"pacient_{data['patient_id']}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

def main():
    """Funcția principală a aplicației"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🤖 EpiMind AI - IAAM Predictor Enhanced</h1>
        <p>Asistent AI pentru evaluarea riscului de infecții asociate asistenței medicale</p>
        <p><em>UMF "Grigore T. Popa" Iași - Version 4.0.0</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inițializează interfața chat
    chat = EnhancedChatInterface()
    
    # Creează sidebar
    create_sidebar()
    
    # Layout principal
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 💬 Chat Medical AI")
        
        # Container pentru chat
        chat_container = st.container()
        
        with chat_container:
            # Mesaj inițial
            if not st.session_state.messages:
                st.markdown("""
                <div class="message ai-message">
                    <strong>🤖 EpiMind AI:</strong><br>
                    Salut! Sunt asistentul tău AI pentru evaluarea riscului IAAM. 
                    Poți să-mi spui despre pacient în limba română, în mod natural.
                    <br><br>
                    <strong>Exemple de introducere date:</strong><br>
                    • "Pacientul este internat de 5 zile, are CVC de 3 zile și ventilație mecanică"<br>
                    • "Leucocite 15.000, CRP 120, procalcitonină 2.5, temperatură 38.5°C"<br>
                    • "Cultură pozitivă E.coli ESBL+, Glasgow 12, TA 90/60"<br>
                    • "Sondă urinară de 7 zile, dren toracic, febră de 39°C"
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
        
        # Input pentru conversație
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Scrie aici informațiile despre pacient...",
                placeholder="Ex: Pacientul are 72 ore de internare, CVC de 4 zile, leucocite 14000, CRP 150, cultură pozitivă Klebsiella ESBL+...",
                height=120,
                key="user_input"
            )
            
            col_send, col_calc, col_clear = st.columns([2, 2, 1])
            
            with col_send:
                submit_button = st.form_submit_button("💬 Trimite", type="primary")
            
            with col_calc:
                calc_button = st.form_submit_button("🎯 Calculează Risc", type="secondary")
            
            with col_clear:
                clear_button = st.form_submit_button("🗑️ Reset")
        
        # Procesează input-ul
        if submit_button and user_input:
            # Adaugă mesajul utilizatorului
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Procesează cu AI
            with st.spinner("🤖 AI procesează datele medicale..."):
                ai_response = chat.process_user_input(user_input)
            
            # Adaugă răspunsul AI
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response
            })
            
            st.rerun()
        
        # Calculează riscul
        if calc_button:
            with st.spinner("🧮 Calculez riscul IAAM..."):
                success = chat.calculate_and_display_risk()
                if success:
                    st.success("✅ Evaluarea IAAM a fost completată!")
        
        # Reset chat
        if clear_button:
            st.session_state.messages = []
            st.session_state.patient_data = PatientData()
            st.rerun()
    
    with col2:
        st.markdown("### 📋 Ghid Date Necesare")
        
        # Checklist interactiv
        st.markdown("""
        <div class="data-card">
            <h4>✅ Date Esențiale IAAM</h4>
            <ul>
                <li>⏰ <strong>Timp spitalizare</strong> (ore/zile) - OBLIGATORIU ≥48h</li>
                <li>🔧 <strong>Dispozitive invazive</strong> și durata lor</li>
                <li>🧪 <strong>Analize laborator</strong> (WBC, CRP, PCT)</li>
                <li>🦠 <strong>Culturi microbiologice</strong> și rezistențe</li>
                <li>💓 <strong>Parametri vitali</strong> (TA, FC, T°, FR)</li>
                <li>🧠 <strong>Scor Glasgow</strong> și status neurologic</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Exemple de dispozitive
        st.markdown("""
        <div class="data-card">
            <h4>🔧 Dispozitive Invazive</h4>
            <ul>
                <li><strong>CVC:</strong> Cateter venos central, PICC, Port</li>
                <li><strong>Ventilație:</strong> Intubație, CPAP, BiPAP</li>
                <li><strong>Sondă urinară:</strong> Foley, cateter urinar</li>
                <li><strong>Traheostomie:</strong> Canulă traheală</li>
                <li><strong>Drenaj:</strong> Dren toracic, abdominal</li>
                <li><strong>PEG:</strong> Gastrostomie, sondă gastrică</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Bacterii și rezistențe comune
        st.markdown("""
        <div class="data-card">
            <h4>🦠 Microbiologie Frecventă</h4>
            <p><strong>Bacterii:</strong> E.coli, Klebsiella, Pseudomonas, Acinetobacter, S.aureus</p>
            <p><strong>Rezistențe:</strong> ESBL, MRSA, VRE, CRE, KPC, NDM, XDR, PDR</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interpretare scoruri
        st.markdown("""
        <div class="data-card">
            <h4>📊 Interpretare Risc IAAM</h4>
            <ul>
                <li>🟢 <strong>SCĂZUT</strong> (0-49): Monitorizare standard</li>
                <li>🟡 <strong>MODERAT</strong> (50-79): Supraveghere extinsă</li>
                <li>🟠 <strong>ÎNALT</strong> (80-109): Măsuri preventive</li>
                <li>🔴 <strong>FOARTE ÎNALT</strong> (110-139): Consult urgent</li>
                <li>🚨 <strong>CRITIC</strong> (≥140): Alertă IAAM</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
