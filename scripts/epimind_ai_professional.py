import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import re
import json
import time
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple, Any
import requests
from pathlib import Path

# Configurare logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PatientData:
    """Structură completă pentru datele pacientului"""
    # Date demografice
    varsta: int = 0
    gen: str = ""
    
    # Date spitalizare
    ore_spitalizare: float = 0.0
    
    # Dispozitive invazive
    cateter_urinar: bool = False
    cateter_vascular: bool = False
    ventilatie_mecanica: bool = False
    sonda_nazogastrica: bool = False
    drenaj_chirurgical: bool = False
    
    # Microbiologie
    bacteria: str = ""
    rezistenta_antibiotice: str = ""
    
    # Semne vitale
    temperatura: float = 0.0
    tensiune_sistolica: int = 0
    tensiune_diastolica: int = 0
    frecventa_cardiaca: int = 0
    frecventa_respiratorie: int = 0
    
    # Markeri inflamatori
    crp: float = 0.0
    pct: float = 0.0
    leucocite: float = 0.0
    
    # Hemograma completa
    hemoglobina: float = 0.0  # g/dL
    hematocrit: float = 0.0   # %
    trombocite: float = 0.0   # /μL
    neutrofile: float = 0.0   # %
    limfocite: float = 0.0    # %
    monocite: float = 0.0     # %
    eozinofile: float = 0.0   # %
    bazofile: float = 0.0     # %
    
    # Biochimie sanguina
    glicemie: float = 0.0     # mg/dL
    uree: float = 0.0         # mg/dL
    creatinina: float = 0.0   # mg/dL
    sodiu: float = 0.0        # mEq/L
    potasiu: float = 0.0      # mEq/L
    clor: float = 0.0         # mEq/L
    
    # Functia hepatica
    alt_alat: float = 0.0     # U/L
    ast_asat: float = 0.0     # U/L
    bilirubina_totala: float = 0.0  # mg/dL
    bilirubina_directa: float = 0.0 # mg/dL
    albumina: float = 0.0     # g/dL
    
    # Coagulare
    pt: float = 0.0           # secunde
    ptt: float = 0.0          # secunde
    inr: float = 0.0
    fibrinogen: float = 0.0   # mg/dL
    
    # Gaze sanguine
    ph_sanguin: float = 0.0
    pco2: float = 0.0         # mmHg
    po2: float = 0.0          # mmHg
    hco3: float = 0.0         # mEq/L
    saturatie_o2: float = 0.0 # %
    
    # Analize urinare
    proteinurie: str = ""  # absent, urme, +, ++, +++, ++++
    hematurie: str = ""    # absent, urme, +, ++, +++, ++++
    nitriti: bool = False
    leucocit_esteraza: str = ""  # negativ, pozitiv, +, ++, +++
    bacterii_urina: int = 0  # CFU/mL
    cultura_urina_pozitiva: bool = False
    bacterie_urina: str = ""
    densitate_urina: float = 0.0  # specific gravity
    ph_urina: float = 0.0
    glucoza_urina: str = ""  # absent, urme, +, ++, +++
    cetone_urina: str = ""   # absent, urme, +, ++, +++
    bilirubina_urina: str = ""  # absent, urme, +, ++
    urobilinogen_urina: str = ""  # normal, crescut
    
    # Scoruri clinice
    glasgow_coma_scale: int = 15
    sofa_score: int = 0

