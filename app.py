
from dash import Dash, dcc, html, Input, Output, State
import dash_daq as daq
import plotly.graph_objs as go
import random
import openai

# إعداد مفتاح OpenAI
openai.api_key = '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'

app = Dash(__name__)

# تصميم الواجهة الأساسية
app.layout = html.Div([
    html.H1("AstroBot AI - Intelligent Satellite Maintenance System", style={'textAlign': 'center', 'color': '#007ACC', 'fontFamily': 'Arial', 'marginTop': '20px'}),

    # مؤشرات النظام
    html.Div([
        html.Div([
            daq.Gauge(
                id='battery-level',
                label="Battery Level",
                value=85,
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
                value=40,
                min=0,
                max=100,
                height=200,
                color="#FF5E5E"
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            daq.LEDDisplay(
                id='power-consumption',
                label="Power Consumption (kW)",
                value="5.4",
                color="#92e0d3",
                size=50
            )
        ], style={'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            daq.Indicator(
                id='signal-strength',
                label="Signal Strength",
                value=True,
                color="#33FF57"
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
        html.Div([
            html.H3("Chat Interface", style={'textAlign': 'center', 'color': '#007ACC', 'fontFamily': 'Arial'}),
            dcc.Textarea(
                id='chat-history',
                value='AstroBot: Hello, how can I assist you today?',
                style={'width': '100%', 'height': 300, 'borderRadius': '10px', 'border': '2px solid #007ACC', 'padding': '10px', 'fontFamily': 'Courier New'}
            ),
            dcc.Input(
                id='user-input',
                type='text',
                placeholder='Type your message here...',
                style={'width': '80%', 'borderRadius': '5px', 'padding': '10px', 'border': '2px solid #007ACC', 'fontFamily': 'Arial'}
            ),
            html.Button('Send', id='send-button', n_clicks=0, style={'width': '15%', 'marginLeft': '5px', 'backgroundColor': '#007ACC', 'color': '#ffffff', 'border': 'none', 'padding': '10px', 'borderRadius': '5px'}),
        ], style={'padding': '20px', 'width': '50%', 'margin': '0 auto', 'backgroundColor': '#e6f7ff', 'borderRadius': '10px', 'border': '1px solid #007ACC'})
    ], style={'padding': '30px', 'backgroundColor': '#f0f0f0'}),

    dcc.Interval(
        id='interval-component',
        interval=2000,  # تحديث كل 2 ثانية
        n_intervals=0
    )
])

# تحديث البيانات الحية للمؤشرات
@app.callback(
    [Output('battery-level', 'value'),
     Output('temperature-indicator', 'value'),
     Output('power-consumption', 'value'),
     Output('signal-strength', 'value'),
     Output('live-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_metrics(n_intervals):
    battery_level = random.randint(50, 100)
    temperature = random.uniform(20, 80)
    power_consumption = str(round(random.uniform(3.0, 8.0), 1))
    signal_strength = random.choice([True, False])

    # إعداد الرسم البياني
    x_values = list(range(20))
    y_values = [random.randint(20, 80) for _ in range(20)]
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
    return battery_level, temperature, power_consumption, signal_strength, figure


# دالة لتحليل المدخلات وتقديم الردود التفاعلية
def get_system_response(user_input, battery_level, temperature, power_consumption, signal_strength):
    if "battery" in user_input.lower():
        return f"The current battery level is {battery_level}%."
    elif "temperature" in user_input.lower():
        return f"The current temperature is {temperature:.2f}°C."
    elif "power" in user_input.lower():
        return f"The power consumption is {power_consumption} kW."
    elif "signal" in user_input.lower():
        return f"The signal strength is {'Strong' if signal_strength else 'Weak'}."
    else:
        return "I'm not able to provide real-time information on that. Please ask about battery, temperature, power, or signal strength."


# تكامل GPT-4 مع واجهة الدردشة وتقديم ردود بناءً على المعلومات الحية
@app.callback(
    [Output('chat-history', 'value'), Output('user-input', 'value')],
    [Input('send-button', 'n_clicks'), Input('battery-level', 'value'), Input('temperature-indicator', 'value'), 
     Input('power-consumption', 'value'), Input('signal-strength', 'value')],
    [State('user-input', 'value'), State('chat-history', 'value')]
)
def update_chat(n_clicks, battery_level, temperature, power_consumption, signal_strength, user_input, chat_history):
    if n_clicks > 0 and user_input:
        # تقديم ردود مخصصة بناءً على المحتوى المدخل
        system_response = get_system_response(user_input, battery_level, temperature, power_consumption, signal_strength)
        chat_history += f"You: {user_input}\nAstroBot: {system_response}\n"
        return chat_history, ""
    return chat_history, ""


if __name__ == '__main__':
    app.run_server(debug=True)
