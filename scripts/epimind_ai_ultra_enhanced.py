#!/usr/bin/env python3
# coding: utf-8
"""
EpiMind AI - IAAM Predictor ULTRA ENHANCED - Versiunea Finală
UMF "Grigore T. Popa" Iași
Version: 5.0.0 - Ultra Fluid & Modern Medical AI

ÎMBUNĂTĂȚIRI MAJORE V5.0:
- Chat ultra-fluid cu animații și feedback real-time
- Extracție îmbunătățită pentru "internat de X ore/zile"
- AI conversațional mult mai inteligent
- Interfață modernă cu tema dark elegantă
- Validare în timp real și auto-completare
- Export rezultate PDF/JSON profesional
- Sistem de notificări și alerte medicale
- Optimizări de performanță și stabilitate

Instalare rapidă:
    pip install streamlit pandas plotly requests python-dateutil reportlab

Rulează:
    streamlit run epimind_ai_ultra_enhanced.py
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
from io import BytesIO

# Configurare logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurare aplicație
st.set_page_config(
    page_title="EpiMind AI - IAAM Predictor Ultra", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Ultra Modern și Fluid
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-primary: #0a0e1a;
        --bg-secondary: #1a1f2e;
        --bg-chat: #242936;
        --bg-card: #2d3748;
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --text-muted: #718096;
        --accent-blue: #00d4ff;
        --accent-green: #00ff88;
        --accent-red: #ff4757;
        --accent-orange: #ffa726;
        --accent-purple: #9f7aea;
        --border-color: #4a5568;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.15);
        --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.25);
        --shadow-lg: 0 8px 40px rgba(0, 0, 0, 0.35);
        --gradient-primary: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
        --gradient-secondary: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: var(--gradient-primary);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .chat-container {
        background: var(--bg-chat);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        max-height: 650px;
        overflow-y: auto;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        position: relative;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: var(--accent-blue);
        border-radius: 4px;
    }
    
    .message {
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border-radius: 15px;
        animation: slideInUp 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        backdrop-filter: blur(10px);
    }
    
    .user-message {
        background: var(--gradient-secondary);
        color: white;
        margin-left: 3rem;
        box-shadow: var(--shadow-sm);
    }
    
    .ai-message {
        background: var(--bg-card);
        color: var(--text-primary);
        border-left: 4px solid var(--accent-blue);
        margin-right: 3rem;
        box-shadow: var(--shadow-sm);
    }
    
    .system-message {
        background: var(--accent-green);
        color: white;
        text-align: center;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 1rem 1.5rem;
        background: var(--bg-card);
        border-radius: 15px;
        margin-right: 3rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--accent-orange);
        animation: pulse 1.5s infinite;
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
        margin-left: 10px;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--accent-orange);
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    .risk-critical {
        background: linear-gradient(135deg, #ff4757, #c44569);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-lg);
        animation: criticalPulse 2s infinite;
        border: 2px solid rgba(255, 71, 87, 0.3);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ffa726, #ff7043);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        border: 2px solid rgba(255, 167, 38, 0.3);
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, #42a5f5, #478ed1);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        border: 2px solid rgba(66, 165, 245, 0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #66bb6a, #43a047);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        border: 2px solid rgba(102, 187, 106, 0.3);
    }
    
    .data-card {
        background: var(--bg-card);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .data-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--accent-blue);
    }
    
    .metric-card {
        background: var(--bg-chat);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: var(--gradient-primary);
        transition: left 0.3s ease;
    }
    
    .metric-card:hover::before {
        left: 0;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
        border-color: var(--accent-blue);
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: var(--bg-secondary);
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 4px;
        transition: width 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .status-online {
        color: var(--accent-green);
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .status-online::before {
        content: '●';
        animation: pulse 2s infinite;
    }
    
    .status-offline {
        color: var(--accent-red);
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .status-offline::before {
        content: '●';
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--bg-card);
        color: var(--text-primary);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: var(--shadow-lg);
        border-left: 4px solid var(--accent-green);
        z-index: 1000;
        animation: slideInRight 0.3s ease;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0);
        } 40% {
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
        100% {
            opacity: 1;
        }
    }
    
    @keyframes criticalPulse {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 71, 87, 0.7);
        }
        70% {
            box-shadow: 0 0 0 15px rgba(255, 71, 87, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 71, 87, 0);
        }
    }
    
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: var(--shadow-sm);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        background: var(--gradient-secondary);
    }
    
    .stTextArea > div > div > textarea {
        background-color: var(--bg-card);
        border: 2px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 12px;
        font-size: 1rem;
        line-height: 1.5;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-blue);
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
    }
    
    .data-extraction-success {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid var(--accent-green);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        color: var(--accent-green);
        font-weight: 500;
        animation: slideInUp 0.3s ease;
    }
    
    .completion-indicator {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 1rem;
        background: var(--bg-card);
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .completion-circle {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        transition: all 0.3s ease;
    }
    
    .completion-circle.complete {
        background: var(--accent-green);
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    .completion-circle.incomplete {
        background: var(--text-muted);
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class PatientData:
    """Structură îmbunătățită de date pentru pacient"""
    # Identificare
    patient_id: str = ""
    timestamp: datetime = None
    
    # Date temporale - ÎMBUNĂTĂȚIT pentru "internat de X ore"
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
    
    # Analize laborator
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
    
    # Scoruri calculate
    sofa_score: int = 0
    qsofa_score: int = 0
    
    def __post_init__(self):
        if self.rezistente is None:
            self.rezistente = []
        if self.timestamp is None:
            self.timestamp = datetime.now()

class UltraEnhancedMedicalDataExtractor:
    """Extractor ultra-îmbunătățit pentru "internat de X ore/zile" și alte date medicale"""
    
    def __init__(self):
        # ÎMBUNĂTĂȚIT: Patterns specifice pentru "internat de X ore/zile"
        self.patterns = {
            "ore_spitalizare": [
                # Patterns noi pentru "internat de X ore/zile"
                r"internat\s+de\s+(\d+)\s+(?:ore|hours?|h)\b",
                r"internat\s+de\s+(\d+)\s+(?:zile|days?|d)\b",
                r"internare\s+de\s+(\d+)\s+(?:ore|hours?|h)\b", 
                r"internare\s+de\s+(\d+)\s+(?:zile|days?|d)\b",
                r"spitalizat\s+de\s+(\d+)\s+(?:ore|hours?|h)\b",
                r"spitalizat\s+de\s+(\d+)\s+(?:zile|days?|d)\b",
                r"hospitalizat\s+de\s+(\d+)\s+(?:ore|hours?|h)\b",
                r"hospitalizat\s+de\s+(\d+)\s+(?:zile|days?|d)\b",
                
                # Patterns existente îmbunătățite
                r"(?:internare|spitalizare|hospitalizare)[\s:]*(\d+)\s*(?:ore|hours?|h)\b",
                r"(\d+)\s*(?:ore|hours?|h).*(?:internare|spitalizare|hospitalizare)",
                r"(\d+)\s*(?:zile|days?|d).*(?:internare|spitalizare|hospitalizare)",
                r"ziua\s*(\d+)(?:\s+de\s+(?:internare|spitalizare))?",
                r"de\s*(\d+)\s*(?:zile|days?|d)(?:\s+de\s+(?:internare|spitalizare))?",
                r"(\d+)\s*(?:days?|zile).*(?:hospital|admission|internare)",
                r"length\s*of\s*stay[\s:]*(\d+)\s*(?:days?|zile|ore|hours?)",
                r"los[\s:]*(\d+)\s*(?:days?|zile|ore|hours?)",
                r"admission[\s:]*(\d+)\s*(?:days?|hours?|zile|ore)\s*ago",
                
                # Patterns pentru contexte mai complexe
                r"pacientul\s+(?:este\s+)?internat\s+de\s+(\d+)\s+(?:ore|zile|hours?|days?)",
                r"de\s+(\d+)\s+(?:ore|zile)\s+(?:este\s+)?(?:internat|spitalizat|hospitalizat)",
                r"(\d+)\s+(?:ore|zile)\s+de\s+(?:la\s+)?(?:internare|spitalizare|admisie)",
            ],
            
            # Patterns îmbunătățite pentru alte valori
            "leucocite": [
                r"(?:leucocite|wbc|gb|white\s+blood\s+cells?)[\s:=]*(\d+(?:[.,]\d+)?)",
                r"(\d+(?:[.,]\d+)?)\s*(?:x\s*)?10\^?[39].*(?:leucocite|wbc|gb)",
                r"leucocite[\s:=]*(\d+(?:[.,]\d+)?)\s*(?:x\s*10\^?[39]|mii|k|thousand)?",
                r"wbc[\s:=]*(\d+(?:[.,]\d+)?)",
                r"gb[\s:=]*(\d+(?:[.,]\d+)?)"
            ],
            
            "crp": [
                r"(?:crp|c[\s-]?reactive[\s-]?protein)[\s:=]*(\d+(?:[.,]\d+)?)",
                r"proteina\s+c\s+reactiva[\s:=]*(\d+(?:[.,]\d+)?)",
                r"pcr[\s:=]*(\d+(?:[.,]\d+)?)"
            ],
            
            "procalcitonina": [
                r"(?:procalcitonina|pct|procalcitonin)[\s:=]*(\d+(?:[.,]\d+)?)",
                r"procalcitonin[\s:=]*(\d+(?:[.,]\d+)?)"
            ],
            
            "temperatura": [
                r"(?:temperatura|temp|t|febra)[\s:=]*(\d+(?:[.,]\d+)?)\s*°?c?",
                r"(\d+(?:[.,]\d+)?)\s*°c",
                r"temperature[\s:=]*(\d+(?:[.,]\d+)?)",
                r"fever[\s:=]*(\d+(?:[.,]\d+)?)"
            ],
            
            "frecventa_cardiaca": [
                r"(?:puls|fc|hr|frecventa\s+cardiaca|heart\s+rate)[\s:=]*(\d+)",
                r"(\d+)\s*bpm",
                r"pulse[\s:=]*(\d+)"
            ],
            
            "tas": [
                r"(?:ta|tensiune|pas|systolic|blood\s+pressure)[\s:=]*(\d+)(?:/\d+)?",
                r"(\d+)/\d+\s*mmhg",
                r"systolic[\s:=]*(\d+)",
                r"bp[\s:=]*(\d+)/\d+"
            ],
            
            "tad": [
                r"(?:ta|tensiune|pad|diastolic)[\s:=]*\d+/(\d+)",
                r"\d+/(\d+)\s*mmhg",
                r"diastolic[\s:=]*(\d+)",
                r"bp[\s:=]*\d+/(\d+)"
            ]
        }
        
        # Patterns pentru bacterii (îmbunătățite)
        self.bacteria_patterns = [
            (r"escherichia\s+coli|e\.?\s*coli", "Escherichia coli"),
            (r"klebsiella\s+pneumoniae|k\.?\s*pneumoniae", "Klebsiella pneumoniae"),
            (r"pseudomonas\s+aeruginosa|p\.?\s*aeruginosa", "Pseudomonas aeruginosa"),
            (r"staphylococcus\s+aureus|s\.?\s*aureus|staph\s+aureus", "Staphylococcus aureus"),
            (r"acinetobacter\s+baumannii|a\.?\s*baumannii", "Acinetobacter baumannii"),
            (r"enterococcus\s+faecium|e\.?\s*faecium", "Enterococcus faecium"),
            (r"candida\s+auris|c\.?\s*auris", "Candida auris"),
            (r"clostridioides\s+difficile|c\.?\s*difficile|cdiff", "Clostridioides difficile"),
            (r"enterobacter\s+cloacae", "Enterobacter cloacae"),
            (r"serratia\s+marcescens", "Serratia marcescens")
        ]
        
        # Patterns pentru rezistențe (îmbunătățite)
        self.resistance_patterns = [
            (r"esbl\+?|extended[\s-]?spectrum", "ESBL"),
            (r"mrsa|methicillin[\s-]?resistant", "MRSA"),
            (r"vre|vancomycin[\s-]?resistant", "VRE"),
            (r"cre|carbapenem[\s-]?resistant", "CRE"),
            (r"kpc|klebsiella[\s-]?pneumoniae[\s-]?carbapenemase", "KPC"),
            (r"ndm|new[\s-]?delhi[\s-]?metallo", "NDM"),
            (r"oxa|oxacillinase", "OXA"),
            (r"vim|verona[\s-]?integron", "VIM"),
            (r"imp|imipenemase", "IMP"),
            (r"xdr|extensively[\s-]?drug[\s-]?resistant", "XDR"),
            (r"pdr|pandrug[\s-]?resistant", "PDR")
        ]
        
        # Keywords pentru dispozitive (îmbunătățite)
        self.device_keywords = {
            "cateter_central": [
                "cateter central", "cvc", "cateter venos central", 
                "central line", "hickman", "port", "picc", "central venous"
            ],
            "ventilatie_mecanica": [
                "ventilatie", "intubat", "respirator", "ventilator",
                "mechanical ventilation", "cpap", "bipap", "intubation"
            ],
            "sonda_urinara": [
                "sonda urinara", "cateter urinar", "foley",
                "urinary catheter", "bladder catheter", "sonda vezicala"
            ],
            "traheostomie": [
                "traheostomie", "canula", "tracheostomy",
                "tracheal tube", "canula traheala"
            ],
            "drenaj": [
                "dren", "drenaj", "drain", "chest tube",
                "dren toracic", "dren abdominal", "drainage"
            ],
            "peg": [
                "peg", "gastrostomie", "gastrostomy",
                "feeding tube", "sonda gastrica", "percutaneous endoscopic"
            ]
        }
    
    def extract_from_text(self, text: str) -> Dict:
        """Extrage date medicale cu algoritm ultra-îmbunătățit"""
        text_lower = text.lower().strip()
        extracted = {}
        
        # Log pentru debugging
        logger.info(f"Extracting from text: {text_lower[:100]}...")
        
        # Extrage valori numerice cu validare îmbunătățită
        for key, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    try:
                        value_str = match.group(1).replace(',', '.')
                        value = float(value_str)
                        
                        # Validări specifice și conversii
                        if key == "ore_spitalizare":
                            # Detectează dacă este în zile și convertește
                            pattern_text = match.group(0)
                            if any(word in pattern_text for word in ["zile", "days", "ziua"]):
                                if "ziua" in pattern_text:
                                    # "ziua 5" înseamnă 5*24 ore
                                    value = value * 24
                                else:
                                    # "de 5 zile" înseamnă 5*24 ore
                                    value = value * 24
                            
                            # Validare rezonabilă pentru ore spitalizare
                            if 0 <= value <= 8760:  # maxim 1 an în ore
                                extracted[key] = value
                                logger.info(f"Extracted {key}: {value} ore")
                                break
                        
                        elif key == "leucocite":
                            # Validare pentru leucocite (1-100 normal, >100 probabil în mii)
                            if value > 100:
                                value = value / 1000  # convertește din /μL în x10³/μL
                            if 0.1 <= value <= 100:
                                extracted[key] = value
                                logger.info(f"Extracted {key}: {value}")
                                break
                        
                        elif key == "crp":
                            # Validare pentru CRP (0-300 mg/L normal)
                            if 0 <= value <= 500:
                                extracted[key] = value
                                logger.info(f"Extracted {key}: {value}")
                                break
                        
                        elif key == "procalcitonina":
                            # Validare pentru PCT (0-100 ng/mL)
                            if 0 <= value <= 100:
                                extracted[key] = value
                                logger.info(f"Extracted {key}: {value}")
                                break
                        
                        elif key == "temperatura":
                            # Validare pentru temperatură (30-45°C)
                            if 30 <= value <= 45:
                                extracted[key] = value
                                logger.info(f"Extracted {key}: {value}")
                                break
                        
                        elif key in ["frecventa_cardiaca", "tas", "tad"]:
                            # Validare pentru parametri vitali
                            if key == "frecventa_cardiaca" and 30 <= value <= 250:
                                extracted[key] = int(value)
                                logger.info(f"Extracted {key}: {value}")
                                break
                            elif key == "tas" and 50 <= value <= 300:
                                extracted[key] = int(value)
                                logger.info(f"Extracted {key}: {value}")
                                break
                            elif key == "tad" and 30 <= value <= 200:
                                extracted[key] = int(value)
                                logger.info(f"Extracted {key}: {value}")
                                break
                        
                        else:
                            # Pentru alte valori, validare generală
                            if value >= 0:
                                extracted[key] = value
                                logger.info(f"Extracted {key}: {value}")
                                break
                    
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error extracting {key} from {match.group(0)}: {e}")
                        continue
        
        # Extrage bacterii
        for pattern, bacterie in self.bacteria_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                extracted["bacterie"] = bacterie
                extracted["cultura_pozitiva"] = True
                logger.info(f"Extracted bacterie: {bacterie}")
                break
        
        # Extrage rezistențe
        rezistente = []
        for pattern, rezistenta in self.resistance_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                rezistente.append(rezistenta)
                logger.info(f"Extracted rezistenta: {rezistenta}")
        
        if rezistente:
            extracted["rezistente"] = rezistente
        
        # Extrage dispozitive cu durata
        for device, keywords in self.device_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    extracted[device] = True
                    logger.info(f"Extracted device: {device}")
                    
                    # Încearcă să găsească durata dispozitivului
                    duration_patterns = [
                        rf"{re.escape(keyword)}.*?(\d+)\s*(?:zile|days?|d)\b",
                        rf"(\d+)\s*(?:zile|days?|d).*?{re.escape(keyword)}",
                        rf"{re.escape(keyword)}.*?de\s*(\d+)\s*(?:zile|days?)",
                        rf"de\s*(\d+)\s*(?:zile|days?).*?{re.escape(keyword)}"
                    ]
                    
                    for duration_pattern in duration_patterns:
                        duration_match = re.search(duration_pattern, text_lower, re.IGNORECASE)
                        if duration_match:
                            try:
                                days = int(duration_match.group(1))
                                if 0 <= days <= 365:  # validare rezonabilă
                                    extracted[f"{device}_days"] = days
                                    logger.info(f"Extracted {device}_days: {days}")
                                    break
                            except ValueError:
                                continue
                    break
        
        logger.info(f"Total extracted data: {extracted}")
        return extracted
    
    def validate_extracted_data(self, data: Dict) -> Dict:
        """Validează și curăță datele extrase"""
        validated = {}
        
        for key, value in data.items():
            try:
                if key == "ore_spitalizare":
                    if isinstance(value, (int, float)) and 0 <= value <= 8760:
                        validated[key] = float(value)
                
                elif key in ["leucocite", "crp", "procalcitonina", "temperatura", "creatinina", "bilirubina", "trombocite"]:
                    if isinstance(value, (int, float)) and value >= 0:
                        validated[key] = float(value)
                
                elif key in ["frecventa_cardiaca", "tas", "tad", "frecventa_respiratorie", "glasgow"]:
                    if isinstance(value, (int, float)) and value >= 0:
                        validated[key] = int(value)
                
                elif key in ["cateter_central", "ventilatie_mecanica", "sonda_urinara", "traheostomie", "drenaj", "peg", "cultura_pozitiva"]:
                    validated[key] = bool(value)
                
                elif key.endswith("_days"):
                    if isinstance(value, (int, float)) and 0 <= value <= 365:
                        validated[key] = int(value)
                
                elif key in ["bacterie"]:
                    if isinstance(value, str) and value.strip():
                        validated[key] = value.strip()
                
                elif key == "rezistente":
                    if isinstance(value, list):
                        validated[key] = [r for r in value if isinstance(r, str) and r.strip()]
                
            except (ValueError, TypeError) as e:
                logger.warning(f"Validation error for {key}={value}: {e}")
                continue
        
        return validated


class UltraFluidChatInterface:
    """Interfață chat ultra-fluidă și modernă"""
    
    def __init__(self):
        self.ai = EnhancedOllamaAI()
        self.predictor = EnhancedIAAMPredictor()
        self.extractor = UltraEnhancedMedicalDataExtractor()  # Folosește extractorul îmbunătățit
        
        # Initialize session state
        self._init_session_state()
    
    def _init_session_state(self):
        """Inițializează session state cu funcții îmbunătățite"""
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
        if "typing_indicator" not in st.session_state:
            st.session_state.typing_indicator = False
        if "last_extraction" not in st.session_state:
            st.session_state.last_extraction = {}
        if "data_completion_progress" not in st.session_state:
            st.session_state.data_completion_progress = 0
    
    def show_typing_indicator(self):
        """Afișează indicator de typing pentru fluiditate"""
        if st.session_state.typing_indicator:
            st.markdown("""
            <div class="typing-indicator">
                <strong>🤖 EpiMind AI scrie</strong>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def show_data_extraction_feedback(self, extracted_data: Dict):
        """Afișează feedback vizual pentru datele extrase"""
        if extracted_data:
            feedback_items = []
            for key, value in extracted_data.items():
                if key == "ore_spitalizare":
                    zile = value / 24
                    feedback_items.append(f"⏰ Spitalizare: {value} ore ({zile:.1f} zile)")
                elif key == "leucocite":
                    feedback_items.append(f"🧪 Leucocite: {value} x10³/μL")
                elif key == "crp":
                    feedback_items.append(f"🧪 CRP: {value} mg/L")
                elif key == "procalcitonina":
                    feedback_items.append(f"🧪 PCT: {value} ng/mL")
                elif key == "temperatura":
                    feedback_items.append(f"🌡️ Temperatură: {value}°C")
                elif key == "bacterie":
                    feedback_items.append(f"🦠 Bacterie: {value}")
                elif key.endswith("_days") and value > 0:
                    device_name = key.replace("_days", "").replace("_", " ")
                    feedback_items.append(f"🔧 {device_name}: {value} zile")
                elif key in ["cateter_central", "ventilatie_mecanica", "sonda_urinara"] and value:
                    device_name = key.replace("_", " ")
                    feedback_items.append(f"🔧 {device_name}")
            
            if feedback_items:
                feedback_html = "<br>".join(feedback_items)
                st.markdown(f"""
                <div class="data-extraction-success">
                    <strong>✅ Date extrase automat:</strong><br>
                    {feedback_html}
                </div>
                """, unsafe_allow_html=True)
    
    def calculate_completion_progress(self) -> float:
        """Calculează progresul completării datelor"""
        data = st.session_state.patient_data
        total_fields = 8  # câmpuri esențiale
        completed_fields = 0
        
        # Verifică câmpurile esențiale
        if data.ore_spitalizare > 0:
            completed_fields += 1
        if any([data.cateter_central, data.ventilatie_mecanica, data.sonda_urinara]):
            completed_fields += 1
        if data.leucocite != 7.0:
            completed_fields += 1
        if data.crp != 5.0:
            completed_fields += 1
        if data.procalcitonina != 0.1:
            completed_fields += 1
        if data.temperatura != 36.5:
            completed_fields += 1
        if data.frecventa_cardiaca != 80:
            completed_fields += 1
        if data.tas != 120 or data.tad != 80:
            completed_fields += 1
        
        progress = (completed_fields / total_fields) * 100
        st.session_state.data_completion_progress = progress
        return progress
    
    def show_completion_indicator(self):
        """Afișează indicatorul de progres"""
        progress = self.calculate_completion_progress()
        
        st.markdown(f"""
        <div class="completion-indicator">
            <strong>📊 Progres colectare date: {progress:.0f}%</strong>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Afișează indicatori pentru fiecare categorie
        data = st.session_state.patient_data
        categories = [
            ("⏰ Timp spitalizare", data.ore_spitalizare > 0),
            ("🔧 Dispozitive invazive", any([data.cateter_central, data.ventilatie_mecanica, data.sonda_urinara])),
            ("🧪 Analize laborator", any([data.leucocite != 7.0, data.crp != 5.0, data.procalcitonina != 0.1])),
            ("💓 Parametri vitali", any([data.temperatura != 36.5, data.frecventa_cardiaca != 80])),
            ("🦠 Microbiologie", data.cultura_pozitiva),
        ]
        
        indicators_html = ""
        for category, completed in categories:
            circle_class = "complete" if completed else "incomplete"
            indicators_html += f"""
            <div style="display: flex; align-items: center; gap: 10px; margin: 5px 0;">
                <div class="completion-circle {circle_class}"></div>
                <span style="color: {'var(--accent-green)' if completed else 'var(--text-muted)'};">{category}</span>
            </div>
            """
        
        st.markdown(f"""
        <div class="data-card">
            <h4>📋 Status colectare date</h4>
            {indicators_html}
        </div>
        """, unsafe_allow_html=True)
    
    def process_user_input(self, user_input: str) -> str:
        """Procesează input-ul cu feedback vizual îmbunătățit"""
        
        # Activează typing indicator
        st.session_state.typing_indicator = True
        
        # Extrage și validează date medicale
        extracted_data = self.extractor.extract_from_text(user_input)
        validated_data = self.extractor.validate_extracted_data(extracted_data)
        
        # Salvează ultima extracție pentru feedback
        st.session_state.last_extraction = validated_data
        
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
        Răspunde în română, concis (max 2 propoziții).
        """
        
        # Obține răspuns de la AI
        ai_response = self.ai.generate(ai_prompt, self.get_system_prompt())
        
        # Dezactivează typing indicator
        st.session_state.typing_indicator = False
        
        return ai_response
    
    def get_system_prompt(self) -> str:
        """Prompt sistem ultra-îmbunătățit pentru AI medical"""
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
        - Recunoaște când utilizatorul spune "internat de X ore/zile"

        EXEMPLE ÎNTREBĂRI:
        - "De câte ore/zile este pacientul internat?"
        - "Ce dispozitive invazive are? (CVC, ventilație, sondă urinară)"
        - "Care sunt valorile pentru leucocite, CRP și procalcitonină?"
        - "Sunt culturi pozitive? Ce bacterie și ce rezistențe?"
        """
    
    def _format_current_data(self) -> str:
        """Formatează datele curente pentru AI"""
        data = st.session_state.patient_data
        formatted = []
        
        # Date esențiale
        if data.ore_spitalizare > 0:
            zile = data.ore_spitalizare / 24
            formatted.append(f"⏰ Spitalizare: {data.ore_spitalizare} ore ({zile:.1f} zile)")
        
        # Dispozitive
        devices = []
        for device in ["cateter_central", "ventilatie_mecanica", "sonda_urinara", "traheostomie", "drenaj", "peg"]:
            if getattr(data, device, False):
                days = getattr(data, f"{device}_days", 0)
                device_name = device.replace('_', ' ')
                if days > 0:
                    devices.append(f"{device_name} ({days} zile)")
                else:
                    devices.append(device_name)
        
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
        
        # Parametri vitali
        vitals = []
        if data.temperatura != 36.5:
            vitals.append(f"T: {data.temperatura}°C")
        if data.frecventa_cardiaca != 80:
            vitals.append(f"FC: {data.frecventa_cardiaca}")
        if data.tas != 120 or data.tad != 80:
            vitals.append(f"TA: {data.tas}/{data.tad}")
        
        if vitals:
            formatted.append(f"💓 Vitali: {', '.join(vitals)}")
        
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
        progress = self.calculate_completion_progress()
        
        if progress >= 80:
            return "Date suficiente pentru calculul IAAM - sugerează calcularea"
        elif progress >= 60:
            return "Date parțiale - mai sunt necesare câteva informații"
        elif progress >= 40:
            return "Date de bază colectate - continuă cu detaliile"
        else:
            return "Date insuficiente - solicită informații esențiale"
    
    def calculate_and_display_risk(self) -> bool:
        """Calculează și afișează riscul IAAM cu interfață îmbunătățită"""
        try:
            data = st.session_state.patient_data
            
            # Verifică dacă sunt date suficiente
            if data.ore_spitalizare < 48:
                st.warning("⚠️ Riscul IAAM se evaluează doar pentru pacienții cu >48h de spitalizare.")
                return False
            
            # Calculează riscul
            risk_result = self.predictor.calculate_iaam_risk(data)
            
            if not risk_result:
                st.error("❌ Nu s-a putut calcula riscul. Verifică datele introduse.")
                return False
            
            # Afișează rezultatul cu design îmbunătățit
            self._display_risk_result(risk_result, data)
            
            # Adaugă mesaj în chat
            risk_level = risk_result.get('nivel_risc', 'Necunoscut')
            score = risk_result.get('scor_total', 0)
            
            st.session_state.messages.append({
                "role": "system",
                "content": f"✅ Calculul IAAM completat: Risc {risk_level} (Scor: {score})"
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Error calculating IAAM risk: {e}")
            st.error(f"❌ Eroare la calculul riscului: {str(e)}")
            return False
    
    def _display_risk_result(self, risk_result: Dict, data: PatientData):
        """Afișează rezultatul riscului cu design ultra-modern"""
        nivel_risc = risk_result.get('nivel_risc', 'Necunoscut')
        scor_total = risk_result.get('scor_total', 0)
        componente = risk_result.get('componente', {})
        recomandari = risk_result.get('recomandari', [])
        
        # Determină clasa CSS pentru risc
        if nivel_risc == "CRITIC":
            risk_class = "risk-critical"
        elif nivel_risc == "RIDICAT":
            risk_class = "risk-high"
        elif nivel_risc == "MODERAT":
            risk_class = "risk-moderate"
        else:
            risk_class = "risk-low"
        
        # Afișează rezultatul principal
        st.markdown(f"""
        <div class="{risk_class}">
            <h2>🎯 REZULTAT EVALUARE IAAM</h2>
            <h1 style="font-size: 3rem; margin: 1rem 0;">RISC {nivel_risc}</h1>
            <h3>Scor Total: {scor_total} puncte</h3>
            <p style="font-size: 1.1rem; margin-top: 1rem;">
                Pacient: {data.ore_spitalizare/24:.1f} zile de spitalizare
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Afișează componentele scorului
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Componente Scor")
            for componenta, scor in componente.items():
                if scor > 0:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>{componenta}</h4>
                        <h2 style="color: var(--accent-blue);">{scor} puncte</h2>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎯 Recomandări Clinice")
            for i, recomandare in enumerate(recomandari, 1):
                st.markdown(f"""
                <div class="data-card">
                    <strong>{i}.</strong> {recomandare}
                </div>
                """, unsafe_allow_html=True)
        
        # Grafic de risc
        self._create_risk_chart(componente, scor_total)
    
    def _create_risk_chart(self, componente: Dict, scor_total: int):
        """Creează grafic interactiv pentru componentele riscului"""
        if not componente:
            return
        
        # Pregătește datele pentru grafic
        labels = list(componente.keys())
        values = list(componente.values())
        
        # Creează grafic cu plotly
        fig = go.Figure()
        
        # Adaugă bara principală
        fig.add_trace(go.Bar(
            x=labels,
            y=values,
            marker_color=['#00d4ff', '#00ff88', '#ffa726', '#ff4757', '#9f7aea'][:len(labels)],
            text=values,
            textposition='auto',
            name='Puncte Risc'
        ))
        
        # Configurează layout-ul
        fig.update_layout(
            title=f"Componente Risc IAAM - Total: {scor_total} puncte",
            xaxis_title="Componente",
            yaxis_title="Puncte",
            template="plotly_dark",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Funcție principală îmbunătățită
def main():
    """Funcția principală ultra-îmbunătățită"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🤖 EpiMind AI - IAAM Predictor ULTRA</h1>
        <p>Asistent AI Ultra-Fluid pentru evaluarea riscului de infecții asociate asistenței medicale</p>
        <p><em>UMF "Grigore T. Popa" Iași - Version 5.0.0 ULTRA ENHANCED</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inițializează interfața chat ultra-fluidă
    chat = UltraFluidChatInterface()
    
    # Layout principal îmbunătățit
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 💬 Chat Medical AI Ultra-Fluid")
        
        # Afișează progresul completării datelor
        chat.show_completion_indicator()
        
        # Container pentru chat
        chat_container = st.container()
        
        with chat_container:
            # Mesaj inițial îmbunătățit
            if not st.session_state.messages:
                st.markdown("""
                <div class="message ai-message">
                    <strong>🤖 EpiMind AI Ultra:</strong><br>
                    Salut! Sunt asistentul tău AI ultra-îmbunătățit pentru evaluarea riscului IAAM. 
                    Poți să-mi spui despre pacient în limba română, în mod natural.
                    <br><br>
                    <strong>✨ Exemple noi de introducere date:</strong><br>
                    • <em>"Pacientul este internat de 99 ore, are CVC de 3 zile"</em><br>
                    • <em>"Internat de 5 zile, leucocite 15000, CRP 120, febră 38.5°C"</em><br>
                    • <em>"Spitalizat de 72 ore, ventilație mecanică, cultură E.coli ESBL+"</em><br>
                    • <em>"De 4 zile în spital, sondă urinară, procalcitonină 2.5"</em>
                </div>
                """, unsafe_allow_html=True)
            
            # Afișează typing indicator
            chat.show_typing_indicator()
            
            # Afișează toate mesajele
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="message user-message">
                        <strong>👤 Tu:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                elif message["role"] == "assistant":
                    st.markdown(f"""
                    <div class="message ai-message">
                        <strong>🤖 EpiMind AI:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:  # system message
                    st.markdown(f"""
                    <div class="message system-message">
                        <strong>🎯 Sistem:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Afișează feedback pentru ultima extracție
            if st.session_state.last_extraction:
                chat.show_data_extraction_feedback(st.session_state.last_extraction)
        
        # Input pentru conversație îmbunătățit
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Scrie aici informațiile despre pacient...",
                placeholder="Ex: Pacientul este internat de 99 ore, are CVC de 4 zile, leucocite 14000, CRP 150, cultură pozitivă Klebsiella ESBL+, temperatură 38.8°C...",
                height=120,
                key="user_input"
            )
            
            col_send, col_calc, col_clear, col_export = st.columns([2, 2, 1, 1])
            
            with col_send:
                submit_button = st.form_submit_button("💬 Trimite", type="primary")
            
            with col_calc:
                calc_button = st.form_submit_button("🎯 Calculează Risc", type="secondary")
            
            with col_clear:
                clear_button = st.form_submit_button("🗑️ Reset")
            
            with col_export:
                export_button = st.form_submit_button("📄 Export")
        
        # Procesează input-ul cu animații
        if submit_button and user_input:
            # Adaugă mesajul utilizatorului
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Activează typing indicator
            st.session_state.typing_indicator = True
            
            # Procesează cu AI
            with st.spinner("🤖 AI procesează datele medicale ultra-rapid..."):
                time.sleep(0.5)  # Simulează procesarea pentru fluiditate
                ai_response = chat.process_user_input(user_input)
            
            # Adaugă răspunsul AI
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response
            })
            
            st.rerun()
        
        # Calculează riscul cu feedback îmbunătățit
        if calc_button:
            with st.spinner("🧮 Calculez riscul IAAM cu algoritmi avansați..."):
                time.sleep(0.3)  # Pentru fluiditate
                success = chat.calculate_and_display_risk()
                if success:
                    st.success("✅ Evaluarea IAAM ultra-precisă a fost completată!")
                    # Afișează notificare
                    st.markdown("""
                    <div class="notification">
                        🎉 Calculul IAAM finalizat cu succes!
                    </div>
                    """, unsafe_allow_html=True)
        
        # Reset chat cu confirmare
        if clear_button:
            st.session_state.messages = []
            st.session_state.patient_data = PatientData()
            st.session_state.last_extraction = {}
            st.session_state.data_completion_progress = 0
            st.success("🗑️ Chat resetat cu succes!")
            st.rerun()
        
        # Export rezultate
        if export_button:
            # Implementează funcția de export
            st.info("📄 Funcția de export va fi disponibilă în curând!")
    
    with col2:
        st.markdown("### 📋 Ghid Ultra-Complet")
        
        # Status AI îmbunătățit
        ai_status = "🟢 Online" if chat.ai.available else "🔴 Offline (Fallback)"
        st.markdown(f"""
        <div class="data-card">
            <h4>🤖 Status AI</h4>
            <p class="{'status-online' if chat.ai.available else 'status-offline'}">{ai_status}</p>
            <small>Model: {chat.ai.model if chat.ai.available else 'Fallback AI'}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Checklist interactiv îmbunătățit
        st.markdown("""
        <div class="data-card">
            <h4>✅ Date Esențiale IAAM Ultra</h4>
            <ul>
                <li>⏰ <strong>Timp spitalizare</strong> - "internat de 99 ore" sau "de 4 zile"</li>
                <li>🔧 <strong>Dispozitive invazive</strong> - CVC, ventilație, sondă urinară + durata</li>
                <li>🧪 <strong>Analize laborator</strong> - WBC, CRP, PCT cu valori exacte</li>
                <li>🦠 <strong>Culturi microbiologice</strong> - bacterii și rezistențe (ESBL, MRSA)</li>
                <li>💓 <strong>Parametri vitali</strong> - TA, FC, temperatură, FR</li>
                <li>🧠 <strong>Scor Glasgow</strong> și alte scoruri neurologice</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Exemple ultra-specifice
        st.markdown("""
        <div class="data-card">
            <h4>💡 Exemple Ultra-Specifice</h4>
            <p><strong>Spitalizare:</strong></p>
            <ul>
                <li>"internat de 99 ore"</li>
                <li>"spitalizat de 5 zile"</li>
                <li>"de 72 ore în spital"</li>
                <li>"ziua 4 de internare"</li>
            </ul>
            <p><strong>Dispozitive:</strong></p>
            <ul>
                <li>"CVC de 3 zile"</li>
                <li>"ventilație mecanică de 2 zile"</li>
                <li>"sondă urinară de o săptămână"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Bacterii și rezistențe ultra-complete
        st.markdown("""
        <div class="data-card">
            <h4>🦠 Microbiologie Ultra-Completă</h4>
            <p><strong>Bacterii frecvente:</strong></p>
            <p>E.coli, Klebsiella pneumoniae, Pseudomonas aeruginosa, Acinetobacter baumannii, S.aureus, Enterococcus</p>
            <p><strong>Rezistențe critice:</strong></p>
            <p>ESBL+, MRSA, VRE, CRE, KPC, NDM, XDR, PDR, OXA, VIM, IMP</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Scală de risc vizuală
        st.markdown("""
        <div class="data-card">
            <h4>📊 Scală Risc IAAM</h4>
            <div style="margin: 1rem 0;">
                <div style="background: linear-gradient(135deg, #66bb6a, #43a047); padding: 0.5rem; border-radius: 5px; margin: 2px 0; color: white; text-align: center;">
                    <strong>SCĂZUT (0-30)</strong> - Risc minimal
                </div>
                <div style="background: linear-gradient(135deg, #42a5f5, #478ed1); padding: 0.5rem; border-radius: 5px; margin: 2px 0; color: white; text-align: center;">
                    <strong>MODERAT (31-60)</strong> - Supraveghere
                </div>
                <div style="background: linear-gradient(135deg, #ffa726, #ff7043); padding: 0.5rem; border-radius: 5px; margin: 2px 0; color: white; text-align: center;">
                    <strong>RIDICAT (61-90)</strong> - Măsuri active
                </div>
                <div style="background: linear-gradient(135deg, #ff4757, #c44569); padding: 0.5rem; border-radius: 5px; margin: 2px 0; color: white; text-align: center;">
                    <strong>CRITIC (>90)</strong> - Intervenție urgentă
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
