
'''

# 🛡️ AutoMap

**AutoMap** is a CLI-first AI security analyst designed for authorized local network scans. It combines the power of traditional networking tools with local LLMs (via Ollama) to provide readable, actionable defensive analysis.

```
××××××××××××××××××××××
[{BY]}> Dhruv-Creator-De-Pal
××××××××××××××××××××××
```
## ✨ Key Features

* **Live Device Discovery**
* **Asynchronous Port Scanning**
* **AI-Powered Analysis**
* **Clean Terminal UI**
* **Professional Reporting**

---

## 🚀 Installation

### Prerequisites

* **Python**: Version 3.10 or higher.
* **Ollama**: Running locally or accessible via a remote URL.
* **Privileges**: Root access (`sudo`) is required for raw network socket operations.

### Setup

Clone the repository and run the provided installer:

```
git clone [https://github.com/Dhruv-Creator-De-Pal/NetOwl-automap.git](https://www.google.com/search?q=https://github.com/Dhruv-Creator-De-Pal/NetOwl-automap.git)
cd NetOwl-automap
sudo ./install.sh
```

---

## 🛠️ Usage

### Full AI Analysis

Connect to your local Ollama instance for a detailed security breakdown:
```
sudo automap scan 10.0.0.0/24 --mode quick --ai-host http://localhost:11434 --ai-model llama3
```
```
### 3. Scan Modes

| Mode    | Description                                                    |
| `quick` | Scans ~50 high-priority ports for speed.                       |
| `smart` | (Default) Scans critical infrastructure and admin ports.       |
| `full`  | Scans all 65,535 TCP ports (Note: takes significantly longer). |
```
### 4. Custom Report Path

Save your report to a specific location:
```
sudo automap scan 192.168.1.1 --report my-network-security.md
```

---

## 📊 Reporting

Every scan generates a `automap-report.md` by default. This includes:

* **Executive Summary**: High-level metrics of devices and risks.
* **AI Summary**: A plain-English explanation of your network posture.
* **Device Inventory**: Detailed tables showing IP, MAC, open ports, and risk levels.
* **Technical Appendix**: Raw JSON data for integration with other tools.

---

## ⚖️ Security Warning

**AutoMap is for defensive and educational purposes only.** Use this tool only on networks where you have explicit authorization. Unauthorized scanning can be illegal and disruptive.
'''
