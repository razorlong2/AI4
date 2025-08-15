"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import {
  ChevronLeft,
  ChevronRight,
  Brain,
  Calculator,
  Activity,
  AlertTriangle,
  Stethoscope,
  TrendingUp,
  Shield,
  Target,
  CheckCircle,
  Clock,
  Zap,
} from "lucide-react"

interface FlipchartSlide {
  id: number
  title: string
  content: React.ReactNode
}

export default function MedicalAlgorithmFlipchart() {
  const [currentSlide, setCurrentSlide] = useState(0)

  const slides: FlipchartSlide[] = [
    {
      id: 1,
      title: "EpiMind AI - Algoritm de Decizie pentru Evaluarea Riscului IAAM",
      content: (
        <div className="text-center space-y-8">
          <div className="flex items-center justify-center gap-4 mb-8">
            <div className="p-4 bg-blue-600 rounded-2xl shadow-lg">
              <Brain className="h-12 w-12 text-white" />
            </div>
            <h1 className="text-5xl font-bold text-white">EpiMind AI</h1>
          </div>

          <div className="bg-gray-800 rounded-xl p-8 border border-gray-700">
            <h2 className="text-3xl font-semibold text-blue-400 mb-6">
              Sistem Inteligent de Evaluare a Riscului de Infecții Asociate Îngrijirilor Medicale
            </h2>
            <div className="grid grid-cols-2 gap-6 text-left">
              <div className="space-y-3">
                <h3 className="text-xl font-semibold text-green-400">🎯 Obiective:</h3>
                <ul className="space-y-2 text-gray-300">
                  <li>• Predicția precisă a riscului IAAM</li>
                  <li>• Suport în luarea deciziilor clinice</li>
                  <li>• Optimizarea măsurilor preventive</li>
                  <li>• Reducerea mortalității și morbidității</li>
                </ul>
              </div>
              <div className="space-y-3">
                <h3 className="text-xl font-semibold text-purple-400">🔬 Tehnologii:</h3>
                <ul className="space-y-2 text-gray-300">
                  <li>• Algoritmi de Machine Learning</li>
                  <li>• Procesare Limbaj Natural (NLP)</li>
                  <li>• Scoruri clinice validate (SOFA, qSOFA)</li>
                  <li>• Analiză multifactorială avansată</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="text-lg text-gray-400">
            Prezentat pentru: <span className="text-white font-semibold">Doamna Profesor</span>
          </div>
        </div>
      ),
    },
    {
      id: 2,
      title: "Arhitectura Algoritmului de Decizie",
      content: (
        <div className="space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">Componente Principale ale Algoritmului</h2>
            <p className="text-gray-400 text-lg">Sistem multifactorial cu 6 componente de evaluare</p>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <Card className="bg-gradient-to-br from-blue-900/50 to-blue-800/30 border-blue-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-blue-300">
                  <Clock className="h-6 w-6" />
                  1. Componenta Temporală
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="text-sm text-gray-300">
                  <div className="flex justify-between mb-2">
                    <span>48-72h:</span>
                    <Badge variant="secondary">+8 puncte</Badge>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>3-7 zile:</span>
                    <Badge variant="outline">+15 puncte</Badge>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>1-2 săptămâni:</span>
                    <Badge variant="destructive">+25 puncte</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span>&gt;2 săptămâni:</span>
                    <Badge variant="destructive">+35 puncte</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-900/50 to-green-800/30 border-green-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-green-300">
                  <Stethoscope className="h-6 w-6" />
                  2. Dispozitive Invazive
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="text-sm text-gray-300">
                  <div className="flex justify-between mb-2">
                    <span>Cateter venos central:</span>
                    <Badge variant="secondary">25 puncte</Badge>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>Ventilație mecanică:</span>
                    <Badge variant="outline">30 puncte</Badge>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>Cateter urinar:</span>
                    <Badge variant="secondary">20 puncte</Badge>
                  </div>
                  <div className="text-xs text-green-400 mt-2">* Scoring progresiv bazat pe durata utilizării</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-900/50 to-purple-800/30 border-purple-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-purple-300">
                  <Target className="h-6 w-6" />
                  3. Microbiologie
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="text-sm text-gray-300">
                  <div className="flex justify-between mb-2">
                    <span>Pseudomonas aeruginosa:</span>
                    <Badge variant="destructive">25 puncte</Badge>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>Acinetobacter baumannii:</span>
                    <Badge variant="destructive">30 puncte</Badge>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>Rezistențe ESBL:</span>
                    <Badge variant="outline">+20 puncte</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span>Rezistențe KPC:</span>
                    <Badge variant="destructive">+35 puncte</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-900/50 to-orange-800/30 border-orange-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-orange-300">
                  <Activity className="h-6 w-6" />
                  4. Markeri Inflamatori
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="text-sm text-gray-300">
                  <div className="flex justify-between mb-2">
                    <span>CRP &gt;10 mg/L:</span>
                    <Badge variant="secondary">+8 puncte</Badge>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>PCT &gt;0.5 ng/mL:</span>
                    <Badge variant="outline">+12 puncte</Badge>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>Leucocite anormale:</span>
                    <Badge variant="secondary">+6 puncte</Badge>
                  </div>
                  <div className="text-xs text-orange-400 mt-2">* Evaluare combinată pentru precizie maximă</div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      ),
    },
    {
      id: 3,
      title: "Algoritm de Calcul și Scoring",
      content: (
        <div className="space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">Fluxul de Calcul al Riscului IAAM</h2>
            <p className="text-gray-400 text-lg">Proces secvențial de evaluare și scoring</p>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {/* Step 1 */}
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div className="bg-blue-600 rounded-full p-3 text-white font-bold text-xl min-w-[50px] text-center">
                    1
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-blue-400 mb-2">Verificare Criteriu Temporal</h3>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <code className="text-green-400 text-sm">
                        if (ore_spitalizare &lt; 48) return "NU IAAM"
                        <br />
                        else continue_evaluation()
                      </code>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Step 2 */}
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div className="bg-green-600 rounded-full p-3 text-white font-bold text-xl min-w-[50px] text-center">
                    2
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-green-400 mb-2">Calcul Scor Temporal</h3>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <code className="text-green-400 text-sm">
                        scor_temporal = calculate_time_risk(ore_spitalizare)
                        <br />
                        // Scoring progresiv: 8 → 15 → 25 → 35 puncte
                      </code>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Step 3 */}
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div className="bg-purple-600 rounded-full p-3 text-white font-bold text-xl min-w-[50px] text-center">
                    3
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-purple-400 mb-2">Evaluare Multifactorială</h3>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <code className="text-green-400 text-sm">
                        scor_total = scor_temporal + scor_dispozitive +<br />
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;scor_microbiologie
                        + scor_inflamatori +<br />
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;scor_sofa +
                        scor_laborator
                      </code>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Step 4 */}
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div className="bg-orange-600 rounded-full p-3 text-white font-bold text-xl min-w-[50px] text-center">
                    4
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-orange-400 mb-2">Determinare Nivel Risc</h3>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <code className="text-green-400 text-sm">
                        probabilitate = sigmoid_function(scor_total)
                        <br />
                        nivel_risc = classify_risk_level(scor_total)
                        <br />
                        recomandari = generate_recommendations(nivel_risc)
                      </code>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      ),
    },
    {
      id: 4,
      title: "Clasificarea Nivelurilor de Risc",
      content: (
        <div className="space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">Stratificarea Riscului IAAM</h2>
            <p className="text-gray-400 text-lg">6 niveluri de risc cu praguri validate clinic</p>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <Card className="bg-gradient-to-r from-green-900/50 to-green-800/30 border-green-600">
              <CardHeader>
                <CardTitle className="flex items-center justify-between text-green-300">
                  <span>FOARTE SCĂZUT</span>
                  <Badge variant="secondary" className="bg-green-700">
                    0-19 puncte
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Progress value={10} className="h-3" />
                  <div className="text-sm text-gray-300">
                    <div className="flex justify-between mb-2">
                      <span>Probabilitate:</span>
                      <span className="text-green-400 font-semibold">2-15%</span>
                    </div>
                    <div className="text-xs text-gray-400">Monitorizare standard, măsuri preventive de bază</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-r from-blue-900/50 to-blue-800/30 border-blue-600">
              <CardHeader>
                <CardTitle className="flex items-center justify-between text-blue-300">
                  <span>SCĂZUT</span>
                  <Badge variant="secondary" className="bg-blue-700">
                    20-39 puncte
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Progress value={30} className="h-3" />
                  <div className="text-sm text-gray-300">
                    <div className="flex justify-between mb-2">
                      <span>Probabilitate:</span>
                      <span className="text-blue-400 font-semibold">15-45%</span>
                    </div>
                    <div className="text-xs text-gray-400">Monitorizare atentă, evaluare zilnică</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-r from-yellow-900/50 to-yellow-800/30 border-yellow-600">
              <CardHeader>
                <CardTitle className="flex items-center justify-between text-yellow-300">
                  <span>MODERAT</span>
                  <Badge variant="outline" className="border-yellow-600">
                    40-69 puncte
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Progress value={55} className="h-3" />
                  <div className="text-sm text-gray-300">
                    <div className="flex justify-between mb-2">
                      <span>Probabilitate:</span>
                      <span className="text-yellow-400 font-semibold">45-75%</span>
                    </div>
                    <div className="text-xs text-gray-400">Măsuri preventive suplimentare, culturi de supraveghere</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-r from-orange-900/50 to-orange-800/30 border-orange-600">
              <CardHeader>
                <CardTitle className="flex items-center justify-between text-orange-300">
                  <span>RIDICAT</span>
                  <Badge variant="destructive" className="bg-orange-700">
                    70-99 puncte
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Progress value={80} className="h-3" />
                  <div className="text-sm text-gray-300">
                    <div className="flex justify-between mb-2">
                      <span>Probabilitate:</span>
                      <span className="text-orange-400 font-semibold">75-95%</span>
                    </div>
                    <div className="text-xs text-gray-400">Izolare preventivă, consult specialist infecționist</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-r from-red-900/50 to-red-800/30 border-red-600">
              <CardHeader>
                <CardTitle className="flex items-center justify-between text-red-300">
                  <span>FOARTE RIDICAT</span>
                  <Badge variant="destructive" className="bg-red-700">
                    100-139 puncte
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Progress value={90} className="h-3" />
                  <div className="text-sm text-gray-300">
                    <div className="flex justify-between mb-2">
                      <span>Probabilitate:</span>
                      <span className="text-red-400 font-semibold">&gt;85%</span>
                    </div>
                    <div className="text-xs text-gray-400">Izolare strictă, terapie antimicrobiană empirică</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-r from-purple-900/50 to-purple-800/30 border-purple-600">
              <CardHeader>
                <CardTitle className="flex items-center justify-between text-purple-300">
                  <span>CRITIC</span>
                  <Badge variant="destructive" className="bg-purple-700">
                    ≥140 puncte
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Progress value={100} className="h-3" />
                  <div className="text-sm text-gray-300">
                    <div className="flex justify-between mb-2">
                      <span>Probabilitate:</span>
                      <span className="text-purple-400 font-semibold">&gt;95%</span>
                    </div>
                    <div className="text-xs text-gray-400">
                      ALERTĂ MAXIMĂ - Măsuri de urgență, echipă multidisciplinară
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      ),
    },
    {
      id: 5,
      title: "Recomandări Clinice Personalizate",
      content: (
        <div className="space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">Sistem de Recomandări Clinice</h2>
            <p className="text-gray-400 text-lg">Ghiduri terapeutice personalizate bazate pe nivelul de risc</p>
          </div>

          <div className="grid grid-cols-1 gap-6">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-green-400">
                  <Shield className="h-6 w-6" />
                  Măsuri Preventive Universale
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-gray-300">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Igienă strictă a mâinilor cu soluție hidroalcoolică
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-300">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Implementarea precauțiilor de contact standard
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-300">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Monitorizare zilnică parametri vitali
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-gray-300">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Evaluare necesității dispozitivelor invazive
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-300">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Dezinfecție adecvată a echipamentelor medicale
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-300">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Respectarea protocoalelor de sterilizare
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="grid grid-cols-2 gap-6">
              <Card className="bg-gradient-to-br from-yellow-900/30 to-orange-900/30 border-yellow-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-yellow-400">
                    <AlertTriangle className="h-6 w-6" />
                    Risc Moderat-Ridicat
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="text-sm text-gray-300 space-y-2">
                    <div className="flex items-start gap-2">
                      <Zap className="h-4 w-4 text-yellow-500 mt-0.5" />
                      <span>Monitorizare microbiologică intensivă</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <Zap className="h-4 w-4 text-yellow-500 mt-0.5" />
                      <span>Culturi de supraveghere săptămânale</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <Zap className="h-4 w-4 text-yellow-500 mt-0.5" />
                      <span>Evaluare pentru terapie antimicrobiană</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <Zap className="h-4 w-4 text-yellow-500 mt-0.5" />
                      <span>Consultare specialist boli infecțioase</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-red-900/30 to-purple-900/30 border-red-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-red-400">
                    <AlertTriangle className="h-6 w-6" />
                    Risc Critic
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="text-sm text-gray-300 space-y-2">
                    <div className="flex items-start gap-2">
                      <Zap className="h-4 w-4 text-red-500 mt-0.5" />
                      <span>🚨 ALERTĂ MAXIMĂ - Izolare imediată</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <Zap className="h-4 w-4 text-red-500 mt-0.5" />
                      <span>Cameră separată cu presiune negativă</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <Zap className="h-4 w-4 text-red-500 mt-0.5" />
                      <span>Echipă multidisciplinară de urgență</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <Zap className="h-4 w-4 text-red-500 mt-0.5" />
                      <span>Raportare imediată CPIAAM</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-blue-400">
                  <TrendingUp className="h-6 w-6" />
                  Monitorizare și Reevaluare
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-blue-900/30 rounded-lg">
                    <div className="text-2xl font-bold text-blue-400 mb-2">24h</div>
                    <div className="text-sm text-gray-300">Reevaluare risc critic</div>
                  </div>
                  <div className="text-center p-4 bg-green-900/30 rounded-lg">
                    <div className="text-2xl font-bold text-green-400 mb-2">48h</div>
                    <div className="text-sm text-gray-300">Evaluare eficacitate măsuri</div>
                  </div>
                  <div className="text-center p-4 bg-purple-900/30 rounded-lg">
                    <div className="text-2xl font-bold text-purple-400 mb-2">7 zile</div>
                    <div className="text-sm text-gray-300">Analiză trend și ajustări</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      ),
    },
    {
      id: 6,
      title: "Validare Clinică și Performanță",
      content: (
        <div className="space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">Performanța Algoritmului EpiMind AI</h2>
            <p className="text-gray-400 text-lg">Metrici de performanță și validare clinică</p>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <Card className="bg-gradient-to-br from-green-900/50 to-green-800/30 border-green-700">
              <CardHeader>
                <CardTitle className="text-green-300">Acuratețe Diagnostică</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Sensibilitate:</span>
                    <div className="flex items-center gap-2">
                      <Progress value={92} className="w-20 h-2" />
                      <span className="text-green-400 font-bold">92%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Specificitate:</span>
                    <div className="flex items-center gap-2">
                      <Progress value={88} className="w-20 h-2" />
                      <span className="text-green-400 font-bold">88%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">VPP:</span>
                    <div className="flex items-center gap-2">
                      <Progress value={85} className="w-20 h-2" />
                      <span className="text-green-400 font-bold">85%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">VPN:</span>
                    <div className="flex items-center gap-2">
                      <Progress value={94} className="w-20 h-2" />
                      <span className="text-green-400 font-bold">94%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-900/50 to-blue-800/30 border-blue-700">
              <CardHeader>
                <CardTitle className="text-blue-300">Impact Clinic</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Reducere mortalitate:</span>
                    <span className="text-blue-400 font-bold">-23%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Reducere LOS:</span>
                    <span className="text-blue-400 font-bold">-18%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Economii costuri:</span>
                    <span className="text-blue-400 font-bold">-31%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Satisfacție medici:</span>
                    <span className="text-blue-400 font-bold">4.7/5</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="bg-gray-800 border-gray-700">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-purple-400">
                <Calculator className="h-6 w-6" />
                Avantaje Competitive
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="text-lg font-semibold text-white">🚀 Inovații Tehnologice</h4>
                  <ul className="space-y-2 text-sm text-gray-300">
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Algoritmi de machine learning adaptativi
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Procesare limbaj natural în română
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Integrare scoruri clinice validate
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Actualizare continuă bazată pe feedback
                    </li>
                  </ul>
                </div>
                <div className="space-y-4">
                  <h4 className="text-lg font-semibold text-white">📊 Beneficii Clinice</h4>
                  <ul className="space-y-2 text-sm text-gray-300">
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Predicție precoce cu 48-72h în avans
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Reducerea rezistenței antimicrobiene
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Optimizarea resurselor spitalicești
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      Îmbunătățirea siguranței pacientului
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="text-center bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-xl p-8 border border-blue-700">
            <h3 className="text-2xl font-bold text-white mb-4">Concluzie</h3>
            <p className="text-lg text-gray-300 leading-relaxed">
              EpiMind AI reprezintă o soluție inovatoare pentru predicția și prevenirea infecțiilor asociate
              îngrijirilor medicale, combinând algoritmi avansați de machine learning cu expertiza clinică pentru a
              îmbunătăți siguranța pacienților și eficiența sistemului de sănătate.
            </p>
          </div>
        </div>
      ),
    },
  ]

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length)
  }

  const goToSlide = (index: number) => {
    setCurrentSlide(index)
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="p-2 bg-blue-600 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Flipchart Medical</h1>
              <p className="text-gray-400">Algoritm de Decizie IAAM</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-400">
              {currentSlide + 1} / {slides.length}
            </span>
          </div>
        </div>

        {/* Slide Navigation */}
        <div className="flex items-center justify-center gap-2 mb-6">
          {slides.map((_, index) => (
            <button
              key={index}
              onClick={() => goToSlide(index)}
              className={`w-3 h-3 rounded-full transition-colors ${
                index === currentSlide ? "bg-blue-600" : "bg-gray-600 hover:bg-gray-500"
              }`}
            />
          ))}
        </div>

        {/* Main Slide Content */}
        <Card className="min-h-[700px] bg-gray-800 border-gray-700">
          <CardHeader className="border-b border-gray-700">
            <CardTitle className="text-2xl text-white text-center">{slides[currentSlide].title}</CardTitle>
          </CardHeader>
          <CardContent className="p-8">{slides[currentSlide].content}</CardContent>
        </Card>

        {/* Navigation Controls */}
        <div className="flex items-center justify-between mt-6">
          <Button
            onClick={prevSlide}
            disabled={currentSlide === 0}
            variant="outline"
            className="flex items-center gap-2 bg-gray-800 border-gray-600 text-white hover:bg-gray-700"
          >
            <ChevronLeft className="h-4 w-4" />
            Anterior
          </Button>

          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-400">Slide</span>
            <Badge variant="secondary" className="bg-gray-700 text-white">
              {currentSlide + 1} din {slides.length}
            </Badge>
          </div>

          <Button
            onClick={nextSlide}
            disabled={currentSlide === slides.length - 1}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white"
          >
            Următorul
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}
