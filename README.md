# AstroBot AI - Intelligent Satellite Maintenance System

## Introduction
AstroBot AI is an intelligent satellite maintenance system that allows users to monitor critical indicators such as battery level, temperature, fuel, pressure, oxygen level, and solar output in real-time. The system is developed using `Dash` for the user interface, and integrates with OpenAI's `GPT` model to provide intelligent responses via the chatbot.

## Features
- **Live Monitoring Dashboard:** Displays real-time metrics of the satellite's vital systems.
- **Chatbot Integration:** AstroBot can answer questions related to satellite maintenance and provide real-time status updates.
- **Dynamic Gauges and Indicators:** Visual representation of battery, temperature, fuel, and more.
- **Interactive Graphs:** View real-time changes in temperature and other parameters.

## Requirements
Before running the project, ensure you have the following libraries installed:

- `dash`
- `dash_daq`
- `plotly`
- `openai`
- `python-dotenv`

You can install these dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt

Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/astrobot-ai.git
cd astrobot-ai
Create a Virtual Environment:

bash
Copy code
python -m venv .venv
Activate the Virtual Environment:

On Windows:
bash
Copy code
.venv\Scripts\activate
On macOS/Linux:
bash
Copy code
source .venv/bin/activate
Install Required Libraries:

bash
Copy code
pip install -r requirements.txt
Set up Environment Variables:

Create a .env file in the project directory and add your OpenAI API key:
makefile
Copy code
OPENAI_API_KEY=your-openai-api-key
Usage
Run the main application file using:

bash
Copy code
python full_enhanced_app.py
The app should launch in your browser at http://127.0.0.1:8050/.

Chatbot Usage
The chatbot can respond to various questions such as:

"What's the battery level?"
"What is the fuel level?"
"What's the temperature?"
"How can I improve satellite efficiency?"
Feel free to test its responses with both technical and non-technical queries!

File Structure
full_enhanced_app.py: Main application file for the Dash app and chatbot.
requirements.txt: Contains all necessary libraries.
.env: File to store environment variables (OpenAI API Key).
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch for your feature (git checkout -b feature-name).
Commit your changes (git commit -m 'Add new feature').
Push to your branch (git push origin feature-name).
Open a Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Developed by AstroBot AI Team 
Mohsen Seraj Al-Ghamdi 
Abdulrhman K Almania
Abdulaziz B Alghoraibi
