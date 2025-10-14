# URL Attack Detection System - Batch Files

This directory contains several Windows batch files (.bat) to easily run the URL Attack Detection System in different modes.

## 🚀 Quick Start Batch Files

### **launcher.bat** - Main Menu (Recommended)
```
Double-click launcher.bat
```
- **Purpose**: Interactive menu with all options
- **Features**: User-friendly interface to choose different modes
- **Best for**: First-time users and general usage

### **start.bat** - Web Interface
```
Double-click start.bat
```
- **Purpose**: Starts the web-based interface
- **Access**: Opens server at http://127.0.0.1:5000
- **Best for**: Full-featured analysis with web dashboard

---

## 📊 Analysis Modes

### **interactive_analysis.bat** - Interactive CLI
```
Double-click interactive_analysis.bat
```
- **Purpose**: Analyze multiple URLs in command line
- **Usage**: Enter URLs one by one, get immediate results
- **Best for**: Quick testing of multiple URLs

### **analyze_url.bat** - Single URL Analysis
```
analyze_url.bat "http://example.com/test?id=1"
```
- **Purpose**: Analyze one specific URL
- **Usage**: Run from command line with URL parameter
- **Best for**: Scripting and automation

---

## 🛠️ Utility Batch Files

### **generate_data.bat** - Sample Data Generator
```
Double-click generate_data.bat
```
- **Purpose**: Create sample attack data for testing
- **Usage**: Specify number of records to generate
- **Best for**: Populating database for demonstration

### **upload_to_github.bat** - GitHub Upload
```
Double-click upload_to_github.bat
```
- **Purpose**: Upload project to GitHub repository
- **Usage**: Follow prompts to set up git and push code
- **Best for**: Sharing your project

---

## 📝 Usage Examples

### Example 1: Basic Web Interface
```batch
REM Just double-click start.bat
start.bat
```

### Example 2: Test Malicious URLs
```batch
REM Test SQL injection
analyze_url.bat "http://site.com/login?user=' OR '1'='1"

REM Test XSS
analyze_url.bat "http://site.com/search?q=<script>alert('XSS')</script>"

REM Test Directory Traversal  
analyze_url.bat "http://site.com/file?path=../../../etc/passwd"
```

### Example 3: Interactive Analysis Session
```batch
REM Start interactive mode
interactive_analysis.bat

REM Then enter URLs interactively:
URL> http://example.com/login?user=' OR '1'='1
URL> http://example.com/search?q=<script>alert('XSS')</script>
URL> quit
```

---

## ⚙️ Configuration

### Web Server Configuration
The batch files start the server with these default settings:
- **Host**: 0.0.0.0 (accessible from network)
- **Port**: 5000
- **Debug Mode**: Enabled

### Customization
To modify server settings, edit the batch files:
```batch
REM In start.bat, change this line:
python main.py --mode web --host 0.0.0.0 --port 5000

REM To custom settings:
python main.py --mode web --host 127.0.0.1 --port 8080
```

---

## 🚨 Troubleshooting

### Common Issues

#### "Python is not recognized"
```
ERROR: Python is not installed or not in PATH
```
**Solution**: Install Python from https://python.org and add to PATH

#### "Module not found" errors
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Install requirements
```batch
pip install -r requirements.txt
```

#### Port already in use
```
Address already in use
```
**Solution**: 
1. Kill existing process using port 5000
2. Or change port in batch file

#### Permission errors
```
Permission denied
```
**Solution**: Run as Administrator

---

## 🔧 Advanced Usage

### Running with Custom Parameters
You can modify any batch file to add custom parameters:

```batch
REM Custom port
python main.py --mode web --port 8080

REM Custom host (localhost only)
python main.py --mode web --host 127.0.0.1

REM Generate more sample data
python main.py --mode generate --num-records 5000
```

### Integration with Other Tools
The batch files can be called from other scripts:

```batch
REM Call from another batch file
call analyze_url.bat "http://suspicious-site.com"

REM Call with error handling
call analyze_url.bat "http://test.com" && echo Success || echo Failed
```

---

## 📁 File Descriptions

| File | Purpose | Mode | Interactive |
|------|---------|------|-------------|
| `launcher.bat` | Main menu system | All | Yes |
| `start.bat` | Web interface | Web | No |
| `interactive_analysis.bat` | CLI analysis | Analyze | Yes |
| `analyze_url.bat` | Single URL | CLI | No |
| `generate_data.bat` | Sample data | Generate | Yes |
| `upload_to_github.bat` | Git operations | Utility | Yes |

---

## 🎯 Best Practices

1. **Start with launcher.bat** - Use the main menu for easy navigation
2. **Use web interface for demos** - Best visual presentation
3. **CLI for automation** - Use analyze_url.bat in scripts
4. **Generate sample data first** - Populate database for better demos
5. **Test with known malicious URLs** - Verify system functionality

---

## 🚀 Quick Demo Sequence

For a complete demonstration:

1. **Start**: Double-click `launcher.bat`
2. **Generate Data**: Choose option 4 to create sample data
3. **Web Interface**: Choose option 1 to start web server
4. **Open Browser**: Go to http://127.0.0.1:5000
5. **Test URLs**: Use the sample malicious URLs provided

This gives you a complete working demonstration of the URL Attack Detection System!

---

**Note**: All batch files include error checking and user-friendly messages. They will automatically navigate to the correct directories and handle most common issues.