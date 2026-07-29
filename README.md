# 🌊 Jal Drishti AI - Groundwater Analysis Chatbot

## 📋 Project Description

**Jal Drishti AI** is an intelligent, AI-powered groundwater analysis chatbot designed to provide comprehensive insights, trend analysis, and predictions for groundwater data across India. The platform leverages advanced natural language processing, machine learning, and data visualization to make groundwater information accessible to researchers, policymakers, farmers, and citizens through an intuitive conversational interface.

The system integrates with Central Ground Water Board (CGWB) data to deliver real-time analysis, historical trend visualization, and predictive insights. With support for multiple Indian languages and voice interaction, Jal Drishti AI democratizes access to critical water resource information, enabling informed decision-making for water management and conservation efforts.

### Key Objectives
- **Accessibility**: Make groundwater data accessible through natural language queries
- **Intelligence**: Provide AI-powered insights and predictions from complex datasets
- **Localization**: Support multiple Indian languages for broader reach
- **Visualization**: Transform raw data into interactive charts and trend analyses
- **User Experience**: Enable voice interaction and smart suggestions for seamless interaction

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- Python 3.8+
- OpenAI API Key (optional, for full AI features)
- npm or yarn package manager

### Installation & Running

**Option 1: One-Command Setup**
```bash
npm run dev
```

**Option 2: Using Startup Scripts**
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

**Option 3: Manual Setup**
```bash
# Install all dependencies
npm run install:all

# Start development servers
npm run dev
```

**Option 4: Python Setup Script**
```bash
python setup_ai_chatbot.py
```

### Access Points
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000

---

## ✨ Features

### 🤖 AI-Powered Capabilities
- **Natural Language Processing**: Understand complex groundwater-related queries in plain English
- **Smart Query Parsing**: AI-powered location matching and entity extraction
- **Intelligent Insights**: Context-aware recommendations and analysis
- **Conversation Memory**: Maintains context across conversation sessions
- **Predictive Analysis**: Trend detection and future predictions based on historical data

### 🗣️ Voice & Language Support
- **Voice Input**: Real-time speech recognition using Web Speech API
- **Multi-language Support**: 6+ Indian languages (English, Hindi, Bengali, Telugu, Tamil, Gujarati)
- **Voice Output**: Text-to-speech capabilities for accessibility
- **Visual Feedback**: Animated indicators for voice interaction states

### 📊 Data Analysis & Visualization
- **Trend Analysis**: AI-enhanced trend detection and visualization
- **Interactive Charts**: Dynamic charts with trend lines and annotations
- **Comparative Analysis**: Compare groundwater data across different locations
- **Anomaly Detection**: Flags unusual water level changes
- **Historical Data**: Multi-year trend analysis and visualization

### 💡 Smart User Experience
- **Context-Aware Suggestions**: AI-generated follow-up questions
- **Dynamic Recommendations**: Suggestions based on conversation history
- **Quick Actions**: One-click access to common queries
- **Responsive Design**: Optimized for all device sizes
- **Real-time Updates**: Dynamic data refresh capabilities

---

## 🏗️ Technology Stack

### Backend
- **Python 3.8+**: Core backend language
- **Flask**: Web framework for API endpoints
- **OpenAI GPT-3.5-turbo**: Natural language understanding and query processing
- **TF-IDF & Cosine Similarity**: Vector similarity search for location matching
- **Data Processing Libraries**: Pandas, NumPy for data analysis

### Frontend
- **Node.js 16+**: JavaScript runtime
- **Modern Web Technologies**: HTML5, CSS3, JavaScript
- **Web Speech API**: Voice input/output capabilities
- **Chart Libraries**: Interactive data visualization
- **Responsive Framework**: Mobile-first design approach

### Development Tools
- **Concurrently**: Run frontend and backend simultaneously
- **npm/yarn**: Package management
- **Git**: Version control

---

## 📁 Project Structure

