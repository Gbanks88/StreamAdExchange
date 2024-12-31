from flask import Blueprint, render_template, jsonify
from .api_services import MarketDataService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/services')
def services():
    return render_template('services.html')

@main_bp.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')

@main_bp.route('/education')
def education():
    return render_template('education.html')

@main_bp.route('/community')
def community():
    return render_template('community.html')

@main_bp.route('/premium')
def premium():
    return render_template('premium.html')

@main_bp.route('/learning-hub')
def hub():
    return render_template('hub.html')

@main_bp.route('/virtual-trading-floor')
def virtual_trading_floor():
    return render_template('virtual_trading_floor.html')

@main_bp.route('/digital-marketplace')
def digital_marketplace():
    return render_template('digital_marketplace.html')

@main_bp.route('/educational-hub')
def educational_hub():
    return render_template('educational_hub.html')

@main_bp.route('/wellness-center')
def wellness_center():
    return render_template('wellness_center.html')

@main_bp.route('/community-engagement')
def community_engagement():
    return render_template('community_engagement.html')

@main_bp.route('/financial-tools')
def financial_tools():
    return render_template('financial_tools.html')

@main_bp.route('/entertainment')
def entertainment():
    return render_template('entertainment.html')

@main_bp.route('/api/market-data/<symbol>')
def get_market_data(symbol):
    market_service = MarketDataService()
    
    if '/' in symbol:  # Forex pair
        data = market_service.get_forex_data(symbol)
    elif symbol.startswith('BTC') or symbol.startswith('ETH'):  # Crypto
        data = market_service.get_crypto_data(symbol)
    else:  # Stock
        data = market_service.get_stock_data(symbol)
    
    return jsonify(data) 