from flask import Blueprint, render_template, jsonify, request, send_from_directory
from app.extensions import cache, limiter
import os

main = Blueprint('main', __name__)

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
            'tagline': 'Your gateway to digital markets and trading opportunities',
            'description': 'Access real-time trading, market analysis, and portfolio management tools.',
            'features': [
                'Real-time Trading',
                'Market Analysis',
                'Portfolio Management',
                'Investment Tools',
                'Trading Signals',
                'Risk Management'
            ]
        },
        'Entertainment Hub': {
            'tagline': 'Stream, watch, and earn rewards',
            'description': 'Access exclusive content and earn while you watch.',
            'features': [
                'Live Streaming',
                'Exclusive Shows',
                'Reward System',
                'Interactive Content'
            ]
        },
        'Education Hub': {
            'tagline': 'Learn and grow with AI-powered education',
            'description': 'Access comprehensive learning resources and personalized education.',
            'features': [
                'Trading Courses',
                'Market Education',
                'AI Learning',
                'Expert Tutorials'
            ]
        },
        'Wellness Center': {
            'tagline': 'Support for your trading journey',
            'description': 'Access mental health and wellness resources designed for traders.',
            'features': [
                'Mental Health Support',
                'Stress Management',
                'Trading Psychology',
                'Wellness Resources'
            ]
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