from flask import Blueprint, render_template

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

@main_bp.route('/hub')
def hub():
    return render_template('hub.html') 