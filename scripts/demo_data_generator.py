#!/usr/bin/env python3
"""
Generator de date demo pentru EpiMind AI
Creează scenarii realiste de pacienți pentru testare
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
from epimind_ai_enhanced import PatientData

class DemoDataGenerator:
    """Generator de date demo pentru pacienți"""
    
    def __init__(self):
        self.bacteria_list = [
            "Escherichia coli", "Klebsiella pneumoniae", "Pseudomonas aeruginosa",
            "Acinetobacter baumannii", "Staphylococcus aureus", "Enterococcus faecium",
            "Candida auris", "Clostridioides difficile"
        ]
        
        self.resistance_patterns = [
            ["ESBL"], ["MRSA"], ["VRE"], ["CRE", "KPC"], 
            ["ESBL", "CRE"], ["XDR"], ["PDR"], ["NDM", "OXA"]
        ]
        
        self.device_combinations = [
            {"cateter_central": True, "cateter_central_days": random.randint(2, 14)},
            {"ventilatie_mecanica": True, "ventilatie_mecanica_days": random.randint(1, 10)},
            {"sonda_urinara": True, "sonda_urinara_days": random.randint(3, 21)},
            {"traheostomie": True, "traheostomie_days": random.randint(5, 30)},
            {"drenaj": True, "drenaj_days": random.randint(1, 7)},
            {"peg": True, "peg_days": random.randint(7, 60)}
        ]
    
    def generate_low_risk_patient(self) -> PatientData:
        """Generează pacient cu risc scăzut"""
        return PatientData(
            ore_spitalizare=random.randint(48, 72),
            temperatura=random.uniform(36.0, 37.2),
            frecventa_cardiaca=random.randint(60, 90),
            tas=random.randint(110, 140),
            tad=random.randint(70, 90),
            frecventa_respiratorie=random.randint(12, 20),
            glasgow=15,
            leucocite=random.uniform(4.0, 10.0),
            crp=random.uniform(1.0, 15.0),
            procalcitonina=random.uniform(0.05, 0.2),
            creatinina=random.uniform(0.8, 1.2),
            bilirubina=random.uniform(0.3, 1.1),
            trombocite=random.uniform(150, 400)
        )
    
    def generate_moderate_risk_patient(self) -> PatientData:
        """Generează pacient cu risc moderat"""
        patient = PatientData(
            ore_spitalizare=random.randint(72, 168),
            temperatura=random.uniform(37.5, 38.2),
            frecventa_cardiaca=random.randint(85, 105),
            tas=random.randint(95, 120),
            tad=random.randint(60, 80),
            frecventa_respiratorie=random.randint(18, 24),
            glasgow=random.randint(13, 15),
            leucocite=random.uniform(10.0, 15.0),
            crp=random.uniform(20.0, 80.0),
            procalcitonina=random.uniform(0.3, 1.0),
            creatinina=random.uniform(1.0, 1.8),
            bilirubina=random.uniform(1.0, 2.5),
            trombocite=random.uniform(100, 200)
        )
        
        # Adaugă 1-2 dispozitive
        devices = random.sample(self.device_combinations, random.randint(1, 2))
        for device in devices:
            for key, value in device.items():
                setattr(patient, key, value)
        
        return patient
    
    def generate_high_risk_patient(self) -> PatientData:
        """Generează pacient cu risc înalt"""
        patient = PatientData(
            ore_spitalizare=random.randint(168, 336),
            temperatura=random.uniform(38.5, 39.5),
            frecventa_cardiaca=random.randint(100, 130),
            tas=random.randint(80, 100),
            tad=random.randint(50, 70),
            frecventa_respiratorie=random.randint(22, 30),
            glasgow=random.randint(10, 14),
            leucocite=random.uniform(15.0, 25.0),
            crp=random.uniform(100.0, 200.0),
            procalcitonina=random.uniform(2.0, 8.0),
            creatinina=random.uniform(1.5, 3.0),
            bilirubina=random.uniform(2.0, 6.0),
            trombocite=random.uniform(50, 120),
            hipotensiune=random.choice([True, False]),
            vasopresoare=random.choice([True, False])
        )
        
        # Adaugă 2-4 dispozitive
        devices = random.sample(self.device_combinations, random.randint(2, 4))
        for device in devices:
            for key, value in device.items():
                setattr(patient, key, value)
        
        # Posibilă cultură pozitivă
        if random.random() < 0.7:
            patient.cultura_pozitiva = True
            patient.bacterie = random.choice(self.bacteria_list)
            if random.random() < 0.5:
                patient.rezistente = random.choice(self.resistance_patterns)
        
        return patient
    
    def generate_critical_risk_patient(self) -> PatientData:
        """Generează pacient cu risc critic"""
        patient = PatientData(
            ore_spitalizare=random.randint(336, 720),
            temperatura=random.uniform(39.0, 41.0),
            frecventa_cardiaca=random.randint(120, 160),
            tas=random.randint(60, 85),
            tad=random.randint(35, 55),
            frecventa_respiratorie=random.randint(25, 40),
            glasgow=random.randint(3, 12),
            leucocite=random.uniform(20.0, 40.0),
            crp=random.uniform(200.0, 400.0),
            procalcitonina=random.uniform(8.0, 50.0),
            creatinina=random.uniform(3.0, 8.0),
            bilirubina=random.uniform(6.0, 20.0),
            trombocite=random.uniform(20, 80),
            pao2_fio2=random.uniform(80, 200),
            hipotensiune=True,
            vasopresoare=True
        )
        
        # Adaugă 3-5 dispozitive
        devices = random.sample(self.device_combinations, random.randint(3, 5))
        for device in devices:
            for key, value in device.items():
                # Mărește durata pentru pacienții critici
                if key.endswith('_days'):
                    value = min(value * 2, 30)
                setattr(patient, key, value)
        
        # Cultură pozitivă cu rezistențe multiple
        patient.cultura_pozitiva = True
        patient.bacterie = random.choice(self.bacteria_list)
        patient.rezistente = random.choice(self.resistance_patterns[-3:])  # rezistențe severe
        
        return patient
    
    def generate_demo_dataset(self, count_per_category: int = 5) -> List[Dict]:
        """Generează un set complet de date demo"""
        patients = []
        
        categories = [
            ("low_risk", self.generate_low_risk_patient),
            ("moderate_risk", self.generate_moderate_risk_patient),
            ("high_risk", self.generate_high_risk_patient),
            ("critical_risk", self.generate_critical_risk_patient)
        ]
        
        for category, generator in categories:
            for i in range(count_per_category):
                patient = generator()
                patient_dict = {
                    "category": category,
                    "patient_id": patient.patient_id,
                    "timestamp": patient.timestamp.isoformat(),
                    "data": {
                        k: v for k, v in patient.__dict__.items() 
                        if k not in ['patient_id', 'timestamp']
                    }
                }
                patients.append(patient_dict)
        
        return patients
    
    def generate_realistic_scenarios(self) -> List[Dict]:
        """Generează scenarii realiste de caz"""
        scenarios = [
            {
                "name": "Pacient post-operator cu complicații",
                "description": "Pacient după chirurgie abdominală cu infecție de plagă",
                "patient": PatientData(
                    ore_spitalizare=96,
                    cateter_central=True,
                    cateter_central_days=4,
                    sonda_urinara=True,
                    sonda_urinara_days=4,
                    drenaj=True,
                    drenaj_days=3,
                    temperatura=38.7,
                    frecventa_cardiaca=95,
                    tas=105,
                    leucocite=13.5,
                    crp=85.0,
                    procalcitonina=1.2,
                    cultura_pozitiva=True,
                    bacterie="Escherichia coli",
                    rezistente=["ESBL"]
                )
            },
            {
                "name": "Pacient ATI cu sepsă severă",
                "description": "Pacient în terapie intensivă cu sepsă și disfuncție multiplă de organe",
                "patient": PatientData(
                    ore_spitalizare=240,
                    cateter_central=True,
                    cateter_central_days=10,
                    ventilatie_mecanica=True,
                    ventilatie_mecanica_days=8,
                    sonda_urinara=True,
                    sonda_urinara_days=10,
                    temperatura=39.8,
                    frecventa_cardiaca=125,
                    tas=75,
                    frecventa_respiratorie=28,
                    glasgow=8,
                    leucocite=22.0,
                    crp=280.0,
                    procalcitonina=15.5,
                    creatinina=2.8,
                    bilirubina=4.2,
                    trombocite=65,
                    pao2_fio2=150,
                    hipotensiune=True,
                    vasopresoare=True,
                    cultura_pozitiva=True,
                    bacterie="Pseudomonas aeruginosa",
                    rezistente=["XDR"]
                )
            },
            {
                "name": "Pacient cu spitalizare prelungită",
                "description": "Pacient cu multiple comorbidități și spitalizare de lungă durată",
                "patient": PatientData(
                    ore_spitalizare=480,
                    cateter_central=True,
                    cateter_central_days=20,
                    traheostomie=True,
                    traheostomie_days=15,
                    peg=True,
                    peg_days=18,
                    sonda_urinara=True,
                    sonda_urinara_days=20,
                    temperatura=37.8,
                    frecventa_cardiaca=88,
                    tas=110,
                    glasgow=12,
                    leucocite=11.0,
                    crp=45.0,
                    procalcitonina=0.8,
                    cultura_pozitiva=True,
                    bacterie="Acinetobacter baumannii",
                    rezistente=["CRE", "KPC"]
                )
            }
        ]
        
        # Convertește în format serializabil
        serializable_scenarios = []
        for scenario in scenarios:
            patient_dict = scenario["patient"].__dict__.copy()
            if 'timestamp' in patient_dict:
                patient_dict['timestamp'] = patient_dict['timestamp'].isoformat()
            
            serializable_scenarios.append({
                "name": scenario["name"],
                "description": scenario["description"],
                "patient_data": patient_dict
            })
        
        return serializable_scenarios

def main():
    """Generează și salvează datele demo"""
    print("🎭 Generez date demo pentru EpiMind AI...")
    
    generator = DemoDataGenerator()
    
    # Generează dataset complet
    print("📊 Generez dataset complet...")
    dataset = generator.generate_demo_dataset(count_per_category=10)
    
    with open("demo_patients_dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generat dataset cu {len(dataset)} pacienți")
    
    # Generează scenarii realiste
    print("🎬 Generez scenarii realiste...")
    scenarios = generator.generate_realistic_scenarios()
    
    with open("realistic_scenarios.json", "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generat {len(scenarios)} scenarii realiste")
    
    # Statistici
    categories = {}
    for patient in dataset:
        cat = patient["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📈 Statistici dataset:")
    for category, count in categories.items():
        print(f"   - {category}: {count} pacienți")
    
    print("\n🎉 Datele demo au fost generate cu succes!")
    print("📁 Fișiere create:")
    print("   - demo_patients_dataset.json")
    print("   - realistic_scenarios.json")

if __name__ == "__main__":
    main()
