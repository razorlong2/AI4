"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Brain, Calculator, MessageSquare, Activity, AlertTriangle, CheckCircle, Users, Stethoscope, Send, Loader2 } from 'lucide-react'

interface PatientData {
  age: number
  gender: string
  hospitalizationHours: number
  invasiveDevices: string[]
  antibiotics: string[]
  comorbidities: string[]
  vitalSigns: {
    temperature: number
    heartRate: number
    bloodPressure: string
    respiratoryRate: number
    oxygenSaturation: number
  }
  labResults: {
    crp: number
    procalcitonin: number
    leukocytes: number
    platelets: number
    creatinine: number
    bilirubin: number
  }
  sofaComponents: {
    respiratory: number
    coagulation: number
    liver: number
    cardiovascular: number
    cns: number
    renal: number
  }
}

interface ChatMessage {
  id: string
  type: "user" | "assistant" | "system"
  content: string
  timestamp: Date
  data?: Partial<PatientData>
}

interface RiskAssessment {
  totalScore: number
  riskLevel: "Foarte Scăzut" | "Scăzut" | "Moderat" | "Ridicat" | "Foarte Ridicat"
  riskPercentage: number
  components: {
    temporal: number
    devices: number
    antibiotics: number
    comorbidities: number
    inflammation: number
    sofa: number
  }
  recommendations: string[]
}

