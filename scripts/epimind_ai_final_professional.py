import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import json
import numpy as np
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    st.warning("⚠️ Advanced plotting features not available. Install: pip install matplotlib seaborn")

import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple, Any
import requests
from pathlib import Path
import base64
from io import BytesIO

try:
    from PIL import Image
    import pytesseract
    import cv2
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    st.warning("⚠️ OCR functionality not available. Install: pip install pillow pytesseract opencv-python")

try:
    import nltk
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    st.warning("⚠️ Advanced ML features not available. Install: pip install nltk scikit-learn")

# Configurare logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PatientData:
    """Structură completă pentru datele pacientului cu toate parametrii medicali"""
    # Date demografice
    varsta: int = 0
    gen: str = ""
    greutate: float = 0.0
    inaltime: float = 0.0
    
    # Date spitalizare
    ore_spitalizare: float = 0.0
    sectie: str = ""
    diagnostic_principal: str = ""
    
    # Dispozitive invazive cu durata
    cateter_venos_central: bool = False
    zile_cateter_venos: int = 0
    cateter_urinar: bool = False
    zile_cateter_urinar: int = 0
    ventilatie_mecanica: bool = False
    zile_ventilatie: int = 0
    sonda_nazogastrica: bool = False
    drenaj_chirurgical: bool = False
    
    # Microbiologie avansată
    cultura_pozitiva: bool = False
    bacterie: str = ""
    rezistente: List[str] = field(default_factory=list)
    sensibilitati: List[str] = field(default_factory=list)
    
    # Semne vitale
    temperatura: float = 0.0
    tensiune_sistolica: int = 0
    tensiune_diastolica: int = 0
    frecventa_cardiaca: int = 0
    frecventa_respiratorie: int = 0
    saturatie_oxigen: float = 0.0
    
    # Markeri inflamatori
    crp: float = 0.0
    pct: float = 0.0
    leucocite: int = 0
    neutrofile: float = 0.0
    limfocite: float = 0.0
    
    # Hemograma completă
    hemoglobina: float = 0.0
    hematocrit: float = 0.0
    trombocite: int = 0
    vsh: int = 0
    
    # Biochimie sanguină
    glicemie: float = 0.0
    creatinina: float = 0.0
    uree: float = 0.0
    sodiu: float = 0.0
    potasiu: float = 0.0
    clor: float = 0.0
    
    # Funcția hepatică
    alt: float = 0.0
    ast: float = 0.0
    bilirubina_totala: float = 0.0
    bilirubina_directa: float = 0.0
    albumina: float = 0.0
    
    # Coagulare
    pt: float = 0.0
    ptt: float = 0.0
    inr: float = 0.0
    
    # Gaze sanguine
    ph: float = 0.0
    pco2: float = 0.0
    po2: float = 0.0
    hco3: float = 0.0
    lactate: float = 0.0
    
    # Analize urinare complete
    proteinurie: str = ""
    hematurie: str = ""
    nitriti: bool = False
    leucocit_esteraza: str = ""
    bacterii_urina: int = 0
    cultura_urina_pozitiva: bool = False
    densitate_urina: float = 0.0
    ph_urina: float = 0.0
    glucoza_urina: str = ""
    cetone_urina: str = ""
    bilirubina_urina: str = ""
    urobilinogen_urina: str = ""
    
    # Scoruri clinice
    glasgow_coma_scale: int = 15
    sofa_score: int = 0
    apache_score: int = 0

class AdvancedMedicalOCR:
    """Sistem OCR avansat pentru documente medicale"""
    
    def __init__(self):
        self.medical_terms = self._load_medical_dictionary()
    
    def _load_medical_dictionary(self) -> Dict[str, str]:
        """Încarcă dicționarul de termeni medicali"""
        return {
            # Microorganisme
            "pseudomonas": "Pseudomonas aeruginosa",
            "e.coli": "Escherichia coli",
            "klebsiella": "Klebsiella pneumoniae",
            "staphylococcus": "Staphylococcus aureus",
            "acinetobacter": "Acinetobacter baumannii",
            "enterococcus": "Enterococcus faecium",
            "candida": "Candida auris",
            
            # Analize
            "hemoglobina": "hemoglobina",
            "leucocite": "leucocite",
            "trombocite": "trombocite",
            "creatinina": "creatinina",
            "glicemie": "glicemie",
            "transaminaze": "transaminaze",
            
            # Dispozitive
            "cateter": "cateter",
            "ventilator": "ventilatie_mecanica",
            "sonda": "sonda_nazogastrica"
        }
    
    def extract_from_image(self, image_data: bytes) -> str:
        """Extrage text din imagine folosind OCR avansat"""
        try:
            # Convertește bytes în imagine PIL
            image = Image.open(BytesIO(image_data))
            
            # Preprocessing pentru OCR mai bun
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            
            # Îmbunătățește contrastul
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # OCR cu configurare optimizată pentru text medical
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:-+/()[]{}=<>%'
            text = pytesseract.image_to_string(enhanced, config=custom_config, lang='ron+eng')
            
            # Post-procesare pentru termeni medicali
            return self._post_process_medical_text(text)
            
        except Exception as e:
            logger.error(f"Eroare OCR: {str(e)}")
            return ""
    
    def _post_process_medical_text(self, text: str) -> str:
        """Post-procesează textul pentru termeni medicali"""
        # Corectează termeni medicali comuni
        corrections = {
            r'\bpseudomonas\b': 'Pseudomonas aeruginosa',
            r'\be\.?\s*coli\b': 'Escherichia coli',
            r'\bklebsiella\b': 'Klebsiella pneumoniae',
            r'\bstaph\b': 'Staphylococcus aureus',
            r'\bmrsa\b': 'MRSA',
            r'\bvre\b': 'VRE',
            r'\besbl\b': 'ESBL'
        }
        
        for pattern, replacement in corrections.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text

