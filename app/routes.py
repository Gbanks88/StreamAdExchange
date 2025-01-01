from flask import Blueprint, render_template, jsonify, request
from .fetch_ai_utils import FetchAIManager

# Create the blueprint
main = Blueprint('main', __name__)
fetch_ai = FetchAIManager()

@main.route('/')
def index():
    platform = {
        'subtitle': 'Your Gateway to Smart Trading',
        'features': ['Real-time Analytics', 'Expert Community', 'Advanced Tools']
    }
    
    trading_hubs = {
        'educational_hub': {
            'icon': '📚',
            'title': 'Educational Hub',
            'description': 'Learn trading strategies and market analysis',
            'features': ['Expert Courses', 'Live Workshops', 'Trading Resources']
        },
        'virtual_trading_floor': {
            'icon': '📊',
            'title': 'Trading Floor',
            'description': 'Experience real-time trading simulation',
            'features': ['Live Markets', 'Practice Trading', 'Real-time Data']
        },
        'community_engagement': {
            'icon': '👥',
            'title': 'Community',
            'description': 'Connect with fellow traders and experts',
            'features': ['Discussion Forums', 'Live Chat', 'Expert Networks']
        },
        'entertainment': {
            'icon': '🎮',
            'title': 'Entertainment',
            'description': 'Enjoy trading-related content and games',
            'features': ['Trading Games', 'Live Streams', 'Educational Videos']
        },
        'wellness_center': {
            'icon': '🧘',
            'title': 'Wellness Center',
            'description': 'Maintain trading psychology and wellbeing',
            'features': ['Stress Management', 'Mental Health', 'Work-Life Balance']
        },
        'financial_tools': {
            'icon': '🔧',
            'title': 'Financial Tools',
            'description': 'Access advanced trading and analysis tools',
            'features': ['Technical Analysis', 'Risk Calculator', 'Portfolio Tracker']
        },
        'meet_your_demand': {
            'icon': '🎯',
            'title': 'Meet Your Demand',
            'description': 'Customize solutions for your trading needs',
            'features': ['Custom Solutions', 'Personal Support', 'Tailored Plans']
        }
    }
    
    return render_template('index.html', platform=platform, trading_hubs=trading_hubs)

@main.route('/educational-hub')
def educational_hub():
    return render_template('educational_hub.html')

@main.route('/virtual-trading-floor')
def virtual_trading_floor():
    return render_template('virtual_trading_floor.html')

@main.route('/community-engagement')
def community_engagement():
    return render_template('community_engagement.html')

@main.route('/entertainment')
def entertainment():
    return render_template('entertainment.html')

@main.route('/wellness-center')
def wellness_center():
    return render_template('wellness_center.html')

@main.route('/meet-your-demand')
def meet_your_demand():
    return render_template('meet_your_demand.html')

@main.route('/financial-tools')
def financial_tools():
    return render_template('financial_tools.html')

@main.route('/ai-analysis', methods=['POST'])
def ai_analysis():
    data = request.json
    analysis = fetch_ai.analyze_market_data(data)
    return jsonify(analysis)

@main.route('/create-ai-agent', methods=['POST'])
def create_ai_agent():
    strategy_params = request.json
    agent = fetch_ai.create_trading_agent(strategy_params)
    return jsonify(agent)

@main.route('/market-predictions/<asset_id>')
def market_predictions(asset_id):
    predictions = fetch_ai.get_market_predictions(asset_id)
    return jsonify(predictions) 