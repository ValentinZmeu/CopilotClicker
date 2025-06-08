# Automation with PyAutoGUI & OpenCV for GitHub Copilot

[![Python Version](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-green)](#license)

Automate clicks on the “Continue” button in GitHub Copilot conversations using template matching. No more manual intervention—just supply a detailed prompt and let the script run uninterrupted.

## 🚀 Features

- **Template Matching** with OpenCV to detect the “Continue” button on-screen
- **Automated Clicks** via PyAutoGUI when the button appears
- **Configurable** detection threshold and scan interval
- **Cross-Platform** support (Windows, macOS, Linux)

## 🔧 Requirements

- Python 3.x
- Libraries:
  - `opencv-python`
  - `numpy`
  - `pyautogui`
  - `Pillow` (Windows only)

## 🛠️ Installation

1. **Clone Repository**  
   ```bash
   git clone https://github.com/ValentinZmeu/CopilotClicker
   cd CopilotClicker
   ```

2. **Setup Virtual Environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

- Place `button.png` in the `assets` folder
- Adjust detection parameters in `config.py`:
  ```python
  MATCH_THRESHOLD = 0.8       # Matching confidence
  SCAN_INTERVAL   = 2.0       # Seconds between scans
  ```

## ▶️ Usage

```bash
python start.py
```

1. Prepare your Copilot prompt with clear, step-by-step instructions.
2. Run the script; it will auto-detect and click “Continue” without pausing.

## 📈 SEO Keywords

`pyautogui automation`, `OpenCV template matching`, `GitHub Copilot script`, `automate button click`, `python screen automation`

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to branch (`git push origin feature-name`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
