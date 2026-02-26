# Jarvis Brain

An intelligent home automation and multi-device orchestration system that combines voice commands, AI reasoning, and autonomous agents to manage macOS, Windows, Android, and cloud environments.

## Architecture

```
jarvis-brain/
├── core/                # Jarvis HQ (Mac mini daemon)
│   ├── main.py          # Entry point for Jarvis HQ
│   ├── voice_nlp.py     # Speech recognition + NLP
│   ├── reasoning.py     # Task planning + breakdown
│   ├── decision_layer.py# IQ module (performance-based assignment)
│   ├── security.py      # Authentication, rollback, logging
│   └── sync.py          # Cloud sync + backup
│
├── agents/              # Device agents
│   ├── mac_agent.py     # Mac control (builds, VS Code, rendering)
│   ├── windows_agent.py # Windows control (deployments, services)
│   ├── android_agent.py # Android companion (WhatsApp, SMS, battery)
│   └── cloud_agent.py   # Cloud node (24/7 uptime, research)
│
├── modules/             # Feature modules (plug-and-play)
│   ├── whatsapp.py      # WhatsApp integration (API/Web/OTP handling)
│   ├── phone_assistant.py # SMS, hotspot, notifications
│   ├── dashboard.py     # Web UI + proactive alerts
│   └── research.py      # Research + planning engine
│
├── data/                # Logs, configs, backups
│   ├── logs/            # Audit logs
│   ├── configs/         # Device configs
│   └── backups/         # Cloud sync backups
│
├── tests/               # Unit + integration tests
│   ├── test_voice.py
│   ├── test_agents.py
│   └── test_security.py
│
└── README.md            # Documentation
```

## Components

### Core Module
The brain of Jarvis, running on a Mac mini daemon:
- **main.py**: Entry point and main event loop
- **voice_nlp.py**: Speech recognition and natural language processing
- **reasoning.py**: Task planning and decomposition
- **decision_layer.py**: Intelligent task assignment based on agent performance
- **security.py**: Authentication, audit logging, and rollback management
- **sync.py**: Cloud synchronization and backup management

### Agents
Autonomous agents for different devices and environments:
- **MacAgent**: Controls macOS operations, builds, VS Code, rendering
- **WindowsAgent**: Manages Windows services and deployments
- **AndroidAgent**: Phone companion for messaging and notifications
- **CloudAgent**: 24/7 cloud node for continuous operations

### Modules
Plug-and-play feature modules:
- **WhatsAppManager**: Messaging integration with multiple connection modes
- **SMSManager**: SMS handling
- **HotspotManager**: Mobile hotspot control
- **NotificationManager**: Push notifications
- **Dashboard**: Web UI and alerts
- **ResearchEngine**: Knowledge gathering and research tasks
- **PlanningEngine**: Strategic planning and objective management

## Getting Started

### Prerequisites
- Python 3.8+
- macOS (for core), Windows, Android device, or cloud account (for respective agents)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd jarvis-brain

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (coming soon)
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_voice.py

# Run with coverage
python -m pytest tests/ --cov=core --cov=agents --cov=modules
```

### Starting Jarvis

```bash
python core/main.py
```

## Usage Examples

### Voice Commands
```python
from core.voice_nlp import VoiceRecognizer, NLPProcessor

recognizer = VoiceRecognizer()
recognizer.start_listening()

processor = NLPProcessor()
command = processor.parse_command("send message to john on whatsapp")
```

### Task Assignment
```python
from core.decision_layer import DecisionLayer
from core.reasoning import ReasoningEngine

decision_layer = DecisionLayer()
reasoning = ReasoningEngine()

task = reasoning.plan_task("build project")
agent = decision_layer.assign_task("build", ["compiler", "git"])
```

### Multi-Device Operations
```python
from agents.mac_agent import MacAgent
from agents.android_agent import AndroidAgent

mac = MacAgent()
mac.build_project("/path/to/project")

android = AndroidAgent("device_123")
android.send_whatsapp_message("+1234567890", "Build complete!")
```

## Features

- 🗣️ Voice command interface with NLP
- 🧠 Intelligent task reasoning and planning
- 🤖 Multi-device agent orchestration
- 📊 Performance-based task assignment
- 💬 WhatsApp, SMS, and notification integration
- 🔐 Authentication and security audit logging
- 💾 Cloud sync and backup management
- 📈 Web dashboard with alerts
- 🔄 System state rollback capabilities

## Development

### Project Structure
- Each module is self-contained and plug-and-play
- Agents communicate through the decision layer
- Logging is centralized for audit trails

### Adding New Agents
1. Create agent file in `agents/`
2. Extend base agent interface
3. Implement required capabilities
4. Register in decision layer

### Adding New Modules
1. Create module in `modules/`
2. Follow existing module patterns
3. Add to `__init__.py`
4. Create tests in `tests/`

## Testing

Unit tests are provided for:
- Voice recognition and NLP
- All agents (Mac, Windows, Android, Cloud)
- Security and authentication
- Task reasoning and planning

Run tests with:
```bash
python -m unittest discover tests/
```

## Security

- Authentication required for sensitive operations
- Audit logging of all system events
- Rollback capabilities for failed operations
- Encrypted cloud synchronization

## Performance Metrics

The decision layer tracks agent performance:
- Success rate per agent type
- Task execution time
- Error rates
- Dynamic performance adjustment

## Cloud Integration

Jarvis supports cloud operations:
- 24/7 uptime on cloud nodes
- Research task distribution
- Backup synchronization
- Remote monitoring and control

## License

TBD

## Contributing

Contributions welcome! Please follow the existing code structure and add tests for new features.

## Future Enhancements

- Machine learning for task optimization
- Advanced reasoning with reinforcement learning
- Real-time collaboration between agents
- Extended device support (IoT, smart home)
- Advanced analytics and reporting

---

**Jarvis Brain** - Your intelligent home automation system
