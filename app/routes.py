from flask import Blueprint, render_template, jsonify, request, send_from_directory, send_file
from app.extensions import cache, limiter
import os
from app.ai_agent import get_latest_market_data, trading_agent, AI_ENABLED
import logging
from app.services.monitor import MonitoringService
from functools import wraps
from app.services.vpn_service import VPNService
import subprocess
import json

main = Blueprint('main', __name__)

# Admin authentication decorator
def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('X-Admin-Token')
        if not auth_token or auth_token != os.environ.get('ADMIN_TOKEN'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    platform = {
        'subtitle': 'Welcome to StreamAd Exchange',
        'description': 'Your gateway to interactive advertising and digital trading.',
        'features': [
            'Real-time Trading',
            'Live Streaming',
            'AI-Powered Learning',
            'Wellness Support'
        ],
        'highlights': [
            'Seamless Integration',
            'Advanced Analytics',
            'Secure Platform',
            '24/7 Support'
        ]
    }
    
    trading_hubs = {
        'Digital Market Hub': {
            'title': 'Digital Market Hub',
            'description': 'Access digital markets and trading opportunities.',
            'icon': '💹',
            'features': [
                'Real-time Trading',
                'Market Analysis',
                'Portfolio Management',
                'Investment Tools'
            ]
        },
        'Entertainment Hub': {
            'title': 'Entertainment Hub',
            'description': 'Stream content and earn rewards.',
            'icon': '🎬',
            'features': [
                'Live Streaming',
                'Exclusive Shows',
                'Reward System',
                'Interactive Content'
            ]
        },
        'Education Hub': {
            'title': 'Education Hub',
            'description': 'Learn and grow with AI-powered education.',
            'icon': '📚',
            'features': [
                'Trading Courses',
                'Market Education',
                'AI Learning',
                'Expert Tutorials'
            ]
        },
        'Wellness Center': {
            'title': 'Wellness Center',
            'description': 'AI-powered mental health support for traders.',
            'icon': '🧘',
            'features': [
                'Mental Health Support',
                'Stress Management',
                'Trading Psychology',
                'Wellness Resources'
            ]
        }
    }
    
    return render_template('index.html', 
                         platform=platform,
                         trading_hubs=trading_hubs,
                         background_image='background3.jpg')

@main.route('/services')
def services():
    page_info = {
        'title': 'Our Services',
        'subtitle': 'Discover Our Trading Hubs',
        'description': 'Explore our range of specialized trading and entertainment services.'
    }
    
    services = [
        {
            'title': 'Digital Market Hub',
            'description': 'Access digital markets and trading opportunities.',
            'icon': '💹',
            'features': ['Real-time Trading', 'Market Analysis', 'Portfolio Management']
        },
        # Add other services...
    ]
    
    return render_template('services.html', page_info=page_info, services=services)

@main.route('/service/<service_name>')
def service_detail(service_name):
    service = {
        'Digital Market Hub': {
            'tagline': 'Advanced Trading Platform',
            'description': 'Experience the future of digital trading with our advanced market hub.',
            'features': [
                'Real-time Analytics',
                'AI Trading Assistant',
                'Market Insights',
                'Portfolio Management',
                'Risk Analysis',
                'Trading Signals',
                'Performance Tracking',
                'Smart Alerts'
            ],
            'feature_descriptions': {
                'Real-time Analytics': 'Get instant market analysis and performance metrics with live data updates.',
                'AI Trading Assistant': 'Advanced AI algorithms help optimize your trading strategy and timing.',
                'Market Insights': 'Deep market analysis and trend predictions based on historical data.',
                'Portfolio Management': 'Comprehensive tools to manage and track your investment portfolio.',
                'Risk Analysis': 'Advanced risk assessment tools to protect your investments.',
                'Trading Signals': 'AI-powered trading signals to identify market opportunities.',
                'Performance Tracking': 'Detailed analytics to monitor your trading performance.',
                'Smart Alerts': 'Customizable alerts for price movements and market events.'
            },
            'feature_icons': {
                'Real-time Analytics': '📈',
                'AI Trading Assistant': '🤖',
                'Market Insights': '🔍',
                'Portfolio Management': '📊',
                'Risk Analysis': '🛡️',
                'Trading Signals': '📱',
                'Performance Tracking': '📉',
                'Smart Alerts': '🔔'
            }
        },
        'Entertainment Hub': {
            'tagline': 'Stream, Watch, and Earn',
            'description': 'Access exclusive content and earn while you watch.',
            'features': [
                'Live Streaming',
                'Exclusive Shows',
                'Reward System',
                'Interactive Content'
            ],
            'feature_descriptions': {
                'Live Streaming': 'Stream your favorite content in real-time with high-quality video.',
                'Exclusive Shows': 'Access premium content available only to our members.',
                'Reward System': 'Earn rewards and tokens while watching your favorite shows.',
                'Interactive Content': 'Engage with interactive features and live community events.'
            }
        },
        'Education Hub': {
            'tagline': 'AI-Powered Learning Platform',
            'description': 'Access comprehensive learning resources and personalized education.',
            'features': [
                'Trading Courses',
                'Market Education',
                'AI Learning',
                'Expert Tutorials'
            ],
            'feature_descriptions': {
                'Trading Courses': 'Comprehensive courses designed by industry experts.',
                'Market Education': 'In-depth market analysis and trading strategies.',
                'AI Learning': 'Personalized learning paths adapted to your progress.',
                'Expert Tutorials': 'Step-by-step guides from professional traders.'
            }
        },
        'Wellness Center': {
            'tagline': 'Support for Your Trading Journey',
            'description': 'Access mental health and wellness resources designed for traders.',
            'features': [
                'Mental Health Support',
                'Stress Management',
                'Trading Psychology',
                'Wellness Resources'
            ],
            'feature_descriptions': {
                'Mental Health Support': 'Professional support for maintaining mental well-being.',
                'Stress Management': 'Tools and techniques for managing trading stress.',
                'Trading Psychology': 'Understanding and improving your trading mindset.',
                'Wellness Resources': 'Comprehensive resources for overall trader wellness.'
            },
            'feature_icons': {
                'Mental Health Support': '🧠',
                'Stress Management': '🌿',
                'Trading Psychology': '🎯',
                'Wellness Resources': '🌟'
            }
        }
    }

    detail = service.get(service_name, {}).get('description', 'Service details not available.')
    features = service.get(service_name, {}).get('features', [])
    
    return render_template('service_detail.html',
                         service_name=service_name,
                         service=service.get(service_name, {}),
                         detail=detail,
                         features=features)

@main.route('/about')
def about():
    return render_template('about.html') 

@main.route('/service/Digital Market Hub/data')
@cache.cached(timeout=5)
def market_data():
    try:
        data = get_latest_market_data()
        if data:
            response = {
                'price': round(float(data.price), 2),
                'volume': int(data.volume),
                'prediction': str(data.prediction),
                'confidence': round(float(data.confidence) * 100, 1),
                'timestamp': str(data.timestamp),
                'status': 'success',
                'mode': 'AI' if AI_ENABLED else 'Fallback'
            }
            logger.debug(f"Market data response: {response}")
            return jsonify(response)
            
        return jsonify({
            'error': 'No data available',
            'status': 'no_data',
            'mode': 'AI' if AI_ENABLED else 'Fallback'
        })
    except Exception as e:
        logger.error(f"Error in market_data route: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error',
            'mode': 'AI' if AI_ENABLED else 'Fallback'
        }), 500 

