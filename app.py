from dash import Dash, dcc, html, Input, Output, State
import dash_daq as daq
import plotly.graph_objs as go
import random
import openai
from dotenv import load_dotenv
import os

# تحميل المتغيرات البيئية من ملف .env
load_dotenv()

# إعداد مفتاح OpenAI من المتغير البيئي
openai.api_key = os.getenv("OPENAI_API_KEY")

# التأكد من أن المفتاح موجود
if not openai.api_key:
    raise ValueError("لم يتم العثور على مفتاح OpenAI. تأكد من إعداد المتغير البيئي 'OPENAI_API_KEY' بشكل صحيح.")

# إعداد التطبيق
app = Dash(__name__)

# المتغيرات الأولية للمؤشرات
current_battery = 85
current_temperature = 40
current_power = 5.4
current_fuel = 70
current_pressure = 150
current_oxygen = 85
current_solar_output = 50

# تصميم الواجهة الأساسية
app.layout = html.Div([
    html.H1("AstroBot AI - Intelligent Satellite Maintenance System",
            style={'textAlign': 'center', 'color': '#007ACC', 'fontFamily': 'Arial', 'marginTop': '20px'}),

    # مؤشرات النظام
    html.Div([
        html.Div([
            daq.Gauge(
                id='battery-level',
                label="Battery Level",
                value=current_battery,
                min=0,
                max=100,
                color={"gradient": True, "ranges": {"green": [60, 100], "yellow": [30, 60], "red": [0, 30]}},
                size=150,
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            daq.Thermometer(
                id='temperature-indicator',
                label="Temperature (°C)",
                value=current_temperature,
                min=-50,
                max=50,
                height=200,
                color="#FF5E5E"
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            daq.LEDDisplay(
                id='power-consumption',
                label="Power Consumption (kW)",
                value=str(current_power),
                color="#92e0d3",
                size=50
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            daq.Tank(
                id='fuel-level',
                label="Fuel Level (%)",
                value=current_fuel,
                min=0,
                max=100,
                showCurrentValue=True,
                color="#1E90FF",
                style={'margin': '0 auto'}
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            daq.Gauge(
                id='pressure-level',
                label="Pressure Level (kPa)",
                value=current_pressure,
                min=0,
                max=200,
                color={"gradient": True, "ranges": {"green": [100, 200], "yellow": [50, 100], "red": [0, 50]}},
                size=150,
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            daq.Tank(
                id='oxygen-level',
                label="Oxygen Level (%)",
                value=current_oxygen,
                min=0,
                max=100,
                showCurrentValue=True,
                color="#FF6347",
                style={'margin': '0 auto'}
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            daq.Gauge(
                id='solar-output',
                label="Solar Output (kW)",
                value=current_solar_output,
                min=0,
                max=100,
                color={"gradient": True, "ranges": {"green": [50, 100], "yellow": [20, 50], "red": [0, 20]}},
                size=150,
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

    ], style={'textAlign': 'center', 'backgroundColor': '#f4f4f4', 'padding': '20px', 'borderRadius': '10px'}),

    # الرسم البياني
    html.Div([
        dcc.Graph(
            id='live-graph',
            animate=True,
            style={'width': '70%', 'margin': '0 auto'}
        )
    ], style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'marginTop': '20px'}),

    # واجهة الشات بوت
    html.Div([
        html.H3("Chat Interface", style={'textAlign': 'center', 'color': '#007ACC', 'fontFamily': 'Arial'}),
        dcc.Textarea(
            id='chat-history',
            value='AstroBot: Hello, how can I assist you today?',
            style={'width': '100%', 'height': 300, 'borderRadius': '10px', 'border': '2px solid #007ACC',
                   'padding': '10px', 'fontFamily': 'Courier New'}
        ),
        dcc.Input(
            id='user-input',
            type='text',
            placeholder='Type your message here...',
            style={'width': '80%', 'borderRadius': '5px', 'padding': '10px', 'border': '2px solid #007ACC',
                   'fontFamily': 'Arial'}
        ),
        html.Button('Send', id='send-button', n_clicks=0,
                    style={'width': '15%', 'marginLeft': '5px', 'backgroundColor': '#007ACC', 'color': '#ffffff',
                           'border': 'none', 'padding': '10px', 'borderRadius': '5px'}),
    ], style={'padding': '20px', 'width': '50%', 'margin': '0 auto', 'backgroundColor': '#e6f7ff',
              'borderRadius': '10px', 'border': '1px solid #007ACC'}),

    dcc.Interval(
        id='interval-component',
        interval=2000,  # تحديث كل 2 ثانية
        n_intervals=0
    )
])

# تحليل طلبات المستخدم وإرجاع القيم بشكل صحيح
def parse_user_message(user_message):
    if "battery" in user_message.lower():
        return f"The current battery level is {int(current_battery)}%."
    elif "fuel" in user_message.lower():
        return f"The current fuel level is {int(current_fuel)}%."
    elif "temperature" in user_message.lower():
        return f"The current temperature is {int(current_temperature)}°C."
    elif "pressure" in user_message.lower():
        return f"The current pressure level is {int(current_pressure)} kPa."
    elif "oxygen" in user_message.lower():
        return f"The current oxygen level is {int(current_oxygen)}%."
    elif "solar" in user_message.lower():
        return f"The current solar output is {int(current_solar_output)} kW."
    elif "power" in user_message.lower():
        return f"The current power consumption is {int(current_power)} kW."
    else:
        return None

# منطق الشات بوت
@app.callback(
    Output('chat-history', 'value'),
    [Input('send-button', 'n_clicks')],
    [State('user-input', 'value'),
     State('chat-history', 'value')]
)
def update_chat(n_clicks, user_message, chat_history):
    if n_clicks > 0 and user_message:
        # تحليل الرسالة للتحقق مما إذا كانت تطلب معلومات معينة
        response = parse_user_message(user_message)
        if response:
            new_history = f"{chat_history}\nUser: {user_message}\nAstroBot: {response}"
            return new_history

        try:
            # استخدام نموذج gpt-3.5-turbo للرد العام
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are AstroBot, an AI assistant for satellite maintenance."},
                    {"role": "user", "content": user_message}
                ]
            )
            astro_response = response['choices'][0]['message']['content'].strip()
            new_history = f"{chat_history}\nUser: {user_message}\nAstroBot: {astro_response}"
            return new_history
        except Exception as e:
            print(f"Error occurred: {e}")  # طباعة الخطأ في وحدة التحكم
            new_history = f"{chat_history}\nUser: {user_message}\nAstroBot: Error: {str(e)}"
            return new_history

    return chat_history


# تحديث القيم الحية للمؤشرات
@app.callback(
    [Output('battery-level', 'value'),
     Output('temperature-indicator', 'value'),
     Output('fuel-level', 'value'),
     Output('pressure-level', 'value'),
     Output('oxygen-level', 'value'),
     Output('solar-output', 'value'),
     Output('power-consumption', 'value'),
     Output('live-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_metrics(n_intervals):
    global current_battery, current_temperature, current_fuel, current_pressure, current_oxygen, current_solar_output, current_power

    # تحديث القيم بشكل تدريجي لتظهر حركة واقعية
    current_battery = max(0, min(100, current_battery + random.uniform(-1, 1)))
    current_temperature = max(-50, min(50, current_temperature + random.uniform(-1, 1)))
    current_fuel = max(0, min(100, current_fuel - random.uniform(0.1, 0.5)))
    current_pressure = max(0, min(200, current_pressure + random.uniform(-1, 1)))
    current_oxygen = max(0, min(100, current_oxygen + random.uniform(-1, 1)))
    current_solar_output = max(0, min(100, current_solar_output + random.uniform(-1, 1)))
    current_power = round(random.uniform(3.0, 8.0), 1)

    # إعداد الرسم البياني
    x_values = list(range(20))
    y_values = [random.randint(-50, 50) for _ in range(20)]
    figure = {
        'data': [
            go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines+markers',
                line={'shape': 'spline'},
                name='Temperature Variation'
            )
        ],
        'layout': go.Layout(
            title='Real-Time Temperature Variation',
            xaxis=dict(range=[min(x_values), max(x_values)]),
            yaxis=dict(range=[min(y_values), max(y_values)]),
            showlegend=True
        )
    }
    return current_battery, current_temperature, current_fuel, current_pressure, current_oxygen, current_solar_output, str(current_power), figure

if __name__ == '__main__':
    app.run_server(debug=True)
