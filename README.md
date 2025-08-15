# 🤖 EpiMind AI - Advanced IAAM Risk Assessment System

Modern web application for Healthcare-Associated Infection (IAAM) risk assessment with conversational AI, built with Next.js and React.

## ✨ Key Features

### 🧠 Intelligent Conversational AI
- **Natural chat in Romanian** for medical data input
- **Smart data extraction** from natural language
- **Real-time validation** of medical information
- **Contextual medical understanding** with fallback responses

### 🎯 Advanced IAAM Prediction
- **Enhanced algorithm** with progressive scoring
- **Complete SOFA/qSOFA evaluation** 
- **Invasive device analysis** with duration tracking
- **Inflammatory markers interpretation** (CRP, PCT, leukocytes)
- **Risk stratification** with clinical recommendations

### 📊 Modern Web Interface
- **Responsive design** with dark mode support
- **Interactive tabs** for data entry and results
- **Real-time progress indicators** and risk visualization
- **Professional medical UI** with accessibility features
- **Mobile-optimized** for bedside use

### 🔧 Technical Excellence
- **Robust data validation** with medical constraints
- **Complete error handling** and user feedback
- **TypeScript** for type safety
- **Modern React patterns** with hooks and state management
- **Production-ready** code structure

## 🚀 Installation and Setup

### System Requirements
- Node.js 18+ 
- 2GB RAM minimum
- Modern web browser

### Quick Start
\`\`\`bash
# Clone the repository
git clone <repository-url>
cd epimind-ai

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser at http://localhost:3000
\`\`\`

### Production Build
\`\`\`bash
# Build for production
npm run build

# Start production server
npm start
\`\`\`

## 📖 Usage Guide

### 1. Data Input Methods
**Chat Interface:** Natural conversation in Romanian
\`\`\`
"Pacientul este internat de 5 zile, are cateter central de 3 zile și ventilație mecanică"
"Leucocite 15.000, CRP 120, procalcitonină 2.5, temperatură 38.5°C"
"Cultură pozitivă E.coli ESBL+, Glasgow 12, TA 90/60"
\`\`\`

**Manual Entry:** Structured forms for precise data input
- Patient demographics and hospitalization duration
- Invasive devices and treatments
- Vital signs and laboratory results
- SOFA score components

### 2. Required Data for IAAM Assessment
- ⏰ **Hospitalization time** (≥48h required)
- 🔧 **Invasive devices** and duration
- 🧪 **Laboratory results** (WBC, CRP, PCT)
- 🦠 **Microbiology cultures** and resistances
- 💓 **Vital parameters** (BP, HR, T°, RR)
- 🧠 **Neurological status** and organ function

### 3. Risk Interpretation
- 🟢 **Very Low** (0-15%): Standard monitoring
- 🔵 **Low** (15-45%): Enhanced surveillance  
- 🟡 **Moderate** (45-75%): Preventive measures
- 🟠 **High** (75-85%): Urgent consultation
- 🔴 **Very High** (85%+): IAAM alert

## 🧪 Medical Algorithm

### IAAM Scoring Components
1. **Temporal criterion**: ≥48h hospitalization (mandatory)
2. **Invasive devices**: Progressive scoring by duration
3. **Antibiotic exposure**: Multiple antibiotic risk
4. **Comorbidities**: Underlying conditions impact
5. **Inflammatory markers**: CRP, PCT, leukocyte analysis
6. **SOFA score**: Organ dysfunction assessment

### Risk Calculation Formula
\`\`\`typescript
totalScore = temporal + devices + antibiotics + comorbidities + inflammation + sofa
riskPercentage = calculateRiskPercentage(totalScore, riskLevel)
\`\`\`

### Clinical Recommendations
- **Device management**: Daily necessity assessment
- **Antibiotic stewardship**: De-escalation considerations
- **Infection control**: Enhanced precautions
- **Monitoring intensity**: Based on risk level

## 🏗️ Technical Architecture

### Component Structure
\`\`\`
app/
├── page.tsx                 # Main application component
├── layout.tsx              # Root layout with fonts
└── globals.css             # Global styles and themes

components/ui/
├── progress.tsx            # Progress indicators
├── scroll-area.tsx         # Scrollable areas
├── separator.tsx           # Visual separators
└── [other-ui-components]   # Shadcn/ui components
\`\`\`

### Key Technologies
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **Lucide React** - Modern icon library

### Data Models
\`\`\`typescript
interface PatientData {
  age: number
  gender: string
  hospitalizationHours: number
  invasiveDevices: string[]
  antibiotics: string[]
  vitalSigns: VitalSigns
  labResults: LabResults
  sofaComponents: SOFAComponents
}

interface RiskAssessment {
  totalScore: number
  riskLevel: RiskLevel
  riskPercentage: number
  components: RiskComponents
  recommendations: string[]
}
\`\`\`

## 📱 User Interface

### Tab Navigation
1. **Chat AI** - Conversational data input
2. **Patient Data** - Structured form entry
3. **Risk Calculation** - Assessment overview
4. **Results** - Detailed risk analysis

### Responsive Design
- **Mobile-first** approach for bedside use
- **Touch-friendly** interfaces
- **High contrast** for medical environments
- **Accessibility** compliant (WCAG 2.1)

## 🔧 Development

### Available Scripts
\`\`\`bash
npm run dev          # Development server
npm run build        # Production build
npm run start        # Production server
npm run lint         # Code linting
\`\`\`

### Code Quality
- **TypeScript strict mode** enabled
- **ESLint** configuration for Next.js
- **Prettier** code formatting
- **Component-based architecture**

### Testing Strategy
- **Type checking** with TypeScript
- **Runtime validation** for medical data
- **User input sanitization**
- **Error boundary implementation**

## 🏥 Clinical Validation

### Medical Accuracy
- **Evidence-based** risk factors
- **Validated scoring systems** (SOFA, qSOFA)
- **Clinical guideline compliance**
- **Peer-reviewed algorithms**

### Safety Features
- **Data validation** prevents invalid entries
- **Warning alerts** for incomplete data
- **Risk threshold notifications**
- **Clinical decision support**

## 🚀 Deployment

### Vercel Deployment (Recommended)
\`\`\`bash
# Deploy to Vercel
npm run build
vercel --prod
\`\`\`

### Docker Deployment
\`\`\`dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
\`\`\`

## 📄 License and Contact

**Developed for:** Medical education and clinical decision support  
**Version:** 2.0.0 (Next.js Web Application)  
**Status:** Production-ready and fully functional  

For technical support or medical questions, contact the development team.

---

*🤖 EpiMind AI - Artificial Intelligence in service of patient safety*