```
Jal-Drishti-AI---Groundwater-Analysis-Chatbot/
├── frontend/                 # Frontend application
│   ├── src/                  # Source files
│   ├── public/               # Static assets
│   └── package.json          # Frontend dependencies
├── backend/                  # Backend API server
│   ├── app.py                # Main Flask application
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   └── data/                 # Groundwater datasets
├── AI_FEATURES.md            # Detailed AI features documentation
├── ChatbotIngres.ipynb       # Jupyter notebook for analysis
├── setup_ai_chatbot.py       # Automated setup script
├── start.bat                 # Windows startup script
├── start.sh                  # Linux/Mac startup script
├── package.json              # Root package configuration
└── README.md                 # Project documentation
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_LANGUAGE=EN
```

### OpenAI Settings
- **Model**: GPT-3.5-turbo (configurable)
- **Temperature**: 0.1-0.3 for consistent responses
- **Max Tokens**: 150-200 for concise insights
- **Language**: Supports multiple Indian languages

---

## 📡 API Documentation

### Chat Endpoint

**POST** `/api/chat`

Process natural language queries about groundwater data.

**Request Body:**
```json
{
  "query": "What's the groundwater status in Mumbai?",
  "language": "EN",
  "context": "previous conversation context (optional)"
}
```

**Response:**
```json
{
  "answer": "AI-generated response with insights",
  "language": "EN",
  "chart_url": "/api/charts/trend_chart.png",
  "ai_insights": true,
  "suggestions": ["Follow-up question 1", "Follow-up question 2"]
}
```

### Available Scripts

```bash
# Development
npm run dev              # Start both frontend and backend
npm run frontend:dev     # Start frontend only
npm run backend:dev      # Start backend only

# Installation
npm run install:all     # Install all dependencies
npm run backend:install  # Install Python dependencies only

# Build
npm run build            # Build frontend for production
npm run frontend:build   # Build frontend only
```

---

## 📊 Data Sources

- **Groundwater Data**: Central Ground Water Board (CGWB) data
- **Location Database**: Comprehensive Indian location database
- **Historical Data**: Multi-year trend analysis (2018-2020+)
- **Real-time Updates**: Dynamic data refresh capabilities

---

## 🎯 Use Cases

### For Researchers
- Analyze groundwater trends across different regions
- Compare data across multiple time periods
- Generate insights for research papers and studies

### For Policymakers
- Access comprehensive groundwater status reports
- Identify regions requiring immediate attention
- Make data-driven policy decisions

### For Farmers
- Check groundwater availability in their region
- Understand seasonal trends and patterns
- Plan irrigation and water management strategies

### For Citizens
- Learn about groundwater status in their area
- Understand water conservation needs
- Access information in their preferred language

---

## 🔮 Future Enhancements

- **Machine Learning Models**: Custom ML models for groundwater prediction
- **Real-time Data**: Integration with IoT sensors
- **Advanced Analytics**: Deep learning for pattern recognition
- **Mobile App**: Native mobile application with AI features
- **API Expansion**: Public API for third-party integrations
- **Geographic Mapping**: Interactive maps with groundwater overlays
- **Alert System**: Notifications for critical groundwater changes

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests for new features
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Guidelines
- Follow existing code style and conventions
- Write clear commit messages
- Add documentation for new features
- Test your changes thoroughly
- Ensure backward compatibility

---

## 📝 License

This project is licensed under the MIT License.

---

## 📞 Support & Contact

For questions, issues, or contributions:
- Open an issue on GitHub
- Check `AI_FEATURES.md` for detailed AI capabilities
- Review the Jupyter notebook for data analysis examples

---

## 🙏 Acknowledgments

- Central Ground Water Board (CGWB) for groundwater data
- OpenAI for natural language processing capabilities
- Open source community for various tools and libraries

---

**Made with 💧 for water conservation and sustainable resource management**