export default function EpiMindAI() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      type: "system",
      content:
        "Bună ziua! Sunt EpiMind AI, asistentul dumneavoastră pentru evaluarea riscului de infecții asociate îngrijirilor medicale (IAAM). Vă pot ajuta să analizați datele pacientului și să calculez riscul de infecție. Introduceți informațiile despre pacient în limba română sau engleză.",
      timestamp: new Date(),
    },
  ])
  const [inputMessage, setInputMessage] = useState("")
  const [patientData, setPatientData] = useState<Partial<PatientData>>({})
  const [riskAssessment, setRiskAssessment] = useState<RiskAssessment | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [activeTab, setActiveTab] = useState("chat")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const extractMedicalData = (text: string): Partial<PatientData> => {
    const extracted: Partial<PatientData> = {}

    const ageMatch = text.match(/(?:vârstă|age|ani|years?|varsta)[\s:]*(\d+)|(\d+)[\s]*(?:ani|years?)/i)
    if (ageMatch) extracted.age = Number.parseInt(ageMatch[1] || ageMatch[2])

    const genderMatch = text.match(/(?:sex|gender|bărbat|femeie|masculin|feminin|male|female|barbat)/i)
    if (genderMatch) {
      const gender = genderMatch[0].toLowerCase()
      extracted.gender =
        gender.includes("bărbat") || gender.includes("barbat") || gender.includes("masculin") || gender.includes("male") ? "Masculin" : "Feminin"
    }

    const text_lower = text.toLowerCase()
    
    // Pattern for "internat de X zile/ore" or "spitalizat de X zile/ore"
    const internedMatch = text_lower.match(/(?:internat|spitalizat|hospitalized)[\s\w]*?(?:de|for)[\s]*(\d+)[\s]*(?:zile|ore|days|hours)/i)
    
    // Pattern for "X zile/ore de internare/spitalizare"
    const durationMatch = text_lower.match(/(\d+)[\s]*(?:zile|ore|days|hours)[\s]*(?:de|of)?[\s]*(?:internare|spitalizare|hospitalization)/i)
    
    // Pattern for "ziua X" or "day X"
    const dayMatch = text_lower.match(/(?:ziua|day)[\s]*(\d+)/i)
    
    // Direct number extraction for hours/days
    const directHoursMatch = text_lower.match(/(\d+)[\s]*(?:ore|hours)/i)
    const directDaysMatch = text_lower.match(/(\d+)[\s]*(?:zile|days)/i)

    if (internedMatch) {
      const value = Number.parseInt(internedMatch[1])
      const unit = internedMatch[0].toLowerCase()
      extracted.hospitalizationHours = unit.includes('ore') || unit.includes('hour') ? value : value * 24
    } else if (durationMatch) {
      const value = Number.parseInt(durationMatch[1])
      const unit = durationMatch[0].toLowerCase()
      extracted.hospitalizationHours = unit.includes('ore') || unit.includes('hour') ? value : value * 24
    } else if (dayMatch) {
      extracted.hospitalizationHours = Number.parseInt(dayMatch[1]) * 24
    } else if (directHoursMatch) {
      extracted.hospitalizationHours = Number.parseInt(directHoursMatch[1])
    } else if (directDaysMatch) {
      extracted.hospitalizationHours = Number.parseInt(directDaysMatch[1]) * 24
    }

    const devices = []
    if (text.match(/(?:cateter|catheter|CVP|central|venos)/i)) devices.push("Cateter venos central")
    if (text.match(/(?:sondă|tube|intubat|ventilat|respirator|mechanical)/i)) devices.push("Intubație/Ventilație")
    if (text.match(/(?:vezical|urinar|foley|bladder)/i)) devices.push("Cateter vezical")
    if (text.match(/(?:drenaj|drain|chest tube)/i)) devices.push("Drenaj")
    if (text.match(/(?:pacemaker|stimulator)/i)) devices.push("Pacemaker")
    if (devices.length > 0) extracted.invasiveDevices = devices

    const antibiotics = []
    const abPatterns = [
      /amoxicilin[a-z]*/gi,
      /ceftriaxon[a-z]*/gi,
      /vancomicin[a-z]*/gi,
      /meropenem/gi,
      /ciprofloxacin[a-z]*/gi,
      /metronidazol/gi,
      /gentamicin[a-z]*/gi,
      /penicillin[a-z]*/gi
    ]
    
    abPatterns.forEach(pattern => {
      const matches = text.match(pattern)
      if (matches) antibiotics.push(...matches.map(ab => ab.charAt(0).toUpperCase() + ab.slice(1).toLowerCase()))
    })
    
    if (text.match(/antibiotic/i) && antibiotics.length === 0) {
      antibiotics.push("Antibioterapie nespecificată")
    }
    if (antibiotics.length > 0) extracted.antibiotics = [...new Set(antibiotics)]

    // Lab results extraction
    const labResults: any = {}
    const crpMatch = text.match(/(?:CRP|proteina C reactiva)[\s:]*(\d+(?:\.\d+)?)/i)
    if (crpMatch) labResults.crp = Number.parseFloat(crpMatch[1])

    const pctMatch = text.match(/(?:procalcitonin|PCT)[\s:]*(\d+(?:\.\d+)?)/i)
    if (pctMatch) labResults.procalcitonin = Number.parseFloat(pctMatch[1])

    const wbcMatch = text.match(/(?:leucocite|leukocytes|WBC)[\s:]*(\d+(?:\.\d+)?)/i)
    if (wbcMatch) labResults.leukocytes = Number.parseFloat(wbcMatch[1])

    if (Object.keys(labResults).length > 0) extracted.labResults = labResults

    // Vital signs
    const vitalSigns: any = {}
    const tempMatch = text.match(/(?:temperatură|temperature|febră)[\s:]*(\d+(?:\.\d+)?)/i)
    if (tempMatch) vitalSigns.temperature = Number.parseFloat(tempMatch[1])

    const hrMatch = text.match(/(?:puls|heart rate|HR)[\s:]*(\d+)/i)
    if (hrMatch) vitalSigns.heartRate = Number.parseInt(hrMatch[1])

    if (Object.keys(vitalSigns).length > 0) extracted.vitalSigns = vitalSigns

    console.log("[v0] Extracted data:", extracted) // Debug log
    return extracted
  }

  const calculateSOFAScore = (data: Partial<PatientData>): number => {
    let totalScore = 0
    const components = data.sofaComponents || {}

    // If individual components are provided, use them
    if (Object.keys(components).length > 0) {
      return Object.values(components).reduce((sum, score) => sum + (score || 0), 0)
    }

    // Otherwise, estimate from available data
    const vitals = data.vitalSigns || {}
    const labs = data.labResults || {}

    // Respiratory (based on oxygen saturation if available)
    if (vitals.oxygenSaturation) {
      if (vitals.oxygenSaturation < 85) totalScore += 4
      else if (vitals.oxygenSaturation < 90) totalScore += 3
      else if (vitals.oxygenSaturation < 95) totalScore += 2
      else if (vitals.oxygenSaturation < 98) totalScore += 1
    }

    // Coagulation (based on platelets)
    if (labs.platelets) {
      if (labs.platelets < 20) totalScore += 4
      else if (labs.platelets < 50) totalScore += 3
      else if (labs.platelets < 100) totalScore += 2
      else if (labs.platelets < 150) totalScore += 1
    }

    // Liver (based on bilirubin)
    if (labs.bilirubin) {
      if (labs.bilirubin > 12) totalScore += 4
      else if (labs.bilirubin > 6) totalScore += 3
      else if (labs.bilirubin > 2) totalScore += 2
      else if (labs.bilirubin > 1.2) totalScore += 1
    }

    // Renal (based on creatinine)
    if (labs.creatinine) {
      if (labs.creatinine > 5) totalScore += 4
      else if (labs.creatinine > 3.5) totalScore += 3
      else if (labs.creatinine > 2) totalScore += 2
      else if (labs.creatinine > 1.2) totalScore += 1
    }

    return totalScore
  }

  const calculateIAAMRisk = (data: Partial<PatientData>): RiskAssessment => {
    let totalScore = 0
    const components = {
      temporal: 0,
      devices: 0,
      antibiotics: 0,
      comorbidities: 0,
      inflammation: 0,
      sofa: 0,
    }

    // Temporal risk (hospitalization duration)
    const hours = data.hospitalizationHours || 0
    if (hours < 48) {
      components.temporal = 0
    } else if (hours < 72) {
      components.temporal = 8
    } else if (hours < 168) {
      // 1 week
      components.temporal = 15
    } else if (hours < 336) {
      // 2 weeks
      components.temporal = 25
    } else {
      components.temporal = 35
    }

    // Invasive devices risk
    const devices = data.invasiveDevices || []
    components.devices = Math.min(devices.length * 12, 40)

    // Antibiotic exposure risk
    const antibiotics = data.antibiotics || []
    if (antibiotics.length > 0) {
      components.antibiotics = Math.min(antibiotics.length * 8, 25)
    }

    // Comorbidities risk
    const comorbidities = data.comorbidities || []
    components.comorbidities = Math.min(comorbidities.length * 6, 20)

    // Inflammatory markers risk
    const labs = data.labResults || {}
    if (labs.crp && labs.crp > 10) components.inflammation += 8
    if (labs.procalcitonin && labs.procalcitonin > 0.5) components.inflammation += 12
    if (labs.leukocytes && (labs.leukocytes > 12 || labs.leukocytes < 4)) components.inflammation += 6

    // SOFA score contribution
    const sofaScore = calculateSOFAScore(data)
    components.sofa = Math.min(sofaScore * 3, 30)

    totalScore = Object.values(components).reduce((sum, score) => sum + score, 0)

    // Determine risk level and percentage
    let riskLevel: RiskAssessment["riskLevel"]
    let riskPercentage: number

    if (totalScore < 20) {
      riskLevel = "Foarte Scăzut"
      riskPercentage = Math.min(totalScore * 2, 15)
    } else if (totalScore < 40) {
      riskLevel = "Scăzut"
      riskPercentage = 15 + (totalScore - 20) * 1.5
    } else if (totalScore < 70) {
      riskLevel = "Moderat"
      riskPercentage = 45 + (totalScore - 40) * 1.2
    } else if (totalScore < 100) {
      riskLevel = "Ridicat"
      riskPercentage = 75 + (totalScore - 70) * 0.8
    } else {
      riskLevel = "Foarte Ridicat"
      riskPercentage = Math.min(95, 85 + (totalScore - 100) * 0.1)
    }

    // Generate recommendations
    const recommendations = []
    if (components.temporal > 20) recommendations.push("Monitorizare intensivă pentru infecții nosocomiale")
    if (components.devices > 15) recommendations.push("Evaluare zilnică a necesității dispozitivelor invazive")
    if (components.antibiotics > 10) recommendations.push("Revizuire terapie antibiotică și considerare de-escalare")
    if (components.inflammation > 15) recommendations.push("Monitorizare markeri inflamatori și hemocultură")
    if (sofaScore > 6) recommendations.push("Evaluare pentru terapie intensivă și suport organ")
    if (riskPercentage > 60) recommendations.push("Implementare măsuri stricte de control infecții")

    return {
      totalScore,
      riskLevel,
      riskPercentage,
      components,
      recommendations,
    }
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    setIsProcessing(true)

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: "user",
      content: inputMessage,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])

    const extractedData = extractMedicalData(inputMessage)
    const updatedPatientData = { ...patientData, ...extractedData }
    setPatientData(updatedPatientData)

    let aiResponse = ""
    const extractedFields = Object.keys(extractedData)

    if (extractedFields.length > 0) {
      aiResponse = `✅ **Am extras următoarele informații medicale:**\n\n`

      if (extractedData.age) aiResponse += `🧑 **Vârstă:** ${extractedData.age} ani\n`
      if (extractedData.gender) aiResponse += `👤 **Sex:** ${extractedData.gender}\n`
      if (extractedData.hospitalizationHours) {
        const days = Math.floor(extractedData.hospitalizationHours / 24)
        const hours = extractedData.hospitalizationHours % 24
        aiResponse += `🏥 **Durată spitalizare:** ${days} zile și ${hours} ore (total: ${extractedData.hospitalizationHours}h)\n`
      }
      if (extractedData.invasiveDevices?.length) {
        aiResponse += `🔌 **Dispozitive invazive:** ${extractedData.invasiveDevices.join(", ")}\n`
      }
      if (extractedData.antibiotics?.length) {
        aiResponse += `💊 **Antibiotice:** ${extractedData.antibiotics.join(", ")}\n`
      }
      if (extractedData.labResults) {
        aiResponse += `🧪 **Rezultate laborator:**\n`
        if (extractedData.labResults.crp) aiResponse += `  • CRP: ${extractedData.labResults.crp} mg/L\n`
        if (extractedData.labResults.procalcitonin)
          aiResponse += `  • Procalcitonină: ${extractedData.labResults.procalcitonin} ng/mL\n`
        if (extractedData.labResults.leukocytes)
          aiResponse += `  • Leucocite: ${extractedData.labResults.leukocytes} × 10³/μL\n`
      }

      aiResponse += `\n🎯 **Următorul pas:** Doresc să calculez riscul IAAM cu aceste date sau aveți informații suplimentare de adăugat?`
      
      if (extractedData.hospitalizationHours && extractedData.hospitalizationHours >= 48) {
        aiResponse += `\n\n💡 **Sugestie:** Aveți suficiente date pentru o evaluare preliminară. Apăsați "Calculează Risc" pentru rezultate.`
      }
    } else {
      aiResponse = `❌ **Nu am putut extrage informații medicale specifice** din mesajul dumneavoastră.\n\n📝 **Vă rog să furnizați detalii precum:**\n• Vârsta pacientului\n• Durata spitalizării (ex: "internat de 5 zile" sau "99 ore")\n• Dispozitive invazive (cateter, sondă, etc.)\n• Rezultate laborator (CRP, leucocite, etc.)\n• Alte informații clinice relevante\n\n💬 **Exemplu:** "Pacient bărbat, 65 ani, internat de 99 ore cu cateter venos central și CRP 45"`
    }

    const assistantMessage: ChatMessage = {
      id: (Date.now() + 1).toString(),
      type: "assistant",
      content: aiResponse,
      timestamp: new Date(),
      data: extractedData,
    }

    setTimeout(() => {
      setMessages((prev) => [...prev, assistantMessage])
      setIsProcessing(false)
    }, 500)
    
    setInputMessage("")
  }

  const handleCalculateRisk = () => {
    if (!patientData.hospitalizationHours || patientData.hospitalizationHours < 48) {
      const warningMessage: ChatMessage = {
        id: Date.now().toString(),
        type: "system",
        content:
          "Atenție: Riscul IAAM se evaluează de obicei după minimum 48 de ore de spitalizare. Datele actuale indică o durată mai mică.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, warningMessage])
    }

    const assessment = calculateIAAMRisk(patientData)
    setRiskAssessment(assessment)
    setActiveTab("results")

    const resultMessage: ChatMessage = {
      id: Date.now().toString(),
      type: "system",
      content: `Evaluarea IAAM completă! Risc: ${assessment.riskLevel} (${assessment.riskPercentage.toFixed(1)}%). Consultați tab-ul "Rezultate" pentru detalii complete.`,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, resultMessage])
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case "Foarte Scăzut":
        return "text-green-600"
      case "Scăzut":
        return "text-blue-600"
      case "Moderat":
        return "text-yellow-600"
      case "Ridicat":
        return "text-orange-600"
      case "Foarte Ridicat":
        return "text-red-600"
      default:
        return "text-gray-600"
    }
  }

  const getRiskBadgeVariant = (level: string) => {
    switch (level) {
      case "Foarte Scăzut":
        return "default"
      case "Scăzut":
        return "secondary"
      case "Moderat":
        return "outline"
      case "Ridicat":
        return "destructive"
      case "Foarte Ridicat":
        return "destructive"
      default:
        return "default"
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="container mx-auto px-4 py-6">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-blue-600 rounded-xl shadow-lg">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold text-white">EpiMind AI</h1>
          </div>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            Sistem avansat de evaluare a riscului de infecții asociate îngrijirilor medicale (IAAM) cu inteligență
            artificială conversațională
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-6 bg-gray-800 border-gray-700">
            <TabsTrigger value="chat" className="flex items-center gap-2 data-[state=active]:bg-gray-700 data-[state=active]:text-white">
              <MessageSquare className="h-4 w-4" />
              Chat AI
            </TabsTrigger>
            <TabsTrigger value="data" className="flex items-center gap-2 data-[state=active]:bg-gray-700 data-[state=active]:text-white">
              <Users className="h-4 w-4" />
              Date Pacient
            </TabsTrigger>
            <TabsTrigger value="calculate" className="flex items-center gap-2 data-[state=active]:bg-gray-700 data-[state=active]:text-white">
              <Calculator className="h-4 w-4" />
              Calcul Risc
            </TabsTrigger>
            <TabsTrigger value="results" className="flex items-center gap-2 data-[state=active]:bg-gray-700 data-[state=active]:text-white">
              <Activity className="h-4 w-4" />
              Rezultate
            </TabsTrigger>
          </TabsList>

          {/* Chat Tab */}
          <TabsContent value="chat">
            <Card className="h-[600px] flex flex-col bg-gray-800 border-gray-700">
              <CardHeader className="border-b border-gray-700">
                <CardTitle className="flex items-center gap-2 text-white">
                  <MessageSquare className="h-5 w-5" />
                  Conversație cu EpiMind AI
                </CardTitle>
                <CardDescription className="text-gray-400">Introduceți informațiile despre pacient în limba română sau engleză</CardDescription>
              </CardHeader>
              <CardContent className="flex-1 flex flex-col p-0">
                <ScrollArea className="flex-1 p-4">
                  {messages.map((message) => (
                    <div key={message.id} className="mb-4">
                      <div className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
                        <div
                          className={`max-w-[80%] p-4 rounded-xl shadow-sm ${
                            message.type === "user"
                              ? "bg-blue-600 text-white"
                              : message.type === "system"
                                ? "bg-yellow-900/30 text-yellow-200 border border-yellow-800"
                                : "bg-gray-700 text-gray-100 border border-gray-600"
                          }`}
                        >
                          <div className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</div>
                          <div className="text-xs opacity-70 mt-2">{message.timestamp.toLocaleTimeString()}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                  {isProcessing && (
                    <div className="flex justify-start mb-4">
                      <div className="bg-gray-700 text-gray-100 border border-gray-600 p-4 rounded-xl flex items-center gap-2">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span className="text-sm">EpiMind AI procesează...</span>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </ScrollArea>

                <div className="p-4 border-t border-gray-700 bg-gray-800/50">
                  <div className="flex gap-3">
                    <Textarea
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      placeholder="Descrieți cazul pacientului (ex: Pacient bărbat, 65 ani, internat de 99 ore cu cateter venos central...)"
                      className="flex-1 bg-gray-700 border-gray-600 text-white placeholder-gray-400 resize-none focus:ring-blue-500 focus:border-blue-500"
                      rows={3}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                          e.preventDefault()
                          handleSendMessage()
                        }
                      }}
                    />
                    <Button
                      onClick={handleSendMessage}
                      disabled={isProcessing || !inputMessage.trim()}
                      className="self-end bg-blue-600 hover:bg-blue-700 text-white px-6"
                      size="lg"
                    >
                      {isProcessing ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Send className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                  <div className="text-xs text-gray-500 mt-2">
                    Apăsați Enter pentru a trimite, Shift+Enter pentru linie nouă
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Patient Data Tab */}
          <TabsContent value="data">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white">
                    <Users className="h-5 w-5" />
                    Informații Demografice
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-400">Vârstă</label>
                      <Input
                        type="number"
                        value={patientData.age || ""}
                        onChange={(e) =>
                          setPatientData((prev) => ({ ...prev, age: Number.parseInt(e.target.value) || 0 }))
                        }
                        placeholder="ani"
                        className="bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-400">Sex</label>
                      <Input
                        value={patientData.gender || ""}
                        onChange={(e) => setPatientData((prev) => ({ ...prev, gender: e.target.value }))}
                        placeholder="Masculin/Feminin"
                        className="bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-400">Ore spitalizare</label>
                    <Input
                      type="number"
                      value={patientData.hospitalizationHours || ""}
                      onChange={(e) =>
                        setPatientData((prev) => ({
                          ...prev,
                          hospitalizationHours: Number.parseInt(e.target.value) || 0,
                        }))
                      }
                      placeholder="ore"
                      className="bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white">
                    <Stethoscope className="h-5 w-5" />
                    Dispozitive și Tratamente
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-400">Dispozitive invazive</label>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {patientData.invasiveDevices?.map((device, index) => (
                        <Badge key={index} variant="secondary" className="bg-gray-700 text-gray-100 border border-gray-600">
                          {device}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-400">Antibiotice</label>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {patientData.antibiotics?.map((antibiotic, index) => (
                        <Badge key={index} variant="outline" className="bg-gray-700 text-gray-100 border border-gray-600">
                          {antibiotic}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-white">Semne Vitale</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-400">Temperatură (°C)</label>
                      <Input
                        type="number"
                        step="0.1"
                        value={patientData.vitalSigns?.temperature || ""}
                        onChange={(e) =>
                          setPatientData((prev) => ({
                            ...prev,
                            vitalSigns: { ...prev.vitalSigns, temperature: Number.parseFloat(e.target.value) || 0 },
                          }))
                        }
                        className="bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-400">Puls (bpm)</label>
                      <Input
                        type="number"
                        value={patientData.vitalSigns?.heartRate || ""}
                        onChange={(e) =>
                          setPatientData((prev) => ({
                            ...prev,
                            vitalSigns: { ...prev.vitalSigns, heartRate: Number.parseInt(e.target.value) || 0 },
                          }))
                        }
                        className="bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-white">Rezultate Laborator</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-400">CRP (mg/L)</label>
                      <Input
                        type="number"
                        step="0.1"
                        value={patientData.labResults?.crp || ""}
                        onChange={(e) =>
                          setPatientData((prev) => ({
                            ...prev,
                            labResults: { ...prev.labResults, crp: Number.parseFloat(e.target.value) || 0 },
                          }))
                        }
                        className="bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-400">Procalcitonină (ng/mL)</label>
                      <Input
                        type="number"
                        step="0.01"
                        value={patientData.labResults?.procalcitonin || ""}
                        onChange={(e) =>
                          setPatientData((prev) => ({
                            ...prev,
                            labResults: { ...prev.labResults, procalcitonin: Number.parseFloat(e.target.value) || 0 },
                          }))
                        }
                        className="bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-400">Leucocite (× 10³/μL)</label>
                    <Input
                      type="number"
                      step="0.1"
                      value={patientData.labResults?.leukocytes || ""}
                      onChange={(e) =>
                        setPatientData((prev) => ({
                          ...prev,
                          labResults: { ...prev.labResults, leukocytes: Number.parseFloat(e.target.value) || 0 },
                        }))
                      }
                      className="bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Calculate Risk Tab */}
          <TabsContent value="calculate">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader className="border-b border-gray-700">
                <CardTitle className="flex items-center gap-2 text-white">
                  <Calculator className="h-5 w-5" />
                  Calculare Risc IAAM
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Evaluare completă a riscului de infecții asociate îngrijirilor medicale
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Data Summary */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <div className="text-sm text-blue-600 dark:text-blue-400">Pacient</div>
                    <div className="font-semibold">
                      {patientData.age ? `${patientData.age} ani` : "Necunoscut"}, {patientData.gender || "Necunoscut"}
                    </div>
                  </div>
                  <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <div className="text-sm text-green-600 dark:text-green-400">Spitalizare</div>
                    <div className="font-semibold">
                      {patientData.hospitalizationHours
                        ? `${Math.floor(patientData.hospitalizationHours / 24)}z ${patientData.hospitalizationHours % 24}h`
                        : "Necunoscut"}
                    </div>
                  </div>
                  <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                    <div className="text-sm text-purple-600 dark:text-purple-400">Dispozitive</div>
                    <div className="font-semibold">{patientData.invasiveDevices?.length || 0} active</div>
                  </div>
                </div>

                {/* Validation Alerts */}
                {(!patientData.hospitalizationHours || patientData.hospitalizationHours < 48) && (
                  <Alert className="bg-gray-700 border border-gray-600 text-gray-100">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertDescription>
                      Atenție: Riscul IAAM se evaluează de obicei după minimum 48 de ore de spitalizare.
                    </AlertDescription>
                  </Alert>
                )}

                {Object.keys(patientData).length < 3 && (
                  <Alert className="bg-gray-700 border border-gray-600 text-gray-100">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertDescription>
                      Pentru o evaluare precisă, vă recomandăm să furnizați mai multe date despre pacient.
                    </AlertDescription>
                  </Alert>
                )}

                <Button
                  onClick={handleCalculateRisk}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                  size="lg"
                  disabled={!patientData.hospitalizationHours}
                >
                  <Calculator className="h-5 w-5 mr-2" />
                  Calculează Risc IAAM
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Results Tab */}
          <TabsContent value="results">
            {riskAssessment ? (
              <div className="space-y-6">
                {/* Risk Overview */}
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader className="border-b border-gray-700">
                    <CardTitle className="flex items-center gap-2 text-white">
                      <Activity className="h-5 w-5" />
                      Evaluare Risc IAAM
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-center py-12">
                    <div className={`text-4xl font-bold mb-2 ${getRiskColor(riskAssessment.riskLevel)}`}>
                      {riskAssessment.riskPercentage.toFixed(1)}%
                    </div>
                    <Badge variant={getRiskBadgeVariant(riskAssessment.riskLevel)} className="text-lg px-4 py-2">
                      Risc {riskAssessment.riskLevel}
                    </Badge>
                    <div className="mt-4">
                      <Progress value={riskAssessment.riskPercentage} className="h-3 bg-gray-700 text-gray-100" />
                    </div>
                  </CardContent>
                </Card>

                {/* Risk Components */}
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader className="border-b border-gray-700">
                    <CardTitle className="text-white">Componente Risc</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {Object.entries(riskAssessment.components).map(([key, value]) => {
                        const labels = {
                          temporal: "Risc Temporal",
                          devices: "Dispozitive Invazive",
                          antibiotics: "Expunere Antibiotice",
                          comorbidities: "Comorbidități",
                          inflammation: "Markeri Inflamatori",
                          sofa: "Scor SOFA",
                        }
                        return (
                          <div key={key} className="flex items-center justify-between">
                            <span className="font-medium text-gray-400">{labels[key as keyof typeof labels]}</span>
                            <div className="flex items-center gap-2">
                              <Progress value={(value / 40) * 100} className="w-24 h-2 bg-gray-700 text-gray-100" />
                              <span className="font-bold w-8 text-right text-gray-100">{value}</span>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                    <Separator className="my-4 bg-gray-700" />
                    <div className="flex items-center justify-between text-lg font-bold text-gray-100">
                      <span>Total Scor</span>
                      <span>{riskAssessment.totalScore}</span>
                    </div>
                  </CardContent>
                </Card>

                {/* Recommendations */}
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader className="border-b border-gray-700">
                    <CardTitle className="flex items-center gap-2 text-white">
                      <CheckCircle className="h-5 w-5" />
                      Recomandări Clinice
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {riskAssessment.recommendations.map((recommendation, index) => (
                        <div key={index} className="flex items-start gap-3">
                          <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-100">{recommendation}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            ) : (
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="text-center py-12">
                  <Activity className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2 text-gray-100">Nicio evaluare disponibilă</h3>
                  <p className="text-gray-400 mb-4">
                    Calculați riscul IAAM pentru a vedea rezultatele aici.
                  </p>
                  <Button onClick={() => setActiveTab("calculate")} className="bg-blue-600 hover:bg-blue-700 text-white">
                    Calculează Risc
                  </Button>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