@main.route('/api/monitor/status')
@require_admin
def monitor_status():
    monitor = MonitoringService.get_instance()
    return jsonify({
        'status': monitor.status,
        'failover_active': monitor._monitor.failover_active if monitor._monitor else False,
        'consecutive_failures': monitor._monitor.consecutive_failures if monitor._monitor else 0,
        'last_check': monitor._monitor.last_check_time if monitor._monitor else None
    })

@main.route('/api/monitor/start', methods=['POST'])
@require_admin
def start_monitor():
    try:
        monitor = MonitoringService.get_instance()
        monitor.start()
        return jsonify({
            'message': 'Monitoring service started',
            'status': monitor.status
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@main.route('/api/monitor/stop', methods=['POST'])
@require_admin
def stop_monitor():
    try:
        monitor = MonitoringService.get_instance()
        monitor.stop()
        return jsonify({
            'message': 'Monitoring service stopped',
            'status': monitor.status
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500 

# VPN Management Routes
@main.route('/api/vpn/status')
@require_admin
def vpn_status():
    vpn = VPNService()
    return jsonify(vpn.get_status())

@main.route('/api/vpn/start', methods=['POST'])
@require_admin
def vpn_start():
    vpn = VPNService()
    if vpn.start_server():
        return jsonify({'status': 'success', 'message': 'VPN server started'})
    return jsonify({'status': 'error', 'message': 'Failed to start VPN server'}), 500

@main.route('/api/vpn/stop', methods=['POST'])
@require_admin
def vpn_stop():
    vpn = VPNService()
    if vpn.stop_server():
        return jsonify({'status': 'success', 'message': 'VPN server stopped'})
    return jsonify({'status': 'error', 'message': 'Failed to stop VPN server'}), 500

@main.route('/api/vpn/clients', methods=['GET'])
@require_admin
def list_vpn_clients():
    vpn = VPNService()
    return jsonify({
        'clients': vpn.config['clients'],
        'total': len(vpn.config['clients'])
    })

@main.route('/api/vpn/clients/<client_name>', methods=['POST'])
@require_admin
def create_vpn_client(client_name):
    vpn = VPNService()
    if vpn.generate_client_config(client_name):
        return jsonify({
            'status': 'success',
            'message': f'Client {client_name} created successfully',
            'config_path': f'vpn/clients/{client_name}/{client_name}.ovpn'
        })
    return jsonify({
        'status': 'error',
        'message': f'Failed to create client {client_name}'
    }), 500

@main.route('/api/vpn/clients/<client_name>/config', methods=['GET'])
@require_admin
def download_client_config(client_name):
    config_path = f'vpn/clients/{client_name}/{client_name}.ovpn'
    try:
        return send_file(
            config_path,
            as_attachment=True,
            download_name=f'{client_name}.ovpn'
        )
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Config file not found for {client_name}'
        }), 404 

@main.route('/vpn/dashboard')
@require_admin
def vpn_dashboard():
    return render_template('vpn_dashboard.html') 

@main.route('/api/vpn/clients/<client_name>/stats')
@require_admin
def get_client_stats(client_name):
    vpn = VPNService()
    return jsonify(vpn.get_client_stats(client_name))

@main.route('/api/vpn/clients/<client_name>/revoke', methods=['POST'])
@require_admin
def revoke_client(client_name):
    vpn = VPNService()
    if vpn.revoke_client(client_name):
        return jsonify({
            'status': 'success',
            'message': f'Client {client_name} revoked successfully'
        })
    return jsonify({
        'status': 'error',
        'message': f'Failed to revoke client {client_name}'
    }), 500 

@main.route('/api/status')
@require_admin
def system_status():
    try:
        # Run the monitor script with JSON output
        result = subprocess.run(
            ['python', 'scripts/monitor_dashboard.py', '--json'],
            capture_output=True,
            text=True
        )
        return jsonify(json.loads(result.stdout))
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 