class ProfessionalAI:
    """AI ultra-avansat pentru procesare medicală"""
    
    def __init__(self):
        self.ollama_available = self._check_ollama()
        self.medical_knowledge = self._load_medical_knowledge()
        
    def _check_ollama(self) -> bool:
        """Verifică disponibilitatea Ollama"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _load_medical_knowledge(self) -> Dict:
        """Încarcă baza de cunoștințe medicale extinsă"""
        return {
            "bacteria_patterns": {
                r"pseudomonas\s+aeruginosa|p\.?\s*aeruginosa|pseudomonas|aeruginosa": "Pseudomonas aeruginosa",
                r"escherichia\s+coli|e\.?\s*coli|ecoli|e\s*coli": "Escherichia coli",
                r"klebsiella\s+pneumoniae|k\.?\s*pneumoniae|klebsiella": "Klebsiella pneumoniae",
                r"staphylococcus\s+aureus|s\.?\s*aureus|staph\s+aureus|mrsa|mssa": "Staphylococcus aureus",
                r"acinetobacter\s+baumannii|a\.?\s*baumannii|acinetobacter": "Acinetobacter baumannii",
                r"enterococcus\s+faecium|e\.?\s*faecium|enterococcus|vre": "Enterococcus faecium",
                r"candida\s+auris|c\.?\s*auris|candida": "Candida auris",
                r"clostridioides\s+difficile|c\.?\s*difficile|cdiff|clostridium": "Clostridioides difficile",
                r"enterobacter\s+cloacae|enterobacter": "Enterobacter cloacae",
                r"serratia\s+marcescens|serratia": "Serratia marcescens"
            },
            "resistance_patterns": {
                r"carbapenem\s*rezistent|crp|carbapenemaza": "Carbapenem-rezistent",
                r"esbl|beta\s*lactamaza": "ESBL",
                r"mrsa|meticilina\s*rezistent": "MRSA",
                r"vre|vancomicina\s*rezistent": "VRE",
                r"mdr|multi\s*drug\s*rezistent": "MDR",
                r"xdr|extensively\s*drug\s*rezistent": "XDR",
                r"pan\s*drug\s*rezistent|pdr": "PDR"
            },
            "urine_patterns": {
                r"proteinurie\s*[:=]?\s*(absent|urme|\+{1,4}|negativ|pozitiv)": "proteinurie",
                r"proteina\s*[:=]?\s*(absent|urme|\+{1,4}|negativ|pozitiv)": "proteinurie",
                r"hematurie\s*[:=]?\s*(absent|urme|\+{1,4}|negativ|pozitiv)": "hematurie",
                r"sange\s+urina\s*[:=]?\s*(absent|urme|\+{1,4}|negativ|pozitiv)": "hematurie",
                r"nitriti\s*[:=]?\s*(pozitiv|negativ|present|absent|\+)": "nitriti",
                r"leucocit\s*esteraza\s*[:=]?\s*(pozitiv|negativ|\+{1,3})": "leucocit_esteraza",
                r"bacterii\s*[:=]?\s*(\d+)\s*(?:cfu|ufc)": "bacterii_urina",
                r"cultura\s*urina\s*[:=]?\s*(pozitiv|negativ)": "cultura_urina",
                r"densitate\s*[:=]?\s*(\d+\.\d+)": "densitate_urina",
                r"ph\s*urina\s*[:=]?\s*(\d+\.\d+)": "ph_urina",
                r"glucoza\s*urina\s*[:=]?\s*(absent|urme|\+{1,3})": "glucoza_urina",
                r"cetone\s*urina\s*[:=]?\s*(absent|urme|\+{1,3})": "cetone_urina",
                r"bilirubina\s*urina\s*[:=]?\s*(absent|urme|\+{1,2})": "bilirubina_urina",
                r"urobilinogen\s*[:=]?\s*(normal|crescut)": "urobilinogen_urina"
            },
            "hospitalization_patterns": [
                r"(\d+)\s+(?:de\s+)?(?:zile|days?)",  # Detectează "8 zile" sau "8 de zile"
                r"(\d+)\s+(?:de\s+)?(?:ore|hours?)",  # Detectează "8 ore" sau "8 de ore"
                r"internat\s+(?:de\s+)?(\d+)\s+(?:de\s+)?(?:ore|hours?)",
                r"spitalizat\s+(?:de\s+)?(\d+)\s+(?:de\s+)?(?:ore|hours?)",
                r"(?:de\s+)?(\d+)\s+(?:de\s+)?(?:ore|hours?)\s+(?:de\s+)?(?:internare|spitalizare)",
                r"internare\s+(?:de\s+)?(\d+)\s+(?:de\s+)?(?:zile|days?)",
                r"spitalizare\s+(?:de\s+)?(\d+)\s+(?:de\s+)?(?:zile|days?)",
                r"(?:de\s+)?(\d+)\s+(?:de\s+)?(?:zile|days?)\s+(?:de\s+)?(?:internare|spitalizare)",
                r"ziua\s+(\d+)\s+(?:de\s+)?(?:internare|spitalizare)",
                r"day\s+(\d+)\s+of\s+(?:hospitalization|admission)"
            ]
        }
    
    def extract_medical_data(self, text: str) -> Dict[str, Any]:
        """Extracție ultra-avansată de date medicale"""
        text_lower = text.lower().strip()
        extracted = {}
        
        # Extrage bacterii cu pattern matching îmbunătățit
        for pattern, bacterie in self.medical_knowledge["bacteria_patterns"].items():
            if re.search(pattern, text_lower, re.IGNORECASE | re.UNICODE):
                extracted["bacterie"] = bacterie
                extracted["cultura_pozitiva"] = True
                logger.info(f"✅ Bacterie detectată: {bacterie}")
                break
        
        # Extrage rezistențe
        rezistente = []
        for pattern, rezistenta in self.medical_knowledge["resistance_patterns"].items():
            if re.search(pattern, text_lower, re.IGNORECASE | re.UNICODE):
                rezistente.append(rezistenta)
                logger.info(f"✅ Rezistență detectată: {rezistenta}")
        
        if rezistente:
            extracted["rezistente"] = rezistente
        
        # Extrage ore spitalizare cu algoritm îmbunătățit
        for pattern in self.medical_knowledge["hospitalization_patterns"]:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.UNICODE)
            if match:
                value = int(match.group(1))
                # Detectează dacă sunt zile sau ore
                if "zile" in pattern or "days" in pattern or "ziua" in pattern:
                    extracted["ore_spitalizare"] = float(value * 24)
                    logger.info(f"✅ Spitalizare detectată: {value} zile = {value * 24} ore")
                else:
                    extracted["ore_spitalizare"] = float(value)
                    logger.info(f"✅ Spitalizare detectată: {value} ore")
                break
        
        # Extrage parametri vitali cu regex îmbunătățit
        vital_patterns = {
            r"temperatura?\s*[:=]?\s*(\d+(?:\.\d+)?)\s*°?c?": "temperatura",
            r"temp\s*[:=]?\s*(\d+(?:\.\d+)?)\s*°?c?": "temperatura",
            r"ta\s*[:=]?\s*(\d+)/(\d+)": "tensiune",
            r"tensiune\s*[:=]?\s*(\d+)/(\d+)": "tensiune",
            r"fc\s*[:=]?\s*(\d+)": "frecventa_cardiaca",
            r"puls\s*[:=]?\s*(\d+)": "frecventa_cardiaca",
            r"fr\s*[:=]?\s*(\d+)": "frecventa_respiratorie",
            r"crp\s*[:=]?\s*(\d+(?:\.\d+)?)": "crp",
            r"pct\s*[:=]?\s*(\d+(?:\.\d+)?)": "pct",
            r"leucocite\s*[:=]?\s*(\d+(?:\.\d+)?)": "leucocite",
            r"glasgow\s*[:=]?\s*(\d+)": "glasgow_coma_scale"
        }
        
        for pattern, param in vital_patterns.items():
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                if param == "tensiune":
                    extracted["tensiune_sistolica"] = int(match.group(1))
                    extracted["tensiune_diastolica"] = int(match.group(2))
                else:
                    value = float(match.group(1))
                    extracted[param] = value
                logger.info(f"✅ Parametru detectat: {param} = {match.group(1)}")
        
        # Extrage parametri analize urinare
        for pattern, param in self.medical_knowledge["urine_patterns"].items():
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                value = match.group(1)
                if param == "nitriti":
                    extracted[param] = value.lower() in ["pozitiv", "present", "+"]
                elif param == "cultura_urina":
                    extracted["cultura_urina_pozitiva"] = value.lower() == "pozitiv"
                elif param == "bacterii_urina":
                    extracted[param] = int(value)
                elif param in ["densitate_urina", "ph_urina"]:
                    extracted[param] = float(value)
                else:
                    extracted[param] = value
                logger.info(f"✅ Parametru urinar detectat: {param} = {value}")

        return extracted
    
    def generate_response(self, user_input: str, context: Dict) -> str:
        """Generează răspuns AI ultra-inteligent"""
        if self.ollama_available:
            return self._generate_with_ollama(user_input, context)
        else:
            return self._generate_fallback(user_input, context)
    
    def _generate_with_ollama(self, user_input: str, context: Dict) -> str:
        """Generare cu Ollama AI"""
        try:
            prompt = self._create_advanced_prompt(user_input, context)
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 200
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            
        except Exception as e:
            logger.error(f"Ollama error: {e}")
        
        return self._generate_fallback(user_input, context)
    
    def _generate_fallback(self, user_input: str, context: Dict) -> str:
        """AI fallback ultra-inteligent"""
        data = context.get("patient_data", {})
        completion = context.get("completion_status", {})
        
        # Analiză inteligentă a input-ului
        input_lower = user_input.lower()
        
        # Răspunsuri contextuale inteligente
        if any(bacteria in input_lower for bacteria in ["pseudomonas", "aeruginosa", "escherichia", "klebsiella"]):
            if not data.get("cultura_pozitiva"):
                return "Excelent! Am detectat microorganismul. Există rezistențe cunoscute (ESBL, carbapenem-rezistent, MRSA)?"
            else:
                return "Perfect! Microorganismul a fost înregistrat. Mai aveți nevoie de alte informații clinice?"
        
        if "ore" in input_lower or "zile" in input_lower or "internat" in input_lower:
            if data.get("ore_spitalizare", 0) > 0:
                ore = data.get("ore_spitalizare", 0)
                zile = int(ore / 24)
                return f"Înregistrat: {zile} zile ({ore:.0f} ore) de spitalizare. Sunt dispozitive invazive (cateter, ventilație)?"
            else:
                return "Vă rog să specificați durata spitalizării în ore sau zile pentru evaluarea riscului IAAM."
        
        # Verifică completarea datelor
        missing_critical = []
        if data.get("ore_spitalizare", 0) < 48:
            missing_critical.append("durata spitalizării (>48h)")
        if not data.get("cultura_pozitiva"):
            missing_critical.append("rezultate microbiologice")
        
        if missing_critical:
            return f"Pentru evaluarea IAAM mai am nevoie de: {', '.join(missing_critical)}. Puteți furniza aceste informații?"
        
        # Sugerează calculul dacă datele sunt complete
        if data.get("ore_spitalizare", 0) >= 48:
            return "Datele par complete pentru evaluarea IAAM. Să calculez riscul de infecție asociată îngrijirilor medicale?"
        
        return "Vă rog să furnizați mai multe detalii despre pacient pentru o evaluare precisă a riscului IAAM."
    
    def _create_advanced_prompt(self, user_input: str, context: Dict) -> str:
        """Creează prompt avansat pentru AI"""
        return f"""
        Ești EpiMind AI, specialist în infecții nosocomiale și IAAM.
        
        Input utilizator: "{user_input}"
        Context: {json.dumps(context, indent=2)}
        
        Răspunde profesional în română, concis (max 2 propoziții).
        Focalizează-te pe colectarea datelor pentru evaluarea riscului IAAM.
        """

class AdvancedIAAMCalculator:
    """Calculator ultra-avansat pentru riscul IAAM"""
    
    def calculate_risk(self, data: PatientData) -> Dict[str, Any]:
        """Calculează riscul IAAM cu algoritm ultra-precis"""
        if data.ore_spitalizare < 48:
            return {
                "nivel_risc": "FĂRĂ RISC",
                "scor_total": 0,
                "mesaj": "Riscul IAAM se evaluează doar după 48h de spitalizare",
                "componente": {},
                "recomandari": ["Monitorizare standard", "Respectarea măsurilor de igienă"]
            }
        
        scor_total = 0
        componente = {}
        
        # 1. Scor temporal (îmbunătățit cu 6 niveluri)
        ore = data.ore_spitalizare
        if ore < 72:  # 48-72h
            scor_temporal = 8
            nivel_temporal = "Risc precoce (48-72h)"
        elif ore < 168:  # 3-7 zile
            scor_temporal = 15
            nivel_temporal = "Risc moderat (3-7 zile)"
        elif ore < 336:  # 1-2 săptămâni
            scor_temporal = 25
            nivel_temporal = "Risc ridicat (1-2 săptămâni)"
        elif ore < 720:  # 2-4 săptămâni
            scor_temporal = 35
            nivel_temporal = "Risc foarte ridicat (2-4 săptămâni)"
        elif ore < 1440:  # 1-2 luni
            scor_temporal = 45
            nivel_temporal = "Risc extrem (1-2 luni)"
        else:  # >2 luni
            scor_temporal = 55
            nivel_temporal = "Risc maxim (>2 luni)"
        
        componente["Durata spitalizării"] = f"{scor_temporal} ({nivel_temporal})"
        scor_total += scor_temporal
        
        # 2. Dispozitive invazive (scoring îmbunătățit)
        scor_dispozitive = 0
        if data.cateter_venos_central:
            scor_cateter = min(data.zile_cateter_venos * 3, 30)
            scor_dispozitive += scor_cateter
            componente["Cateter venos central"] = f"{scor_cateter} ({data.zile_cateter_venos} zile)"
        
        if data.cateter_urinar:
            scor_urinar = min(data.zile_cateter_urinar * 2, 20)
            scor_dispozitive += scor_urinar
            componente["Cateter urinar"] = f"{scor_urinar} ({data.zile_cateter_urinar} zile)"
        
        if data.ventilatie_mecanica:
            scor_ventilatie = min(data.zile_ventilatie * 4, 40)
            scor_dispozitive += scor_ventilatie
            componente["Ventilație mecanică"] = f"{scor_ventilatie} ({data.zile_ventilatie} zile)"
        
        scor_total += scor_dispozitive
        
        # 3. Microbiologie (scoring ultra-precis)
        scor_micro = 0
        if data.cultura_pozitiva and data.bacterie:
            # Scoring bazat pe patogenitatea bacteriei
            pathogen_scores = {
                "Pseudomonas aeruginosa": 25,
                "Acinetobacter baumannii": 25,
                "Klebsiella pneumoniae": 20,
                "Escherichia coli": 15,
                "Staphylococcus aureus": 20,
                "Enterococcus faecium": 18,
                "Candida auris": 30,
                "Clostridioides difficile": 35
            }
            
            scor_micro = pathogen_scores.get(data.bacterie, 10)
            componente["Microorganisme"] = f"{scor_micro} ({data.bacterie})"
            
            # Bonus pentru rezistențe
            if data.rezistente:
                resistance_bonus = len(data.rezistente) * 8
                scor_micro += resistance_bonus
                componente["Rezistențe"] = f"{resistance_bonus} ({', '.join(data.rezistente)})"
        
        scor_total += scor_micro
        
        # 4. Markeri inflamatori (nou)
        scor_inflamatori = 0
        if data.crp > 0:
            if data.crp > 150:
                scor_crp = 15
            elif data.crp > 50:
                scor_crp = 10
            elif data.crp > 10:
                scor_crp = 5
            else:
                scor_crp = 0
            scor_inflamatori += scor_crp
            componente["CRP"] = f"{scor_crp} (CRP: {data.crp} mg/L)"
        
        if data.pct > 0:
            if data.pct > 10:
                scor_pct = 20
            elif data.pct > 2:
                scor_pct = 15
            elif data.pct > 0.5:
                scor_pct = 10
            else:
                scor_pct = 5
            scor_inflamatori += scor_pct
            componente["PCT"] = f"{scor_pct} (PCT: {data.pct} ng/mL)"
        
        scor_total += scor_inflamatori
        
        # 5. Analize urinare (nou)
        scor_urinare = 0
        if data.cultura_urina_pozitiva:
            scor_urinare += 10
            componente["Cultura urina"] = "10 (pozitivă)"
        
        if data.bacterii_urina > 0:
            scor_bacterii = min(data.bacterii_urina * 0.5, 10)
            scor_urinare += scor_bacterii
            componente["Bacterii urina"] = f"{scor_bacterii} ({data.bacterii_urina} CFU/mL)"
        
        if data.nitriti:
            scor_urinare += 5
            componente["Nitriti"] = "5 (pozitivi)"
        
        if data.leucocit_esteraza:
            scor_leucocite = 5
            scor_urinare += scor_leucocite
            componente["Leucocite esterase"] = f"{scor_leucocite} ({data.leucocit_esteraza})"
        
        scor_total += scor_urinare
        
        # 6. Determinarea nivelului de risc (îmbunătățit)
        if scor_total < 20:
            nivel_risc = "SCĂZUT"
            culoare = "#28a745"
        elif scor_total < 40:
            nivel_risc = "MODERAT"
            culoare = "#ffc107"
        elif scor_total < 70:
            nivel_risc = "RIDICAT"
            culoare = "#fd7e14"
        elif scor_total < 100:
            nivel_risc = "FOARTE RIDICAT"
            culoare = "#dc3545"
        else:
            nivel_risc = "CRITIC"
            culoare = "#6f42c1"
        
        # 7. Recomandări clinice ultra-detaliate
        recomandari = self._generate_clinical_recommendations(nivel_risc, data, scor_total)
        
        return {
            "nivel_risc": nivel_risc,
            "scor_total": scor_total,
            "culoare": culoare,
            "componente": componente,
            "recomandari": recomandari,
            "interpretare": self._generate_interpretation(nivel_risc, scor_total, data)
        }
    
    def _generate_clinical_recommendations(self, nivel_risc: str, data: PatientData, scor: int) -> List[str]:
        """Generează recomandări clinice ultra-detaliate"""
        recomandari = []
        
        # Recomandări de bază
        recomandari.append("🧼 Igienă strictă a mâinilor înainte și după contactul cu pacientul")
        recomandari.append("🦠 Precauții de contact și izolare conform protocoalelor")
        
        # Recomandări specifice nivelului de risc
        if nivel_risc in ["RIDICAT", "FOARTE RIDICAT", "CRITIC"]:
            recomandari.append("🔬 Monitorizare microbiologică intensivă (culturi săptămânale)")
            recomandari.append("💊 Evaluare pentru terapie antimicrobiană profilactică")
            recomandari.append("👥 Consultare specialist boli infecțioase")
        
        if nivel_risc in ["FOARTE RIDICAT", "CRITIC"]:
            recomandari.append("🏥 Izolare în cameră separată cu presiune negativă")
            recomandari.append("⚡ Alertă echipă de control infecții nosocomiale")
            recomandari.append("📊 Raportare către comisia de infecții nosocomiale")
        
        # Recomandări specifice dispozitivelor
        if data.cateter_venos_central:
            recomandari.append("🩸 Evaluare zilnică necesitate cateter venos central")
            recomandari.append("🧽 Dezinfecție cu clorhexidină la manipularea cateterului")
        
        if data.cateter_urinar:
            recomandari.append("🚿 Evaluare zilnică necesitate cateter urinar")
            recomandari.append("💧 Menținerea sistemului de drenaj închis")
        
        if data.ventilatie_mecanica:
            recomandari.append("🫁 Protocol de sevraj ventilator accelerat")
            recomandari.append("🦷 Igienă orală cu clorhexidină")
        
        # Recomandări specifice microorganismelor
        if data.bacterie:
            if "Pseudomonas" in data.bacterie:
                recomandari.append("💉 Considerare terapie combinată anti-Pseudomonas")
            elif "Acinetobacter" in data.bacterie:
                recomandari.append("🔬 Testare sensibilitate la colistin și tigecyclină")
            elif "MRSA" in str(data.rezistente):
                recomandari.append("💊 Considerare vancomicină sau linezolid")
        
        # Recomandări specifice analizei urinare
        if data.cultura_urina_pozitiva:
            recomandari.append("🔬 Analiza culturii urinare pentru identificarea bacteriilor")
        
        if data.bacterii_urina > 0:
            recomandari.append(" antibiotice adecvate pentru bacterii urinare")
        
        if data.nitriti:
            recomandari.append("🔬 Testare urina pentru bacterii urinare")
        
        if data.leucocit_esteraza:
            recomandari.append("🔬 Testare urina pentru bacterii urinare")
        
        return recomandari
    
    def _generate_interpretation(self, nivel_risc: str, scor: int, data: PatientData) -> str:
        """Generează interpretare clinică detaliată"""
        interpretari = {
            "SCĂZUT": f"Risc scăzut de IAAM (scor: {scor}). Pacientul prezintă factori de risc minimi. Continuați măsurile standard de prevenție.",
            "MODERAT": f"Risc moderat de IAAM (scor: {scor}). Pacientul necesită monitorizare atentă și măsuri suplimentare de prevenție.",
            "RIDICAT": f"Risc ridicat de IAAM (scor: {scor}). Pacientul necesită măsuri intensive de prevenție și monitorizare microbiologică frecventă.",
            "FOARTE RIDICAT": f"Risc foarte ridicat de IAAM (scor: {scor}). Pacientul necesită măsuri maxime de prevenție și consultare specialist.",
            "CRITIC": f"Risc critic de IAAM (scor: {scor}). Pacientul necesită măsuri de urgență și management multidisciplinar."
        }
        
        return interpretari.get(nivel_risc, f"Risc nedeterminat (scor: {scor})")

class UltraProfessionalInterface:
    """Interfață ultra-profesională pentru aplicația medicală"""
    
    def __init__(self):
        self.ai = ProfessionalAI()
        self.calculator = AdvancedIAAMCalculator()
        self._init_session_state()
        self.apply_custom_css()
    
    def _init_session_state(self):
        """Inițializează starea sesiunii"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "patient_data" not in st.session_state:
            st.session_state.patient_data = PatientData()
        
        if "risk_calculated" not in st.session_state:
            st.session_state.risk_calculated = False
    
    def apply_custom_css(self):
        """Aplică CSS ultra-profesional pentru temă dark medicală"""
        st.markdown("""
        <style>
        /* Complete dark medical theme with better contrast */
        .stApp {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
            color: #e8eaed;
        }
        
        .main .block-container {
            background: rgba(15, 20, 25, 0.95);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid #2d3748;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        /* Headers with medical blue accent */
        h1, h2, h3 {
            color: #4fc3f7 !important;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        /* Input styling */
        .stTextInput input, .stTextArea textarea {
            background: #2d3748 !important;
            color: #e8eaed !important;
            border: 2px solid #4a5568 !important;
            border-radius: 8px;
            font-size: 16px !important;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #4fc3f7 !important;
            box-shadow: 0 0 0 2px rgba(79, 195, 247, 0.2) !important;
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(45deg, #1976d2, #42a5f5) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.75rem 2rem;
            font-size: 16px !important;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background: linear-gradient(45deg, #1565c0, #1976d2) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
        }
        
        /* Risk display cards */
        .risk-display {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            border: 2px solid #4fc3f7;
            box-shadow: 0 8px 32px rgba(79, 195, 247, 0.2);
        }
        
        .risk-low { border-color: #4caf50; }
        .risk-moderate { border-color: #ff9800; }
        .risk-high { border-color: #f44336; }
        .risk-critical { border-color: #9c27b0; }
        
        /* Data cards */
        .data-card {
            background: #2d3748;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 4px solid #4fc3f7;
        }
        
        /* Recommendations styling */
        .recommendation-item {
            background: #2d3748;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
            color: #e8eaed;
            font-size: 16px;
        }
        
        /* Chat messages */
        .chat-message {
            background: #2d3748;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #4fc3f7;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: #1a202c;
        }
        
        /* Success/Warning messages */
        .stSuccess {
            background: rgba(76, 175, 80, 0.1) !important;
            border: 1px solid #4caf50 !important;
            color: #4caf50 !important;
        }
        
        .stWarning {
            background: rgba(255, 152, 0, 0.1) !important;
            border: 1px solid #ff9800 !important;
            color: #ff9800 !important;
        }
        
        /* Text readability improvements */
        p, div, span {
            color: #e8eaed !important;
            line-height: 1.6;
        }
        
        .stMarkdown {
            color: #e8eaed !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Randează header-ul ultra-profesional"""
        st.markdown("""
        <div class="main-header">
            <h1>🧬 EpiMind AI Professional</h1>
            <p>🏥 Sistem Ultra-Avansat pentru Evaluarea Riscului IAAM</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Randează sidebar-ul cu informații și progres"""
        with st.sidebar:
            st.markdown("### 📊 Status Evaluare")
            
            data = st.session_state.patient_data
            
            # Progress pentru date critice
            critical_fields = [
                ("Spitalizare >48h", data.ore_spitalizare >= 48),
                ("Date microbiologice", data.cultura_pozitiva),
                ("Dispozitive invazive", any([data.cateter_venos_central, data.cateter_urinar, data.ventilatie_mecanica])),
                ("Parametri vitali", any([data.temperatura > 0, data.tensiune_sistolica > 0])),
                ("Analize urinare", any([data.cultura_urina_pozitiva, data.bacterii_urina > 0]))
            ]
            
            completed = sum(1 for _, status in critical_fields if status)
            progress = completed / len(critical_fields)
            
            st.progress(progress)
            st.write(f"**Progres:** {completed}/{len(critical_fields)} componente")
            
            # Detalii progres
            for field, status in critical_fields:
                icon = "✅" if status else "⏳"
                st.write(f"{icon} {field}")
            
            st.markdown("---")
            
            # Informații despre IAAM
            st.markdown("""
            ### 📚 Despre IAAM
            
            **Infecțiile Asociate Asistenței Medicale** sunt infecții care apar la pacienții spitalizați după 48-72 ore de la internare.
            
            **Factori de risc principali:**
            - Durata spitalizării
            - Dispozitive invazive
            - Microorganisme rezistente
            - Comorbidități
            - Vârsta înaintată
            
            **Prevenție:**
            - Igienă strictă
            - Utilizare rațională antibiotice
            - Îndepărtarea precoce dispozitive
            - Izolare când e necesar
            """)
    
    def render_chat(self):
        """Randează interfața de chat ultra-fluidă"""
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Afișează mesajele
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f'<div class="chat-message user-message">👤 {content}</div>', unsafe_allow_html=True)
            elif role == "assistant":
                st.markdown(f'<div class="chat-message assistant-message">🤖 {content}</div>', unsafe_allow_html=True)
            elif role == "system":
                st.markdown(f'<div class="chat-message system-message">ℹ️ {content}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_input_section(self):
        """Randează secțiunea de input ultra-responsivă"""
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Introduceți informații despre pacient:",
                placeholder="Ex: Pacient internat de 99 ore, cultura pozitivă cu Pseudomonas aeruginosa carbapenem-rezistent...",
                key="user_input_field"
            )
        
        with col2:
            send_button = st.button("📤 Trimite", use_container_width=True)
        
        # Procesează input-ul
        if send_button and user_input:
            # Adaugă mesajul utilizatorului
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Procesează cu AI
            with st.spinner("🧠 AI procesează informațiile medicale..."):
                time.sleep(0.3)  # Pentru fluiditate vizuală
                
                # Extrage date medicale
                extracted_data = self.ai.extract_medical_data(user_input)
                
                if extracted_data:
                    for key, value in extracted_data.items():
                        if hasattr(st.session_state.patient_data, key):
                            setattr(st.session_state.patient_data, key, value)
                
                # Generează răspuns AI
                context = {
                    "patient_data": asdict(st.session_state.patient_data),
                    "completion_status": self._assess_completion()
                }
                
                ai_response = self.ai.generate_response(user_input, context)
                
                # Adaugă răspunsul AI
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })
            
            st.rerun()
    
    def render_action_buttons(self):
        """Randează butoanele de acțiune"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            calc_button = st.button("🧮 Calculează Risc IAAM", use_container_width=True)
        
        with col2:
            export_button = st.button("📊 Exportă Rezultate", use_container_width=True)
        
        with col3:
            reset_button = st.button("🔄 Resetează Chat", use_container_width=True)
        
        # Procesează acțiunile
        if calc_button:
            self._calculate_risk()
        
        if export_button:
            self._export_results()
        
        if reset_button:
            self._reset_chat()
    
    def _calculate_risk(self):
        """Calculează și afișează riscul IAAM"""
        data = st.session_state.patient_data
        
        print(f"[v0] Starting risk calculation with data: {data}")
        print(f"[v0] Hospitalization hours: {data.ore_spitalizare}")
        
        if data.ore_spitalizare < 48:
            st.warning("⚠️ Riscul IAAM se evaluează doar pentru pacienții cu >48h de spitalizare.")
            print(f"[v0] Risk calculation stopped - insufficient hospitalization hours")
            return
        
        print(f"[v0] Proceeding with risk calculation...")
        
        with st.spinner("🧮 Calculez riscul IAAM cu algoritmi ultra-avansați..."):
            time.sleep(0.5)  # Pentru experiență fluidă
            
            risk_result = self.calculator.calculate_risk(data)
            
            print(f"[v0] Risk calculation completed")
            print(f"[v0] Risk result keys: {list(risk_result.keys())}")
            print(f"[v0] Risk level: {risk_result.get('nivel_risc', 'N/A')}")
            print(f"[v0] Total score: {risk_result.get('scor_total', 'N/A')}")
            print(f"[v0] Number of recommendations: {len(risk_result.get('recomandari', []))}")
            print(f"[v0] Recommendations: {risk_result.get('recomandari', [])}")
            
            st.markdown("## 🎯 REZULTAT EVALUARE RISC IAAM")
            
            # Display risk level prominently
            nivel_risc = risk_result.get("nivel_risc", "NECUNOSCUT")
            scor_total = risk_result.get("scor_total", 0)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                <h1 style="color: white; font-size: 2.5rem; margin: 0;">{nivel_risc}</h1>
                <h3 style="color: #bfdbfe; margin: 0.5rem 0;">Scor Total: {scor_total} puncte</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Display recommendations prominently
            recomandari = risk_result.get("recomandari", [])
            print(f"[v0] About to display {len(recomandari)} recommendations")
            
            if recomandari:
                st.markdown("### 🎯 RECOMANDĂRI CLINICE")
                for i, recomandare in enumerate(recomandari, 1):
                    st.markdown(f"**{i}.** {recomandare}")
                    print(f"[v0] Displayed recommendation {i}: {recomandare}")
            else:
                st.error("❌ EROARE: Nu s-au generat recomandări!")
                print(f"[v0] ERROR: No recommendations generated!")
            
            # Display components
            componente = risk_result.get("componente", {})
            if componente:
                st.markdown("### 📊 COMPONENTE SCOR")
                for componenta, scor in componente.items():
                    st.markdown(f"- **{componenta}**: {scor}")
            
            # Afișează rezultatul cu metoda originală
            self._display_risk_result(risk_result)
            
            # Adaugă în chat
            st.session_state.messages.append({
                "role": "system",
                "content": f"✅ Calculul IAAM completat: Risc {risk_result['nivel_risc']} (Scor: {risk_result['scor_total']})"
            })
            
            st.session_state.risk_calculated = True
            st.success("🎉 Evaluarea IAAM ultra-precisă a fost completată!")
            
            print(f"[v0] Risk calculation process completed successfully")
    
    def _display_risk_result(self, risk_result: Dict):
        """Afișează rezultatul riscului cu design ultra-profesional"""
        nivel_risc = risk_result["nivel_risc"]
        scor_total = risk_result["scor_total"]
        componente = risk_result["componente"]
        recomandari = risk_result["recomandari"]
        interpretare = risk_result["interpretare"]
        
        print(f"[v0] Displaying recommendations: {recomandari}")
        
        # Display principal
        st.markdown(f"""
        <div class="risk-display">
            <h2>🎯 EVALUARE RISC IAAM</h2>
            <h1 style="font-size: 3rem; margin: 1rem 0; color: #4fc3f7;">{nivel_risc}</h1>
            <h3 style="font-size: 1.5rem; color: #e8eaed;">Scor Total: {scor_total} puncte</h3>
            <p style="font-size: 1.1rem; margin-top: 1rem; color: #b0bec5;">{interpretare}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Componente și recomandări
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.markdown("### 📊 COMPONENTE SCOR")
            for componenta, scor in componente.items():
                st.markdown(f"""
                <div class="data-card">
                    <strong>{componenta}</strong><br>
                    <span style="font-size: 1.2rem; color: #4fc3f7;">{scor}</span>
                </div>
                """, unsafe_allow_html=True)
    
        with col2:
            st.markdown("### 🎯 RECOMANDĂRI CLINICE")
            
            if recomandari:
                for i, recomandare in enumerate(recomandari, 1):
                    st.markdown(f"""
                    <div class="recommendation-item">
                        <strong>{i}.</strong> {recomandare}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ Nu s-au generat recomandări!")
            
            st.markdown(f"**Total recomandări generate:** {len(recomandari)}")

        data_completeness = self._calculate_data_completeness()
        st.info(f"📊 Completitudine date: {data_completeness:.0f}%")

        # Grafic interactiv
        self._create_risk_visualization(componente, scor_total, nivel_risc)
    
    def _create_risk_visualization(self, componente: Dict, scor_total: int, nivel_risc: str):
        """Creează vizualizare interactivă a riscului"""
        # Grafic cu componentele
        labels = list(componente.keys())
        values = [int(comp.split()[0]) for comp in componente.values()]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Distribuția Scorului', 'Evoluția Riscului'),
            specs=[[{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Pie chart pentru componente
        fig.add_trace(
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker_colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
            ),
            row=1, col=1
        )
        
        # Bar chart pentru niveluri de risc
        risk_levels = ['SCĂZUT', 'MODERAT', 'RIDICAT', 'FOARTE RIDICAT', 'CRITIC']
        risk_thresholds = [20, 40, 70, 100, 150]
        colors = ['#10b981', '#f59e0b', '#ef4444', '#dc2626', '#8b5cf6']
        
        current_color = colors[risk_levels.index(nivel_risc)] if nivel_risc in risk_levels else '#6b7280'
        
        fig.add_trace(
            go.Bar(
                x=risk_levels,
                y=risk_thresholds,
                marker_color=['#10b981', '#f59e0b', '#ef4444', '#dc2626', '#8b5cf6'],
                opacity=0.7
            ),
            row=1, col=2
        )
        
        # Adaugă linia pentru scorul actual
        fig.add_hline(
            y=scor_total,
            line_dash="dash",
            line_color=current_color,
            annotation_text=f"Scor actual: {scor_total}",
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Analiza Detaliată a Riscului IAAM",
            showlegend=False,
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _assess_completion(self) -> Dict:
        """Evaluează completarea datelor"""
        data = st.session_state.patient_data
        
        return {
            "spitalizare": data.ore_spitalizare >= 48,
            "microbiologie": data.cultura_pozitiva,
            "dispozitive": any([data.cateter_venos_central, data.cateter_urinar, data.ventilatie_mecanica]),
            "vitale": any([data.temperatura > 0, data.tensiune_sistolica > 0]),
            "urinare": any([data.cultura_urina_pozitiva, data.bacterii_urina > 0])
        }
    
    def _export_results(self):
        """Exportă rezultatele în format JSON"""
        data = {
            "patient_data": asdict(st.session_state.patient_data),
            "messages": st.session_state.messages,
            "timestamp": datetime.now().isoformat()
        }
        
        st.download_button(
            label="📥 Descarcă Rezultate JSON",
            data=json.dumps(data, indent=2, ensure_ascii=False),
            file_name=f"epimind_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    def _reset_chat(self):
        """Resetează chat-ul și datele"""
        st.session_state.messages = [{
            "role": "assistant",
            "content": "👋 Chat resetat! Sunt gata să evaluez un nou pacient pentru riscul IAAM."
        }]
        st.session_state.patient_data = PatientData()
        st.session_state.risk_calculated = False
        st.rerun()
    
    def _calculate_data_completeness(self) -> int:
        """Calculează procentul de completitudine a datelor"""
        data = st.session_state.patient_data
        total_fields = 18
        completed_fields = 0
        
        if data.ore_spitalizare > 0: completed_fields += 1
        if data.varsta > 0: completed_fields += 1
        if data.gen: completed_fields += 1
        if data.diagnostic_principal: completed_fields += 1
        if data.bacterie: completed_fields += 1
        if data.rezistente: completed_fields += 1
        if data.cateter_venos_central is not None: completed_fields += 1
        if data.cateter_urinar is not None: completed_fields += 1
        if data.ventilatie_mecanica is not None: completed_fields += 1
        if data.crp > 0: completed_fields += 1
        if data.pct > 0: completed_fields += 1
        if data.leucocite > 0: completed_fields += 1
        if data.cultura_urina_pozitiva: completed_fields += 1
        if data.bacterii_urina > 0: completed_fields += 1
        if data.nitriti: completed_fields += 1
        if data.leucocit_esteraza: completed_fields += 1
        
        return int((completed_fields / total_fields) * 100)

def main():
    """Funcția principală a aplicației"""
    st.set_page_config(
        page_title="EpiMind AI Professional",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inițializează interfața
    interface = UltraProfessionalInterface()
    
    # Randează componentele
    interface.render_header()
    interface.render_sidebar()
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        interface.render_chat()
        interface.render_input_section()
    
    with col2:
        st.markdown("### ⚡ Acțiuni Rapide")
        interface.render_action_buttons()
        
        # Afișează datele curente
        st.markdown("### 📋 Date Pacient")
        try:
            data = st.session_state.patient_data
            
            if data.ore_spitalizare > 0:
                st.metric("Spitalizare", f"{data.ore_spitalizare:.0f} ore")
            
            if data.bacterie:
                st.metric("Microorganism", data.bacterie)
            
            if data.rezistente:
                st.metric("Rezistențe", f"{len(data.rezistente)} detectate")
        except Exception as e:
            st.error(f"Eroare la afișarea datelor: {str(e)}")

if __name__ == "__main__":
    main()
