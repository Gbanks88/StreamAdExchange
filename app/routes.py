from flask import Blueprint, render_template
from ad_manager import AdManager

main_bp = Blueprint('main', __name__)
ad_manager = AdManager()

@main_bp.route('/')
def home():
    return render_template('home.html', title='Home')

@main_bp.route('/marketplace')
def marketplace():
    active_ads = ad_manager.get_active_ads()
    return render_template('marketplace.html', 
                         title='Marketplace',
                         active_ads=active_ads,
                         total_count=len(active_ads))

@main_bp.route('/entertainment')
def entertainment():
    return render_template('entertainment.html', title='Entertainment')

@main_bp.route('/financial')
def financial():
    return render_template('financial.html', title='Financial Tools')

@main_bp.route('/education')
def education():
    return render_template('education.html', title='Education')

@main_bp.route('/mental-health')
def mental_health():
    return render_template('mental_health.html', title='Mental Health')

@main_bp.route('/community')
def community():
    return render_template('community.html', title='Community') 