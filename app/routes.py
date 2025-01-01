from flask import Blueprint, render_template, jsonify, redirect, url_for
from app.api_services import MarketDataService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Add platform and trading hubs data
    platform_data = {
        'subtitle': 'Your Gateway to Smart Trading',
        'description': 'Experience the future of trading with our innovative platform combining AI, education, and community.',
        'features': ['Live Trading', 'AI Analysis', 'Educational Resources', 'Community Support']
    }
    
    trading_hubs = {
        'virtual_trading_floor': {
            'icon': '📊',
            'title': 'Virtual Trading Floor',
            'description': 'Experience real-time trading in a risk-free environment',
            'features': ['Live Market Data', 'Practice Trading', 'Performance Analytics']
        },
        'digital_marketplace': {
            'icon': '🏪',
            'title': 'Digital Marketplace',
            'description': 'Explore and invest in diverse digital assets',
            'features': ['Stocks', 'Crypto', 'NFTs', 'Real Estate']
        },
        'educational_hub': {
            'icon': '📚',
            'title': 'Educational Hub',
            'description': 'Learn trading strategies and financial concepts',
            'features': ['Courses', 'Tutorials', 'Expert Insights']
        },
        'wellness_center': {
            'icon': '🧘',
            'title': 'Wellness Center',
            'description': 'Maintain balance in your trading journey',
            'features': ['Stress Management', 'Trading Psychology', 'Health Tips']
        },
        'community_engagement': {
            'icon': '👥',
            'title': 'Community',
            'description': 'Connect with fellow traders and experts',
            'features': ['Forums', 'Live Chat', 'Events']
        },
        'financial_tools': {
            'icon': '🛠️',
            'title': 'Financial Tools',
            'description': 'Access professional trading tools and analytics',
            'features': ['Technical Analysis', 'Portfolio Management', 'Risk Calculator']
        },
        'entertainment': {
            'icon': '🎮',
            'title': 'Entertainment',
            'description': 'Learn while having fun',
            'features': ['Trading Games', 'Educational Videos', 'Podcasts']
        }
    }
    
    return render_template('index.html', 
                         platform=platform_data,
                         trading_hubs=trading_hubs)

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

@main_bp.route('/service/<service_name>')
def service_detail(service_name):
    # Map service names to their respective routes
    service_routes = {
        'Virtual Trading Floor': 'virtual_trading_floor',
        'Digital Marketplace': 'digital_marketplace',
        'Educational Hub': 'educational_hub',
        'Wellness Center': 'wellness_center',
        'Community': 'community_engagement',
        'Financial Tools': 'financial_tools',
        'Entertainment': 'entertainment'
    }
    
    route = service_routes.get(service_name)
    if route:
        return redirect(url_for(f'main.{route}'))
    return redirect(url_for('main.home')) 

@main_bp.route('/meet-your-demand')
def meet_your_demand():
    return render_template('meet_your_demand.html') 

@main_bp.route('/company-partnerships')
def company_partnerships():
    return render_template('company_partnerships.html') 