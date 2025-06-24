import subprocess

# Using a raw string to avoid escape sequence issues
subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])


import webbrowser

# Open a website
webbrowser.open("https://www.google.com")
webbrowser.open("https://chatgpt.com/?model=auto")