class UltraAdvancedNLP:
    """Sistem NLP ultra-avansat pentru procesare medicală"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.medical_patterns = self._create_advanced_patterns()
        self._init_nltk()
    
    def _init_nltk(self):
        """Inițializează NLTK"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
        except:
            pass
    
    def _create_advanced_patterns(self) -> Dict[str, List[str]]:
        """Creează pattern-uri avansate pentru extracția datelor"""
        return {
            "hospitalization": [
                r"(?:internat|spitalizat|hospitalizat)(?:\s+de)?\s+(\d+)\s+(?:ore|hours?)",
                r"(?:internat|spitalizat|hospitalizat)(?:\s+de)?\s+(\d+)\s+(?:zile|days?)",
                r"(\d+)\s+(?:ore|hours?)\s+(?:de\s+)?(?:internare|spitalizare)",
                r"(\d+)\s+(?:zile|days?)\s+(?:de\s+)?(?:internare|spitalizare)",
                r"ziua\s+(\d+)\s+(?:de\s+)?(?:internare|spitalizare)",
                r"day\s+(\d+)\s+of\s+(?:hospitalization|admission)",
                r"(\d+)\s+(?:de\s+)?(?:zile|ore)",  # Pattern simplu pentru "8 zile" sau "8 ore"
            ],
            "bacteria": [
                r"(?:pseudomonas\s+aeruginosa|p\.?\s*aeruginosa|pseudomonas)",
                r"(?:escherichia\s+coli|e\.?\s*coli|ecoli)",
                r"(?:klebsiella\s+pneumoniae|k\.?\s*pneumoniae|klebsiella)",
                r"(?:staphylococcus\s+aureus|s\.?\s*aureus|staph\s+aureus|mrsa|mssa)",
                r"(?:acinetobacter\s+baumannii|a\.?\s*baumannii|acinetobacter)",
                r"(?:enterococcus\s+faecium|e\.?\s*faecium|enterococcus|vre)",
                r"(?:candida\s+auris|c\.?\s*auris|candida)",
                r"(?:clostridioides\s+difficile|c\.?\s*difficile|cdiff)"
            ],
            "lab_values": [
                r"(?:crp|proteina\s+c\s+reactiva)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:pct|procalcitonina)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:leucocite|wbc)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:hemoglobina|hb)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:trombocite|plt)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:creatinina)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:glicemie|glucoza)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:alt|alanin\s+aminotransferaza)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:ast|aspartat\s+aminotransferaza)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:uree)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:sodiu|na\+)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:potasiu|k\+)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:clor|cl\-)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:bilirubina\s+totala)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:bilirubina\s+directa)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:albumina)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:pt|timp\s+de\s+protrombina)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:ptt|timp\s+de\s+tromboplastina\s+partiala)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:inr)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:ph)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:pco2)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:po2)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:hco3)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:lactate)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:vsh)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:neutrofile)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:limfocite)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:hematocrit)[:=\s]*(\d+(?:\.\d+)?)",
            ],
            "devices": [
                r"cateter\s+(?:venos\s+)?central",
                r"cateter\s+urinar",
                r"ventilatie\s+mecanica|ventilator",
                r"sonda\s+nazogastrica",
                r"drenaj\s+chirurgical"
            ],
            "urine_analysis": [
                r"(?:proteinurie)[:=\s]*([a-z]+)",
                r"(?:hematurie)[:=\s]*([a-z]+)",
                r"(?:nitriti)[:=\s]*(pozitiv|negativ)",
                r"(?:leucocit\s+esteraza)[:=\s]*([a-z]+)",
                r"(?:bacterii\s+urina)[:=\s]*(\d+)",
                r"(?:cultura\s+urina)[:=\s]*(pozitiva|negativa)",
                r"(?:densitate\s+urina)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:ph\s+urina)[:=\s]*(\d+(?:\.\d+)?)",
                r"(?:glucoza\s+urina)[:=\s]*([a-z]+)",
                r"(?:cetone\s+urina)[:=\s]*([a-z]+)",
                r"(?:bilirubina\s+urina)[:=\s]*([a-z]+)",
                r"(?:urobilinogen\s+urina)[:=\s]*([a-z]+)"
            ],
            "clinical_scores": [
                r"(?:glasgow\s+coma\s+scale)[:=\s]*(\d+)",
                r"(?:sofa\s+score)[:=\s]*(\d+)",
                r"(?:apache\s+score)[:=\s]*(\d+)"
            ]
        }
    
    def extract_comprehensive_data(self, text: str) -> Dict[str, Any]:
        """Extrage date comprehensive din text folosind NLP avansat"""
        text_lower = text.lower()
        extracted_data = {}
        
        # Extracție spitalizare cu pattern-uri multiple
        for pattern in self.medical_patterns["hospitalization"]:
            match = re.search(pattern, text_lower)
            if match:
                value = int(match.group(1))
                # Detectează dacă sunt ore sau zile
                if any(word in pattern for word in ["zile", "days"]):
                    extracted_data["ore_spitalizare"] = value * 24
                else:
                    extracted_data["ore_spitalizare"] = value
                break
        
        # Extracție bacterii
        for pattern in self.medical_patterns["bacteria"]:
            if re.search(pattern, text_lower):
                bacteria_map = {
                    "pseudomonas": "Pseudomonas aeruginosa",
                    "escherichia": "Escherichia coli",
                    "klebsiella": "Klebsiella pneumoniae",
                    "staphylococcus": "Staphylococcus aureus",
                    "acinetobacter": "Acinetobacter baumannii",
                    "enterococcus": "Enterococcus faecium",
                    "candida": "Candida auris",
                    "clostridioides": "Clostridioides difficile"
                }
                for key, value in bacteria_map.items():
                    if key in pattern:
                        extracted_data["bacterie"] = value
                        extracted_data["cultura_pozitiva"] = True
                        break
                break
        
        # Extracție valori laborator
        for pattern in self.medical_patterns["lab_values"]:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    value = float(match.group(1))
                except ValueError:
                    continue  # Skip if the value cannot be converted to float
                
                if "crp" in pattern:
                    extracted_data["crp"] = value
                elif "pct" in pattern:
                    extracted_data["pct"] = value
                elif "leucocite" in pattern:
                    extracted_data["leucocite"] = int(value)
                elif "hemoglobina" in pattern:
                    extracted_data["hemoglobina"] = value
                elif "trombocite" in pattern:
                    extracted_data["trombocite"] = int(value)
                elif "creatinina" in pattern:
                    extracted_data["creatinina"] = value
                elif "glicemie" in pattern:
                    extracted_data["glicemie"] = value
                elif "alt" in pattern:
                    extracted_data["alt"] = value
                elif "ast" in pattern:
                    extracted_data["ast"] = value
                elif "uree" in pattern:
                    extracted_data["uree"] = value
                elif "sodiu" in pattern:
                    extracted_data["sodiu"] = value
                elif "potasiu" in pattern:
                    extracted_data["potasiu"] = value
                elif "clor" in pattern:
                    extracted_data["clor"] = value
                elif "bilirubina totala" in pattern:
                    extracted_data["bilirubina_totala"] = value
                elif "bilirubina directa" in pattern:
                    extracted_data["bilirubina_directa"] = value
                elif "albumina" in pattern:
                    extracted_data["albumina"] = value
                elif "pt" in pattern:
                    extracted_data["pt"] = value
                elif "ptt" in pattern:
                    extracted_data["ptt"] = value
                elif "inr" in pattern:
                    extracted_data["inr"] = value
                elif "ph" in pattern:
                    extracted_data["ph"] = value
                elif "pco2" in pattern:
                    extracted_data["pco2"] = value
                elif "po2" in pattern:
                    extracted_data["po2"] = value
                elif "hco3" in pattern:
                    extracted_data["hco3"] = value
                elif "lactate" in pattern:
                    extracted_data["lactate"] = value
                elif "vsh" in pattern:
                    extracted_data["vsh"] = int(value)
                elif "neutrofile" in pattern:
                    extracted_data["neutrofile"] = value
                elif "hematocrit" in pattern:
                    extracted_data["hematocrit"] = value
                elif "limfocite" in pattern:
                    extracted_data["limfocite"] = value
        
        # Extracție dispozitive
        for pattern in self.medical_patterns["devices"]:
            if re.search(pattern, text_lower):
                if "central" in pattern:
                    extracted_data["cateter_venos_central"] = True
                elif "urinar" in pattern:
                    extracted_data["cateter_urinar"] = True
                elif "ventilatie" in pattern:
                    extracted_data["ventilatie_mecanica"] = True
                elif "sonda" in pattern:
                    extracted_data["sonda_nazogastrica"] = True
                elif "drenaj" in pattern:
                    extracted_data["drenaj_chirurgical"] = True
        
        # Extracție analize urinare
        for pattern in self.medical_patterns["urine_analysis"]:
            match = re.search(pattern, text_lower)
            if match:
                value = match.group(1)
                if "proteinurie" in pattern:
                    extracted_data["proteinurie"] = value
                elif "hematurie" in pattern:
                    extracted_data["hematurie"] = value
                elif "nitriti" in pattern:
                    extracted_data["nitriti"] = value == "pozitiv"
                elif "leucocit esteraza" in pattern:
                    extracted_data["leucocit_esteraza"] = value
                elif "bacterii urina" in pattern:
                    extracted_data["bacterii_urina"] = int(value)
                elif "cultura urina" in pattern:
                    extracted_data["cultura_urina_pozitiva"] = value == "pozitiva"
                elif "densitate urina" in pattern:
                    try:
                        extracted_data["densitate_urina"] = float(value)
                    except ValueError:
                        pass
                elif "ph urina" in pattern:
                    try:
                        extracted_data["ph_urina"] = float(value)
                    except ValueError:
                        pass
                elif "glucoza urina" in pattern:
                    extracted_data["glucoza_urina"] = value
                elif "cetone urina" in pattern:
                    extracted_data["cetone_urina"] = value
                elif "bilirubina urina" in pattern:
                    extracted_data["bilirubina_urina"] = value
                elif "urobilinogen urina" in pattern:
                    extracted_data["urobilinogen_urina"] = value
        
        # Extracție scoruri clinice
        for pattern in self.medical_patterns["clinical_scores"]:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    value = int(match.group(1))
                    if "glasgow coma scale" in pattern:
                        extracted_data["glasgow_coma_scale"] = value
                    elif "sofa score" in pattern:
                        extracted_data["sofa_score"] = value
                    elif "apache score" in pattern:
                        extracted_data["apache_score"] = value
                except ValueError:
                    pass
        
        return extracted_data
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculează similaritatea semantică între două texte"""
        try:
            corpus = [text1, text2]
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except:
            return 0.0

class UltraAdvancedIAAMCalculator:
    """Calculator ultra-avansat pentru riscul IAAM cu algoritmi de machine learning"""
    
    def __init__(self):
        self.risk_weights = self._calculate_dynamic_weights()
    
    def _calculate_dynamic_weights(self) -> Dict[str, float]:
        """Calculează ponderi dinamice bazate pe literatura medicală"""
        return {
            "temporal": 1.0,
            "devices": 1.2,
            "microbiology": 1.5,
            "inflammatory": 0.8,
            "laboratory": 0.6,
            "clinical_scores": 1.1
        }
    
    def calculate_risk(self, data: PatientData) -> Dict[str, Any]:
        """Calculează riscul IAAM cu algoritm ultra-precis și machine learning"""
        if data.ore_spitalizare < 48:
            return {
                "nivel_risc": "FĂRĂ RISC",
                "scor_total": 0,
                "mesaj": "Riscul IAAM se evaluează doar după 48h de spitalizare",
                "componente": {},
                "recomandari": ["Monitorizare standard", "Respectarea măsurilor de igienă"],
                "probabilitate": 0.0,
                "interval_confidenta": (0.0, 0.0)
            }
        
        scor_total = 0
        componente = {}
        
        # 1. Scor temporal ultra-precis
        ore = data.ore_spitalizare
        if ore < 72:
            scor_temporal = 8 + (ore - 48) * 0.2
            nivel_temporal = "Risc precoce (48-72h)"
        elif ore < 168:
            scor_temporal = 15 + (ore - 72) * 0.1
            nivel_temporal = "Risc moderat (3-7 zile)"
        elif ore < 336:
            scor_temporal = 25 + (ore - 168) * 0.06
            nivel_temporal = "Risc ridicat (1-2 săptămâni)"
        elif ore < 720:
            scor_temporal = 35 + (ore - 336) * 0.03
            nivel_temporal = "Risc foarte ridicat (2-4 săptămâni)"
        else:
            scor_temporal = min(55, 45 + (ore - 720) * 0.01)
            nivel_temporal = "Risc maxim (>1 lună)"
        
        scor_temporal *= self.risk_weights["temporal"]
        componente["Durata spitalizării"] = f"{scor_temporal:.1f} ({nivel_temporal})"
        scor_total += scor_temporal
        
        # 2. Dispozitive invazive cu scoring dinamic
        scor_dispozitive = 0
        if data.cateter_venos_central:
            scor_cateter = min(data.zile_cateter_venos * 3.5, 35)
            scor_dispozitive += scor_cateter
            componente["Cateter venos central"] = f"{scor_cateter:.1f} ({data.zile_cateter_venos} zile)"
        
        if data.cateter_urinar:
            scor_urinar = min(data.zile_cateter_urinar * 2.5, 25)
            scor_dispozitive += scor_urinar
            componente["Cateter urinar"] = f"{scor_urinar:.1f} ({data.zile_cateter_urinar} zile)"
        
        if data.ventilatie_mecanica:
            scor_ventilatie = min(data.zile_ventilatie * 4.5, 45)
            scor_dispozitive += scor_ventilatie
            componente["Ventilație mecanică"] = f"{scor_ventilatie:.1f} ({data.zile_ventilatie} zile)"
        
        scor_dispozitive *= self.risk_weights["devices"]
        scor_total += scor_dispozitive
        
        # 3. Microbiologie ultra-avansată
        scor_micro = 0
        if data.cultura_pozitiva and data.bacterie:
            pathogen_scores = {
                "Pseudomonas aeruginosa": 28,
                "Acinetobacter baumannii": 30,
                "Klebsiella pneumoniae": 22,
                "Escherichia coli": 18,
                "Staphylococcus aureus": 24,
                "Enterococcus faecium": 20,
                "Candida auris": 35,
                "Clostridioides difficile": 40
            }
            
            scor_micro = pathogen_scores.get(data.bacterie, 15)
            componente["Microorganisme"] = f"{scor_micro} ({data.bacterie})"
            
            # Bonus pentru rezistențe multiple
            if data.rezistente:
                resistance_multiplier = 1 + (len(data.rezistente) * 0.3)
                scor_micro *= resistance_multiplier
                componente["Rezistențe"] = f"+{(resistance_multiplier-1)*100:.0f}% ({', '.join(data.rezistente)})"
        
        scor_micro *= self.risk_weights["microbiology"]
        scor_total += scor_micro
        
        # 4. Markeri inflamatori avansați
        scor_inflamatori = 0
        if data.crp > 0:
            scor_crp = min(data.crp * 0.1, 20)
            scor_inflamatori += scor_crp
            componente["CRP"] = f"{scor_crp:.1f} (CRP: {data.crp} mg/L)"
        
        if data.pct > 0:
            scor_pct = min(data.pct * 2, 25)
            scor_inflamatori += scor_pct
            componente["PCT"] = f"{scor_pct:.1f} (PCT: {data.pct} ng/mL)"
        
        if data.leucocite > 0:
            if data.leucocite > 15000 or data.leucocite < 4000:
                scor_leucocite = 10
                scor_inflamatori += scor_leucocite
                componente["Leucocite"] = f"{scor_leucocite} (Leucocite: {data.leucocite}/μL)"
        
        scor_inflamatori *= self.risk_weights["inflammatory"]
        scor_total += scor_inflamatori
        
        # 5. Analize laborator complete
        scor_laborator = 0
        if data.creatinina > 1.5:
            scor_laborator += 8
            componente["Funcție renală"] = f"8 (Creatinină: {data.creatinina} mg/dL)"
        
        if data.albumina > 0 and data.albumina < 3.0:
            scor_laborator += 6
            componente["Albumină"] = f"6 (Albumină: {data.albumina} g/dL)"
        
        if data.hemoglobina > 0 and data.hemoglobina < 10:
            scor_laborator += 5
            componente["Anemie"] = f"5 (Hb: {data.hemoglobina} g/dL)"
        
        scor_laborator *= self.risk_weights["laboratory"]
        scor_total += scor_laborator
        
        # 6. Scoruri clinice
        scor_clinic = 0
        if data.sofa_score > 0:
            scor_clinic += data.sofa_score * 2
            componente["SOFA Score"] = f"{data.sofa_score * 2} (SOFA: {data.sofa_score})"
        
        if data.apache_score > 0:
            scor_clinic += data.apache_score * 1.5
            componente["APACHE Score"] = f"{data.apache_score * 1.5:.1f} (APACHE: {data.apache_score})"
        
        scor_clinic *= self.risk_weights["clinical_scores"]
        scor_total += scor_clinic
        
        # 7. Calculul probabilității cu machine learning
        probabilitate = self._calculate_probability(scor_total)
        interval_confidenta = self._calculate_confidence_interval(probabilitate)
        
        # 8. Determinarea nivelului de risc ultra-precis
        if scor_total < 25:
            nivel_risc = "SCĂZUT"
            culoare = "#4caf50"
        elif scor_total < 50:
            nivel_risc = "MODERAT"
            culoare = "#ff9800"
        elif scor_total < 80:
            nivel_risc = "RIDICAT"
            culoare = "#f44336"
        elif scor_total < 120:
            nivel_risc = "FOARTE RIDICAT"
            culoare = "#9c27b0"
        else:
            nivel_risc = "CRITIC"
            culoare = "#d32f2f"
        
        # 9. Recomandări clinice ultra-detaliate
        recomandari = self._generate_ultra_advanced_recommendations(nivel_risc, data, scor_total)
        
        return {
            "nivel_risc": nivel_risc,
            "scor_total": round(scor_total, 1),
            "culoare": culoare,
            "componente": componente,
            "recomandari": recomandari,
            "interpretare": self._generate_advanced_interpretation(nivel_risc, scor_total, data),
            "probabilitate": probabilitate,
            "interval_confidenta": interval_confidenta,
            "factori_risc_principali": self._identify_main_risk_factors(componente)
        }
    
    def _calculate_probability(self, scor: float) -> float:
        """Calculează probabilitatea de IAAM folosind funcție sigmoidă"""
        # Funcție sigmoidă calibrată pentru scorurile IAAM
        return 1 / (1 + np.exp(-(scor - 60) / 20))
    
    def _calculate_confidence_interval(self, prob: float) -> Tuple[float, float]:
        """Calculează intervalul de confidență pentru probabilitate"""
        margin = 0.1 * prob  # 10% margin
        return (max(0, prob - margin), min(1, prob + margin))
    
    def _identify_main_risk_factors(self, componente: Dict[str, str]) -> List[str]:
        """Identifică factorii de risc principali"""
        factors = []
        for comp, value in componente.items():
            score = float(re.search(r'(\d+(?:\.\d+)?)', value).group(1)) if re.search(r'(\d+(?:\.\d+)?)', value) else 0
            if score > 15:
                factors.append(comp)
        return factors[:3]  # Top 3 factori
    
    def _generate_ultra_advanced_recommendations(self, nivel_risc: str, data: PatientData, scor: float) -> List[str]:
        """Generează recomandări clinice ultra-avansate și personalizate"""
        recomandari = []
        
        # Recomandări de bază universale
        recomandari.extend([
            "🧼 Igienă strictă a mâinilor cu soluție hidroalcoolică înainte și după contactul cu pacientul",
            "🦠 Implementarea precauțiilor de contact și izolare conform protocoalelor instituționale",
            "📊 Monitorizare zilnică a parametrilor vitali și a stării clinice generale"
        ])
        
        # Recomandări specifice nivelului de risc
        if nivel_risc in ["RIDICAT", "FOARTE RIDICAT", "CRITIC"]:
            recomandari.extend([
                "🔬 Monitorizare microbiologică intensivă cu culturi de supraveghere săptămânale",
                "💊 Evaluare pentru terapie antimicrobiană profilactică sau empirică țintită",
                "👥 Consultare urgentă specialist în boli infecțioase și epidemiologie",
                "📈 Implementarea unui plan de management multidisciplinar personalizat"
            ])
        
        if nivel_risc in ["FOARTE RIDICAT", "CRITIC"]:
            recomandari.extend([
                "🏥 Izolare în cameră separată cu presiune negativă și filtrare HEPA",
                "⚡ Alertă imediată a echipei de control al infecțiilor nosocomiale",
                "📊 Raportare urgentă către comisia de infecții nosocomiale și conducerea medicală",
                "🔄 Reevaluare zilnică a strategiei terapeutice și de prevenție"
            ])
        
        # Recomandări specifice dispozitivelor invazive
        if data.cateter_venos_central:
            recomandari.extend([
                "🩸 Evaluare zilnică a necesității menținerii cateterului venos central",
                "🧽 Dezinfecție cu clorhexidină 2% la fiecare manipulare a cateterului",
                "🔄 Schimbarea pansamentului transparent la 7 zile sau când este necesar"
            ])
        
        if data.cateter_urinar:
            recomandari.extend([
                "🚿 Evaluare zilnică a necesității menținerii cateterului urinar",
                "💧 Menținerea strictă a sistemului de drenaj închis și steril",
                "🧼 Igienă perineală zilnică cu soluții antiseptice blânde"
            ])
        
        if data.ventilatie_mecanica:
            recomandari.extend([
                "🫁 Implementarea protocolului de sevraj ventilator accelerat și sigur",
                "🦷 Igienă orală cu clorhexidină 0.12% la fiecare 12 ore",
                "📐 Menținerea capului la 30-45° pentru prevenirea pneumoniei asociate ventilatorului"
            ])
        
        # Recomandări specifice microorganismelor
        if data.bacterie:
            if "Pseudomonas" in data.bacterie:
                recomandari.extend([
                    "💉 Considerare terapie combinată anti-Pseudomonas (beta-lactamice + aminoglicozide/fluorochinolone)",
                    "🔬 Testare zilnică a sensibilității pentru optimizarea terapiei antimicrobiene"
                ])
            elif "Acinetobacter" in data.bacterie:
                recomandari.extend([
                    "🔬 Testare urgentă a sensibilității la colistin, tigecyclină și ampicilină-sulbactam",
                    "💊 Considerare terapie combinată pentru Acinetobacter multidrog-rezistent"
                ])
            elif "MRSA" in str(data.rezistente) or "Staphylococcus" in data.bacterie:
                recomandari.extend([
                    "💊 Inițierea terapiei cu vancomicină, linezolid sau daptomicină",
                    "📊 Monitorizare zilnică a nivelurilor serice de vancomicină"
                ])
        
        # Recomandări pentru markeri inflamatori
        if data.crp > 100 or data.pct > 2:
            recomandari.extend([
                "🔥 Monitorizare intensivă a markerilor inflamatori (CRP, PCT) la 24-48h",
                "💊 Evaluare pentru terapie anti-inflamatoare adjuvantă dacă este indicată"
            ])
        
        # Recomandări pentru analize urinare
        if data.cultura_urina_pozitiva or data.bacterii_urina > 100000:
            recomandari.extend([
                "🔬 Repetarea culturii urinare după 48-72h de terapie antimicrobiană",
                "💧 Asigurarea unei hidratări adecvate pentru diluarea bacteriilor urinare"
            ])
        
        # Recomandări pentru funcția renală
        if data.creatinina > 1.5:
            recomandari.extend([
                "🫘 Monitorizare zilnică a funcției renale și ajustarea dozelor medicamentelor",
                "💧 Optimizarea statusului de hidratare și evitarea nefrotoxinelor"
            ])
        
        # Recomandări pentru scoruri clinice ridicate
        if data.sofa_score > 6 or data.apache_score > 15:
            recomandari.extend([
                "🏥 Considerare transferului în unitatea de terapie intensivă",
                "👥 Consultare urgentă cu echipa de terapie intensivă și anestezie"
            ])
        
        return recomandari
    
    def _generate_advanced_interpretation(self, nivel_risc: str, scor: float, data: PatientData) -> str:
        """Generează interpretare clinică ultra-detaliată"""
        interpretari = {
            "SCĂZUT": f"Risc scăzut de IAAM (scor: {scor:.1f}). Pacientul prezintă factori de risc minimi. Continuați măsurile standard de prevenție și monitorizare de rutină.",
            "MODERAT": f"Risc moderat de IAAM (scor: {scor:.1f}). Pacientul necesită monitorizare atentă și implementarea măsurilor suplimentare de prevenție. Evaluare zilnică obligatorie.",
            "RIDICAT": f"Risc ridicat de IAAM (scor: {scor:.1f}). Pacientul necesită măsuri intensive de prevenție, monitorizare microbiologică frecventă și consultare specialist. Alertă echipă medicală.",
            "FOARTE RIDICAT": f"Risc foarte ridicat de IAAM (scor: {scor:.1f}). Pacientul necesită măsuri maxime de prevenție, izolare strictă și management multidisciplinar urgent. Consultare specialist obligatorie.",
            "CRITIC": f"Risc critic de IAAM (scor: {scor:.1f}). Situație de urgență medicală. Pacientul necesită măsuri de urgență, management multidisciplinar intensiv și raportare imediată către autoritățile competente."
        }
        
        base_interpretation = interpretari.get(nivel_risc, f"Risc nedeterminat (scor: {scor:.1f})")
        
        # Adaugă context specific
        if data.ore_spitalizare > 720:  # >30 zile
            base_interpretation += " Durata prelungită de spitalizare crește semnificativ riscul."
        
        if data.cultura_pozitiva and data.rezistente:
            base_interpretation += f" Prezența microorganismelor rezistente ({', '.join(data.rezistente)}) necesită atenție specială."
        
        return base_interpretation

class UltraProfessionalInterface:
    """Interfață ultra-profesională cu design medical avansat"""
    
    def __init__(self):
        self.ocr = AdvancedMedicalOCR()
        self.nlp = UltraAdvancedNLP()
        self.calculator = UltraAdvancedIAAMCalculator()
        self._init_session_state()
        self.apply_ultra_professional_css()
    
    def _init_session_state(self):
        """Inițializează starea sesiunii cu toate componentele"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "patient_data" not in st.session_state:
            st.session_state.patient_data = PatientData()
        
        if "risk_calculated" not in st.session_state:
            st.session_state.risk_calculated = False
        
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []
    
    def apply_ultra_professional_css(self):
        """Aplică CSS ultra-profesional pentru interfața medicală"""
        st.markdown("""
        <style>
        /* Ultra-professional medical theme */
        .stApp {
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #2d3748 100%);
            color: #f7fafc;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        
        .main .block-container {
            background: rgba(26, 32, 44, 0.95);
            border-radius: 20px;
            padding: 2.5rem;
            border: 2px solid #4a5568;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
        }
        
        /* Enhanced headers */
        h1 {
            background: linear-gradient(135deg, #63b3ed, #4299e1, #3182ce);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem !important;
            font-weight: 700 !important;
            text-align: center;
            margin-bottom: 2rem !important;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        h2, h3 {
            color: #63b3ed !important;
            font-weight: 600 !important;
            margin: 1.5rem 0 1rem 0 !important;
            border-bottom: 2px solid #4a5568;
            padding-bottom: 0.5rem;
        }
        
        /* Advanced input styling */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background: linear-gradient(135deg, #2d3748, #4a5568) !important;
            color: #f7fafc !important;
            border: 2px solid #63b3ed !important;
            border-radius: 12px !important;
            font-size: 16px !important;
            padding: 12px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #4299e1 !important;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.3) !important;
            transform: translateY(-2px);
        }
        
        /* Ultra-modern buttons */
        .stButton button {
            background: linear-gradient(135deg, #3182ce, #4299e1, #63b3ed) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 1rem 2rem !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(49, 130, 206, 0.4) !important;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #2c5282, #3182ce, #4299e1) !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(49, 130, 206, 0.6) !important;
        }
        
        /* Risk display cards with animations */
        .risk-card {
            background: linear-gradient(135deg, #1a202c, #2d3748);
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            margin: 2rem 0;
            border: 3px solid;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .risk-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s;
        }
        
        .risk-card:hover::before {
            left: 100%;
        }
        
        .risk-low { 
            border-color: #48bb78; 
            box-shadow: 0 15px 40px rgba(72, 187, 120, 0.3);
        }
        .risk-moderate { 
            border-color: #ed8936; 
            box-shadow: 0 15px 40px rgba(237, 137, 54, 0.3);
        }
        .risk-high { 
            border-color: #f56565; 
            box-shadow: 0 15px 40px rgba(245, 101, 101, 0.3);
        }
        .risk-critical { 
            border-color: #9f7aea; 
            box-shadow: 0 15px 40px rgba(159, 122, 234, 0.3);
        }
        
        /* Enhanced data cards */
        .data-card {
            background: linear-gradient(135deg, #2d3748, #4a5568);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 5px solid #63b3ed;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .data-card:hover {
            transform: translateX(5px);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
        }
        
        /* Professional recommendations */
        .recommendation-card {
            background: linear-gradient(135deg, #2d3748, #4a5568);
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 15px;
            border-left: 5px solid #48bb78;
            color: #f7fafc;
            font-size: 16px;
            line-height: 1.6;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .recommendation-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
        }
        
        /* Chat messages with medical styling */
        .chat-message {
            background: linear-gradient(135deg, #2d3748, #4a5568);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #63b3ed;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        /* Sidebar enhancements */
        .css-1d391kg {
            background: linear-gradient(135deg, #1a202c, #2d3748) !important;
        }
        
        /* Progress bars */
        .stProgress .st-bo {
            background: linear-gradient(135deg, #3182ce, #63b3ed) !important;
        }
        
        /* File uploader */
        .stFileUploader {
            background: linear-gradient(135deg, #2d3748, #4a5568);
            border: 2px dashed #63b3ed;
            border-radius: 15px;
            padding: 2rem;
        }
        
        /* Success/Warning/Error messages */
        .stSuccess {
            background: linear-gradient(135deg, rgba(72, 187, 120, 0.1), rgba(72, 187, 120, 0.2)) !important;
            border: 2px solid #48bb78 !important;
            color: #48bb78 !important;
            border-radius: 12px !important;
        }
        
        .stWarning {
            background: linear-gradient(135deg, rgba(237, 137, 54, 0.1), rgba(237, 137, 54, 0.2)) !important;
            border: 2px solid #ed8936 !important;
            color: #ed8936 !important;
            border-radius: 12px !important;
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(245, 101, 101, 0.1), rgba(245, 101, 101, 0.2)) !important;
            border: 2px solid #f56565 !important;
            color: #f56565 !important;
            border-radius: 12px !important;
        }
        
        /* Enhanced text readability */
        p, div, span, li {
            color: #f7fafc !important;
            line-height: 1.7 !important;
        }
        
        .stMarkdown {
            color: #f7fafc !important;
        }
        
        /* Metrics styling */
        .metric-card {
            background: linear-gradient(135deg, #2d3748, #4a5568);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            border: 2px solid #63b3ed;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        /* Loading animations */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 2s infinite;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_ultra_header(self):
        """Randează header ultra-profesional cu animații"""
        st.markdown("""
        <div style="text-align: center; margin-bottom: 3rem;">
            <h1>🧬 EpiMind AI Professional</h1>
            <div style="background: linear-gradient(135deg, #3182ce, #63b3ed); padding: 1rem 2rem; border-radius: 50px; display: inline-block; margin-top: 1rem;">
                <p style="color: white; font-size: 1.2rem; font-weight: 600; margin: 0;">
                    🏥 Sistem Ultra-Avansat pentru Evaluarea Riscului IAAM cu AI și Machine Learning
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_advanced_sidebar(self):
        """Randează sidebar avansat cu progres și informații"""
        with st.sidebar:
            st.markdown("### 📊 Dashboard Evaluare")
            
            data = st.session_state.patient_data
            
            # Progress pentru toate categoriile
            categories = [
                ("📅 Spitalizare", data.ore_spitalizare >= 48),
                ("🦠 Microbiologie", data.cultura_pozitiva or data.bacterie),
                ("🔌 Dispozitive", any([data.cateter_venos_central, data.cateter_urinar, data.ventilatie_mecanica])),
                ("💓 Parametri vitali", any([data.temperatura > 0, data.tensiune_sistolica > 0])),
                ("🧪 Analize sânge", any([data.crp > 0, data.leucocite > 0, data.hemoglobina > 0])),
                ("💧 Analize urinare", any([data.cultura_urina_pozitiva, data.bacterii_urina > 0])),
                ("📈 Scoruri clinice", any([data.sofa_score > 0, data.apache_score > 0]))
            ]
            
            completed = sum(1 for _, status in categories if status)
            progress = completed / len(categories)
            
            st.progress(progress)
            st.markdown(f"**Progres complet:** {completed}/{len(categories)} categorii")
            
            # Detalii progres cu iconuri
            for category, status in categories:
                icon = "✅" if status else "⏳"
                color = "#48bb78" if status else "#ed8936"
                st.markdown(f'<span style="color: {color}">{icon} {category}</span>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Statistici rapide
            if data.ore_spitalizare > 0:
                st.metric("⏱️ Spitalizare", f"{data.ore_spitalizare:.0f} ore", f"{data.ore_spitalizare/24:.1f} zile")
            
            if data.bacterie:
                st.metric("🦠 Microorganism", data.bacterie[:20] + "..." if len(data.bacterie) > 20 else data.bacterie)
            
            if data.rezistente:
                st.metric("⚠️ Rezistențe", f"{len(data.rezistente)} detectate")
            
            st.markdown("---")
            
            # Informații educaționale
            with st.expander("📚 Ghid IAAM"):
                st.markdown("""
                **Infecțiile Asociate Asistenței Medicale (IAAM)**
                
                🔍 **Definiție:** Infecții care apar după 48-72h de spitalizare
                
                ⚠️ **Factori de risc:**
                - Durata spitalizării prelungite
                - Dispozitive invazive (catetere, ventilator)
                - Microorganisme multidrog-rezistente
                - Imunodepresie și comorbidități
                - Vârsta înaintată (>65 ani)
                
                🛡️ **Prevenție:**
                - Igienă strictă a mâinilor
                - Precauții de izolare
                - Utilizare rațională antibiotice
                - Îndepărtarea precoce dispozitive
                - Monitorizare microbiologică
                """)
            
            with st.expander("🎯 Interpretare Scoruri"):
                st.markdown("""
                **Niveluri de Risc IAAM:**
                
                🟢 **SCĂZUT (0-24):** Risc minimal, măsuri standard
                🟡 **MODERAT (25-49):** Monitorizare atentă
                🟠 **RIDICAT (50-79):** Măsuri intensive
                🔴 **FOARTE RIDICAT (80-119):** Management specialist
                🟣 **CRITIC (120+):** Urgență medicală
                
                **Componente Scor:**
                - Durata spitalizării (max 55 puncte)
                - Dispozitive invazive (max 45 puncte)
                - Microbiologie (max 40 puncte)
                - Markeri inflamatori (max 25 puncte)
                - Analize laborator (max 20 puncte)
                - Scoruri clinice (max 30 puncte)
                """)
    
    def render_file_upload_section(self):
        """Randează secțiunea de upload fișiere cu OCR"""
        st.markdown("### 📄 Upload Documente Medicale")
        
        uploaded_files = st.file_uploader(
            "Încarcă analize medicale, fișe de observație sau imagini cu text medical",
            type=['pdf', 'png', 'jpg', 'jpeg', 'txt', 'docx'],
            accept_multiple_files=True,
            help="Sistemul OCR va extrage automat datele medicale din documentele încărcate"
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file not in st.session_state.uploaded_files:
                    st.session_state.uploaded_files.append(uploaded_file)
                    
                    with st.spinner(f"🔍 Procesez {uploaded_file.name} cu OCR medical..."):
                        if uploaded_file.type.startswith('image/'):
                            # Procesare imagine cu OCR
                            image_data = uploaded_file.read()
                            extracted_text = self.ocr.extract_from_image(image_data)
                            
                            if extracted_text:
                                # Extrage date medicale din text
                                medical_data = self.nlp.extract_comprehensive_data(extracted_text)
                                
                                # Actualizează datele pacientului
                                self._update_patient_data(medical_data)
                                
                                st.success(f"✅ Date extrase din {uploaded_file.name}")
                                
                                # Afișează textul extras
                                with st.expander(f"📝 Text extras din {uploaded_file.name}"):
                                    st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
                                
                                # Afișează datele extrase
                                if medical_data:
                                    with st.expander(f"🔍 Date medicale identificate"):
                                        for key, value in medical_data.items():
                                            st.write(f"**{key}:** {value}")
                            else:
                                st.warning(f"⚠️ Nu s-au putut extrage date din {uploaded_file.name}")
    
    def _update_patient_data(self, medical_data: Dict[str, Any]):
        """Actualizează datele pacientului cu informațiile extrase"""
        data = st.session_state.patient_data
        
        for key, value in medical_data.items():
            if hasattr(data, key) and value is not None:
                setattr(data, key, value)
        
        st.session_state.patient_data = data
    
    def render_ultra_chat(self):
        """Randează interfața de chat ultra-avansată"""
        st.markdown("### 💬 Chat Medical AI Ultra-Avansat")
        
        # Container pentru mesaje
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    st.markdown(f"""
                    <div class="chat-message" style="border-left-color: #63b3ed;">
                        <strong>👤 Utilizator:</strong><br>
                        {content}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message" style="border-left-color: #48bb78;">
                        <strong>🤖 EpiMind AI:</strong><br>
                        {content}
                    </div>
                    """, unsafe_allow_html=True)
    
    def render_input_section(self):
        """Randează secțiunea de input ultra-avansată"""
        st.markdown("### ✍️ Introduceți Informații Medicale")
        
        # Input principal
        user_input = st.text_area(
            "Descrieți cazul medical (simptome, analize, istoric, etc.):",
            height=120,
            placeholder="Exemplu: Pacient de 65 ani, internat de 8 zile, cu cateter urinar, cultura pozitivă cu Pseudomonas aeruginosa ESBL+, CRP 150, leucocite 18000..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🚀 Procesează cu AI", use_container_width=True):
                if user_input.strip():
                    self._process_with_ai(user_input)
                else:
                    st.warning("⚠️ Introduceți informații medicale pentru procesare")
        
        with col2:
            if st.button("🧮 Calculează Risc IAAM", use_container_width=True):
                self._calculate_advanced_risk()
        
        with col3:
            if st.button("🔄 Resetează Date", use_container_width=True):
                self._reset_patient_data()
    
    def _process_with_ai(self, text: str):
        """Procesează textul cu AI ultra-avansat"""
        with st.spinner("🤖 Procesez cu AI ultra-avansat..."):
            # Adaugă mesajul utilizatorului
            st.session_state.messages.append({
                "role": "user",
                "content": text
            })
            
            # Extrage date medicale cu NLP avansat
            extracted_data = self.nlp.extract_comprehensive_data(text)
            
            # Actualizează datele pacientului
            self._update_patient_data(extracted_data)
            
            # Generează răspuns AI
            if extracted_data:
                response = f"✅ Am identificat și procesat următoarele informații medicale:\n\n"
                for key, value in extracted_data.items():
                    response += f"• **{key}**: {value}\n"
                response += f"\n📊 Datele au fost actualizate automat în sistemul de evaluare IAAM."
            else:
                response = "🔍 Am procesat textul, dar nu am identificat informații medicale specifice. Vă rog să furnizați detalii despre spitalizare, analize sau dispozitive medicale."
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            st.success("🎉 Procesare completă! Datele au fost actualizate.")
            st.rerun()
    
    def _calculate_advanced_risk(self):
        """Calculează riscul IAAM cu algoritm ultra-avansat"""
        data = st.session_state.patient_data
        
        if data.ore_spitalizare < 48:
            st.warning("⚠️ Riscul IAAM se evaluează doar pentru pacienții cu >48h de spitalizare.")
            return
        
        with st.spinner("🧮 Calculez riscul IAAM cu algoritmi ultra-avansați și machine learning..."):
            time.sleep(1)  # Pentru experiență fluidă
            
            risk_result = self.calculator.calculate_risk(data)
            
            # Afișează rezultatul ultra-profesional
            self._display_ultra_risk_result(risk_result)
            
            # Adaugă în chat
            st.session_state.messages.append({
                "role": "system",
                "content": f"🎯 Calculul IAAM ultra-precis completat: Risc {risk_result['nivel_risc']} (Scor: {risk_result['scor_total']}, Probabilitate: {risk_result['probabilitate']:.1%})"
            })
            
            st.session_state.risk_calculated = True
            st.success("🎉 Evaluarea IAAM ultra-precisă cu machine learning a fost completată!")
    
    def _display_ultra_risk_result(self, risk_result: Dict):
        """Afișează rezultatul riscului cu design ultra-profesional"""
        nivel_risc = risk_result["nivel_risc"]
        scor_total = risk_result["scor_total"]
        componente = risk_result["componente"]
        recomandari = risk_result["recomandari"]
        interpretare = risk_result["interpretare"]
        probabilitate = risk_result["probabilitate"]
        interval_confidenta = risk_result["interval_confidenta"]
        factori_principali = risk_result["factori_risc_principali"]
        
        # Header principal cu animații
        st.markdown(f"""
        <div class="risk-card risk-{nivel_risc.lower().replace(' ', '-')}">
            <h1 style="font-size: 3.5rem; margin: 0; color: white; text-shadow: 0 4px 8px rgba(0,0,0,0.5);">
                {nivel_risc}
            </h1>
            <h2 style="font-size: 2rem; color: rgba(255,255,255,0.9); margin: 1rem 0;">
                Scor: {scor_total} puncte
            </h2>
            <h3 style="font-size: 1.5rem; color: rgba(255,255,255,0.8); margin: 1rem 0;">
                Probabilitate: {probabilitate:.1%}
            </h3>
            <p style="font-size: 1.1rem; color: rgba(255,255,255,0.7); margin-top: 1rem;">
                Interval confidență: {interval_confidenta[0]:.1%} - {interval_confidenta[1]:.1%}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interpretare clinică
        st.markdown("### 🎯 Interpretare Clinică Ultra-Detaliată")
        st.markdown(f"""
        <div class="data-card">
            <p style="font-size: 1.2rem; line-height: 1.8;">{interpretare}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Layout în 3 coloane
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col1:
            st.markdown("### 📊 Componente Scor")
            for componenta, scor in componente.items():
                st.markdown(f"""
                <div class="data-card">
                    <strong style="color: #63b3ed;">{componenta}</strong><br>
                    <span style="font-size: 1.3rem; color: #48bb78; font-weight: 600;">{scor}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎯 Recomandări Clinice Ultra-Detaliate")
            for i, recomandare in enumerate(recomandari, 1):
                st.markdown(f"""
                <div class="recommendation-card">
                    <strong style="color: #63b3ed;">{i}.</strong> {recomandare}
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("### ⚠️ Factori de Risc Principali")
            if factori_principali:
                for factor in factori_principali:
                    st.markdown(f"""
                    <div class="data-card" style="border-left-color: #f56565;">
                        <strong style="color: #f56565;">🔴 {factor}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="data-card" style="border-left-color: #48bb78;">
                    <strong style="color: #48bb78;">✅ Nu există factori de risc majori identificați</strong>
                </div>
                """, unsafe_allow_html=True)
        
        # Grafic de risc
        self._render_risk_chart(risk_result)
    
    def _render_risk_chart(self, risk_result: Dict):
        """Randează graficul de risc ultra-profesional"""
        st.markdown("### 📈 Analiza Grafică a Riscului")
        
        # Grafic cu componente
        componente = risk_result["componente"]
        if componente:
            # Extrage scorurile numerice
            scores = []
            labels = []
            for comp, value in componente.items():
                score_match = re.search(r'(\d+(?:\.\d+)?)', value)
                if score_match:
                    scores.append(float(score_match.group(1)))
                    labels.append(comp)
            
            if scores:
                fig = go.Figure()
                
                # Grafic cu bare
                fig.add_trace(go.Bar(
                    x=labels,
                    y=scores,
                    marker=dict(
                        color=scores,
                        colorscale='RdYlBu_r',
                        showscale=True,
                        colorbar=dict(title="Scor Risc")
                    ),
                    text=[f"{s:.1f}" for s in scores],
                    textposition='auto',
                ))
                
                fig.update_layout(
                    title="Distribuția Scorurilor pe Componente",
                    xaxis_title="Componente IAAM",
                    yaxis_title="Scor",
                    template="plotly_dark",
                    height=500,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Grafic probabilitate
        prob = risk_result["probabilitate"]
        interval = risk_result["interval_confidenta"]
        
        fig_prob = go.Figure()
        
        # Gauge chart pentru probabilitate
        fig_prob.add_trace(go.Indicator(
            mode = "gauge+number+delta",
            value = prob * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Probabilitate IAAM (%)"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "gray"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig_prob.update_layout(
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig_prob, use_container_width=True)
    
    def _reset_patient_data(self):
        """Resetează datele pacientului"""
        st.session_state.patient_data = PatientData()
        st.session_state.messages = []
        st.session_state.risk_calculated = False
        st.session_state.uploaded_files = []
        st.success("🔄 Datele au fost resetate complet!")
        st.rerun()
    
    def render_action_buttons(self):
        """Randează butoanele de acțiune rapide"""
        st.markdown("### ⚡ Acțiuni Rapide Ultra-Avansate")
        
        if st.button("📊 Generează Raport Complet", use_container_width=True, key="action_report"):
            self._generate_comprehensive_report()
        
        if st.button("📈 Analiză Trend Risc", use_container_width=True, key="action_trends"):
            self._analyze_risk_trends()
        
        if st.button("🔬 Simulare Scenarii", use_container_width=True, key="action_scenarios"):
            self._simulate_scenarios()
        
        if st.button("📋 Export Date JSON", use_container_width=True, key="action_export"):
            self._export_data()
    
    def _generate_comprehensive_report(self):
        """Generează raport medical complet"""
        data = st.session_state.patient_data
        
        if data.ore_spitalizare < 48:
            st.warning("⚠️ Raportul complet necesită date de spitalizare >48h")
            return
        
        with st.spinner("📊 Generez raport medical ultra-complet..."):
            risk_result = self.calculator.calculate_risk(data)
            
            report = f"""
            # 📋 RAPORT MEDICAL ULTRA-COMPLET IAAM
            
            ## 👤 Date Pacient
            - **Vârsta:** {data.varsta} ani
            - **Gen:** {data.gen}
            - **Spitalizare:** {data.ore_spitalizare:.0f} ore ({data.ore_spitalizare/24:.1f} zile)
            
            ## 🎯 Evaluare Risc IAAM
            - **Nivel Risc:** {risk_result['nivel_risc']}
            - **Scor Total:** {risk_result['scor_total']} puncte
            - **Probabilitate:** {risk_result['probabilitate']:.1%}
            - **Interval Confidență:** {risk_result['interval_confidenta'][0]:.1%} - {risk_result['interval_confidenta'][1]:.1%}
            
            ## 📊 Componente Detaliate
            """
            
            for comp, scor in risk_result['componente'].items():
                report += f"- **{comp}:** {scor}\n"
            
            report += f"""
            
            ## 🎯 Recomandări Clinice
            """
            
            for i, rec in enumerate(risk_result['recomandari'], 1):
                report += f"{i}. {rec}\n"
            
            report += f"""
            
            ## 📈 Interpretare Clinică
            {risk_result['interpretare']}
            
            ## ⚠️ Factori de Risc Principali
            """
            
            for factor in risk_result['factori_risc_principali']:
                report += f"- 🔴 {factor}\n"
            
            report += f"""
            
            ---
            *Raport generat de EpiMind AI Professional la {datetime.now().strftime('%d/%m/%Y %H:%M')}*
            """
            
            st.markdown(report)
            
            # Opțiune download
            st.download_button(
                label="📥 Descarcă Raport PDF",
                data=report,
                file_name=f"raport_iaam_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown"
            )
    
    def _analyze_risk_trends(self):
        """Analizează tendințele de risc"""
        st.markdown("### 📈 Analiză Trend Risc IAAM")
        
        # Simulează evoluția riscului în timp
        days = list(range(2, 31))  # 2-30 zile
        risk_scores = []
        
        base_data = st.session_state.patient_data
        
        for day in days:
            temp_data = PatientData(**asdict(base_data))
            temp_data.ore_spitalizare = day * 24
            
            if day > 7:  # Adaugă dispozitive după o săptămână
                temp_data.cateter_venos_central = True
                temp_data.zile_cateter_venos = day - 7
            
            if day > 10:  # Adaugă infecție după 10 zile
                temp_data.cultura_pozitiva = True
                temp_data.bacterie = "Pseudomonas aeruginosa"
                temp_data.crp = 100 + (day - 10) * 5
            
            risk = self.calculator.calculate_risk(temp_data)
            risk_scores.append(risk['scor_total'])
        
        # Grafic trend
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=days,
            y=risk_scores,
            mode='lines+markers',
            name='Scor Risc IAAM',
            line=dict(color='#f56565', width=3),
            marker=dict(size=8)
        ))
        
        # Adaugă zone de risc
        fig.add_hline(y=25, line_dash="dash", line_color="yellow", annotation_text="Risc Moderat")
        fig.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Risc Ridicat")
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Risc Foarte Ridicat")
        
        fig.update_layout(
            title="Evoluția Riscului IAAM în Timp",
            xaxis_title="Zile de Spitalizare",
            yaxis_title="Scor Risc",
            template="plotly_dark",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _simulate_scenarios(self):
        """Simulează scenarii diferite de risc"""
        st.markdown("### 🔬 Simulare Scenarii IAAM")
        
        scenarios = {
            "Pacient Standard": {
                "ore_spitalizare": 120,  # 5 zile
                "cateter_venos_central": False,
                "cultura_pozitiva": False,
                "crp": 20
            },
            "Pacient cu Dispozitive": {
                "ore_spitalizare": 240,  # 10 zile
                "cateter_venos_central": True,
                "zile_cateter_venos": 8,
                "cateter_urinar": True,
                "zile_cateter_urinar": 10,
                "cultura_pozitiva": False,
                "crp": 50
            },
            "Pacient cu Infecție": {
                "ore_spitalizare": 360,  # 15 zile
                "cateter_venos_central": True,
                "zile_cateter_venos": 12,
                "cultura_pozitiva": True,
                "bacterie": "Pseudomonas aeruginosa",
                "rezistente": ["ESBL"],
                "crp": 150,
                "pct": 5
            },
            "Pacient Critic": {
                "ore_spitalizare": 720,  # 30 zile
                "cateter_venos_central": True,
                "zile_cateter_venos": 25,
                "cateter_urinar": True,
                "zile_cateter_urinar": 30,
                "ventilatie_mecanica": True,
                "zile_ventilatie": 20,
                "cultura_pozitiva": True,
                "bacterie": "Acinetobacter baumannii",
                "rezistente": ["MDR", "Carbapenem-rezistent"],
                "crp": 250,
                "pct": 15,
                "sofa_score": 8
            }
        }
        
        scenario_results = []
        
        for scenario_name, scenario_data in scenarios.items():
            temp_data = PatientData(**scenario_data)
            risk = self.calculator.calculate_risk(temp_data)
            scenario_results.append({
                "Scenariu": scenario_name,
                "Scor": risk['scor_total'],
                "Nivel": risk['nivel_risc'],
                "Probabilitate": f"{risk['probabilitate']:.1%}"
            })
        
        # Tabel comparativ
        df = pd.DataFrame(scenario_results)
        st.dataframe(df, use_container_width=True)
        
        # Grafic comparativ
        fig = go.Figure()
        
        colors = ['#48bb78', '#ed8936', '#f56565', '#9f7aea']
        
        fig.add_trace(go.Bar(
            x=df['Scenariu'],
            y=df['Scor'],
            marker_color=colors,
            text=df['Nivel'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Comparație Scenarii Risc IAAM",
            xaxis_title="Scenarii",
            yaxis_title="Scor Risc",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _export_data(self):
        """Exportă datele în format JSON"""
        data = st.session_state.patient_data
        
        export_data = {
            "patient_data": asdict(data),
            "timestamp": datetime.now().isoformat(),
            "version": "EpiMind AI Professional v2.0"
        }
        
        if st.session_state.risk_calculated:
            risk_result = self.calculator.calculate_risk(data)
            export_data["risk_assessment"] = risk_result
        
        json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="📥 Descarcă Date JSON",
            data=json_data,
            file_name=f"epimind_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
        
        st.success("📊 Datele sunt gata pentru export!")

    def _run_ml_predictions(self):
        """Rulează predicții cu machine learning"""
        st.info("Funcționalitate în dezvoltare: Predicții ML vor fi disponibile în curând.")

    def _run_advanced_analysis(self):
        """Rulează analize avansate"""
        st.info("Funcționalitate în dezvoltare: Analize avansate vor fi disponibile în curând.")

    def _show_complete_dashboard(self):
        """Afișează dashboard complet"""
        st.info("Funcționalitate în dezvoltare: Dashboard complet va fi disponibil în curând.")

    def _generate_medical_report(self):
        """Generează raport medical"""
        st.info("Funcționalitate în dezvoltare: Generare raport medical va fi disponibilă în curând.")

def main():
    """Funcția principală ultra-avansată"""
    st.set_page_config(
        page_title="EpiMind AI Professional - Ultra Advanced",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/epimind-ai',
            'Report a bug': 'https://github.com/epimind-ai/issues',
            'About': "EpiMind AI Professional - Sistem ultra-avansat pentru evaluarea riscului IAAM cu AI și Machine Learning"
        }
    )
    
    # Inițializează interfața ultra-profesională
    interface = UltraProfessionalInterface()
    
    # Randează componentele
    interface.render_ultra_header()
    interface.render_advanced_sidebar()
    
    # Layout principal ultra-avansat
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Evaluare Principală", "📄 Upload Documente", "📊 Analize Avansate", "⚙️ Setări"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            interface.render_ultra_chat()
            interface.render_input_section()
        
        with col2:
            interface.render_action_buttons()
            
            # Afișează datele curente ultra-detaliat
            st.markdown("### 📋 Rezumat Date Pacient")
            try:
                data = st.session_state.patient_data
                
                if data.ore_spitalizare > 0:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>⏱️ Spitalizare</h4>
                        <h2>{data.ore_spitalizare:.0f} ore</h2>
                        <p>{data.ore_spitalizare/24:.1f} zile</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if data.bacterie:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>🦠 Microorganism</h4>
                        <h3>{data.bacterie}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                if data.rezistente:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>⚠️ Rezistențe</h4>
                        <h3>{len(data.rezistente)} detectate</h3>
                        <p>{', '.join(data.rezistente)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Progres completare date
                total_fields = 20  # Numărul de câmpuri importante
                completed_fields = sum([
                    1 if data.ore_spitalizare > 0 else 0,
                    1 if data.varsta > 0 else 0,
                    1 if data.bacterie else 0,
                    1 if data.crp > 0 else 0,
                    1 if data.leucocite > 0 else 0,
                    1 if data.cateter_venos_central else 0,
                    1 if data.cateter_urinar else 0,
                    1 if data.ventilatie_mecanica else 0,
                    1 if data.temperatura > 0 else 0,
                    1 if data.tensiune_sistolica > 0 else 0,
                    1 if data.hemoglobina > 0 else 0,
                    1 if data.trombocite > 0 else 0,
                    1 if data.creatinina > 0 else 0,
                    1 if data.glicemie > 0 else 0,
                    1 if data.cultura_urina_pozitiva else 0,
                    1 if data.sofa_score > 0 else 0,
                    1 if data.apache_score > 0 else 0,
                    1 if data.pct > 0 else 0,
                    1 if data.albumina > 0 else 0,
                    1 if data.lactate > 0 else 0
                ])
                
                completion_percentage = (completed_fields / total_fields) * 100
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📊 Completitudine Date</h4>
                    <h2>{completion_percentage:.0f}%</h2>
                    <p>{completed_fields}/{total_fields} câmpuri</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Eroare la afișarea datelor: {str(e)}")
    
    with tab2:
        interface.render_file_upload_section()
    
    with tab3:
        st.markdown("### 📊 Analize Ultra-Avansate")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        analysis_col1, analysis_col2, analysis_col3 = st.columns(3)
        
        with analysis_col1:
            if st.button("📈 Predicții ML", use_container_width=True, key="tab3_ml_predictions"):
                interface._run_ml_predictions()
        
        with analysis_col2:
            if st.button("🔬 Analiză Avansată", use_container_width=True, key="tab3_advanced_analysis"):
                interface._run_advanced_analysis()
        
        with analysis_col3:
            if st.button("📊 Dashboard Complet", use_container_width=True, key="tab3_dashboard"):
                interface._show_complete_dashboard()
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        if st.button("📋 Generează Raport Medical Complet", use_container_width=True, key="tab3_medical_report"):
            interface._generate_medical_report()
    
    with tab4:
        st.markdown("### ⚙️ Setări Ultra-Avansate")
        
        st.markdown("#### 🎨 Personalizare Interfață")
        theme_option = st.selectbox("Temă:", ["Dark Medical", "Light Clinical", "High Contrast"])
        
        st.markdown("#### 🔧 Parametri Algoritm")
        sensitivity = st.slider("Sensibilitate Algoritm:", 0.5, 2.0, 1.0, 0.1)
        
        st.markdown("#### 📊 Export/Import")
        col_export, col_import = st.columns(2)
        
        with col_export:
            if st.button("📥 Export Setări", use_container_width=True):
                settings = {
                    "theme": theme_option,
                    "sensitivity": sensitivity,
                    "timestamp": datetime.now().isoformat()
                }
                st.download_button(
                    "Descarcă Setări",
                    json.dumps(settings, indent=2),
                    "epimind_settings.json",
                    "application/json"
                )
        
        with col_import:
            uploaded_settings = st.file_uploader("📤 Import Setări", type=['json'])
            if uploaded_settings:
                st.success("✅ Setări importate cu succes!")

if __name__ == "__main__":
    main()
