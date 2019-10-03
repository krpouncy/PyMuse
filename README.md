# PyMuse
A way to connect to the Muse Headset via the Muse Monitor
### Windows Python Only :(

# Getting Connected
### 1. Connect your headband to the Muse Monitor App 
[[Android](https://play.google.com/store/apps/details?id=com.sonicPenguins.museMonitor)][[Apple](https://apps.apple.com/us/app/muse-monitor/id988527143
)]
### 2. Check the Muse Monitor Settings
1. Set the Server IP to your computer IP address
2. Set the Server Port to 5000
3. Set the OSC Stream Brainwaves to "All Values"
# <img alt="check settings" src="https://i.imgur.com/iqPnhLa.gif">
### 3. Start the Server
# <img alt="start server" src="https://i.imgur.com/Qhf49tR.gif">

# Usage Examples
### Getting Started
```python
import PyMuse
headband = PyMuse.Headband()
headband.start_server()
```
### Setting the Server IP Address and Port Number
#### Method 1:
```python
headband = PyMuse.Headband(ip = "192.168.0.42", port = 8000)
```
#### Method 2: (when multithreading)
```python
class MindReader(QObject, PyMuse.Headband):
  def __init__(self)
    super().__init__()
    
  def run(self):
    pass
    
headband = MindReader()
headband.setServerInfo("192.168.0.42", 8000)
```

### Getting Derivative Brainwaves
```python
import PyMuse

# Create a child class
class MindReader(PyMuse.Headband):
  def run(self):
  """ this method updates at 10hz """
    brainwaves = self.get_brainwaves()
    alpha_brainwaves = brainwaves["alpha"]
    theta_brainwaves = brainwaves["theta"]
    
    average = lambda x: sum(x)/len(x)
    if average(alpha_brainwaves) < average(gamma_brainwaves):
      print("More Alpha than Theta")

# Start the server
headband = MindReader()
headband = MindReader(ip = "192.168.0.42", port = 8000)
headband.start_server()
```
### Getting Raw Brainwaves
```python
class MindReader(PyMuse.Headband):
  def run(self):
    raw_eeg = self.get_raw_brainwaves()
    eeg1 = raw_eeg[0]
    eeg2 = raw_eeg[1]
    eeg3 = raw_eeg[2]
    eeg4 = raw_eeg[3]
    print(eeg1, eeg2, eeg3, eeg4)

headband = MindReader(ip = "192.168.0.42", port = 8000)
headband.start_server()
```
