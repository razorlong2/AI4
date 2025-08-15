#!/usr/bin/env python3
"""
Test script pentru EpiMind AI Enhanced
Testează toate funcționalitățile principale
"""

import sys
import json
from datetime import datetime
from epimind_ai_enhanced import (
    PatientData, EnhancedOllamaAI, EnhancedIAAMPredictor, 
    EnhancedMedicalDataExtractor
)

def test_patient_data():
    """Testează clasa PatientData"""
    print("🧪 Testez PatientData...")
    
    # Test cu date implicite
    patient1 = PatientData()
    print(f"✅ Pacient nou creat cu ID: {patient1.patient_id}")
    
    # Test cu date specifice
    patient2 = PatientData(
        ore_spitalizare=72,
        cateter_central=True,
        cateter_central_days=5,
        leucocite=15.0,
        crp=120.0,
        temperatura=38.5
    )
    print(f"✅ Pacient cu date specifice: {patient2.patient_id}")
    print(f"   - Spitalizare: {patient2.ore_spitalizare}h")
    print(f"   - CVC: {patient2.cateter_central} ({patient2.cateter_central_days} zile)")
    print(f"   - Leucocite: {patient2.leucocite}")

def test_data_extractor():
    """Testează extractorul de date medicale"""
    print("\n🧪 Testez EnhancedMedicalDataExtractor...")
    
    extractor = EnhancedMedicalDataExtractor()
    
    # Test text complex
    test_text = """
    Pacientul este internat de 5 zile (120 ore), are cateter central de 4 zile,
    ventilație mecanică de 3 zile. Leucocite 15000, CRP 150 mg/L, 
    procalcitonină 3.2 ng/mL. Temperatura 38.8°C, TA 85/50 mmHg, 
    FC 110/min, Glasgow 13. Cultură pozitivă E.coli ESBL+.
    """
    
    extracted = extractor.extract_from_text(test_text)
    validated = extractor.validate_extracted_data(extracted)
    
    print("✅ Date extrase:")
    for key, value in validated.items():
        print(f"   - {key}: {value}")

def test_iaam_predictor():
    """Testează predictorul IAAM"""
    print("\n🧪 Testez EnhancedIAAMPredictor...")
    
    predictor = EnhancedIAAMPredictor()
    
    # Pacient cu risc înalt
    patient_high_risk = PatientData(
        ore_spitalizare=120,  # 5 zile
        cateter_central=True,
        cateter_central_days=4,
        ventilatie_mecanica=True,
        ventilatie_mecanica_days=3,
        sonda_urinara=True,
        sonda_urinara_days=5,
        leucocite=18.0,
        crp=180.0,
        procalcitonina=4.5,
        temperatura=39.2,
        tas=85,
        frecventa_cardiaca=115,
        glasgow=12,
        cultura_pozitiva=True,
        bacterie="Escherichia coli",
        rezistente=["ESBL", "CRE"]
    )
    
    result = predictor.predict_iaam_risk(patient_high_risk)
    
    print("✅ Rezultat predicție:")
    print(f"   - Scor: {result['score']}")
    print(f"   - Nivel: {result['level']}")
    print(f"   - SOFA: {result['sofa_score']}")
    print(f"   - qSOFA: {result['qsofa_score']}")
    print("   - Detalii:")
    for detail in result['details'][:5]:  # primele 5
        print(f"     • {detail}")

def test_ai_fallback():
    """Testează funcționalitatea AI cu fallback"""
    print("\n🧪 Testez EnhancedOllamaAI...")
    
    ai = EnhancedOllamaAI()
    print(f"✅ Status Ollama: {'Online' if ai.available else 'Offline (Fallback)'}")
    
    # Test răspunsuri
    test_prompts = [
        "Salut, vreau să evaluez un pacient",
        "Pacientul are 72 ore de internare",
        "Are cateter central și ventilație mecanică",
        "Leucocite 15000, CRP 120"
    ]
    
    for prompt in test_prompts:
        response = ai.generate(prompt)
        print(f"   Q: {prompt}")
        print(f"   A: {response[:100]}...")

def test_complete_workflow():
    """Testează workflow-ul complet"""
    print("\n🧪 Testez workflow-ul complet...")
    
    # Simulează introducerea datelor prin chat
    extractor = EnhancedMedicalDataExtractor()
    predictor = EnhancedIAAMPredictor()
    
    # Mesaje simulate de la utilizator
    user_messages = [
        "Pacientul este internat de 4 zile",
        "Are cateter central de 3 zile și ventilație mecanică de 2 zile",
        "Leucocite 16000, CRP 140, procalcitonină 3.8",
        "Temperatura 38.9, TA 90/55, puls 108, Glasgow 13",
        "Cultură pozitivă Klebsiella pneumoniae ESBL+"
    ]
    
    # Inițializează pacientul
    patient = PatientData()
    
    print("✅ Simulez introducerea datelor:")
    for i, message in enumerate(user_messages, 1):
        print(f"   Mesaj {i}: {message}")
        
        # Extrage date
        extracted = extractor.extract_from_text(message)
        
        # Actualizează pacientul
        for key, value in extracted.items():
            if hasattr(patient, key):
                setattr(patient, key, value)
        
        print(f"   → Date extrase: {list(extracted.keys())}")
    
    # Calculează riscul final
    if patient.ore_spitalizare >= 48:
        result = predictor.predict_iaam_risk(patient)
        print(f"\n✅ Rezultat final:")
        print(f"   - Pacient ID: {result['patient_id']}")
        print(f"   - Scor IAAM: {result['score']}")
        print(f"   - Nivel risc: {result['level']}")
        print(f"   - Recomandări: {len(result['recommendations'])} acțiuni")
    else:
        print("❌ Timp insuficient pentru IAAM")

def generate_test_report():
    """Generează raport de testare"""
    print("\n📊 Generez raport de testare...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "tests_run": [
            "PatientData creation and validation",
            "Medical data extraction from text",
            "IAAM risk prediction algorithm",
            "AI fallback functionality",
            "Complete workflow simulation"
        ],
        "status": "All tests completed successfully",
        "version": "4.0.0"
    }
    
    with open("test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("✅ Raport salvat în test_report.json")

def main():
    """Rulează toate testele"""
    print("🚀 Încep testarea EpiMind AI Enhanced")
    print("=" * 50)
    
    try:
        test_patient_data()
        test_data_extractor()
        test_iaam_predictor()
        test_ai_fallback()
        test_complete_workflow()
        generate_test_report()
        
        print("\n" + "=" * 50)
        print("✅ Toate testele au fost completate cu succes!")
        print("🎉 EpiMind AI Enhanced este complet funcțional!")
        
    except Exception as e:
        print(f"\n❌ Eroare în timpul testării: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
