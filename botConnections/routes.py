from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db, MarketingUser, BotConnectionLog, SocialConnection
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
import uuid

bot_bp = Blueprint('bot', __name__, template_folder='templates', static_folder='static')

@bot_bp.route('/')
@login_required
def dashboard():
    logs = BotConnectionLog.query.order_by(BotConnectionLog.timestamp.desc()).limit(15).all()
    
    # Ensure all required platforms exist for this user
    required_platforms = ['WhatsApp', 'Instagram', 'Telegram', 'Twitter', 'Gmail']
    current_connections = SocialConnection.query.filter_by(user_id=current_user.id).all()
    existing_platforms = [c.platform for c in current_connections]
    
    added_new = False
    for p in required_platforms:
        if p not in existing_platforms:
            conn = SocialConnection(platform=p, status='inactive', user_id=current_user.id)
            db.session.add(conn)
            added_new = True
    
    if added_new:
        db.session.commit()
    
    connections = SocialConnection.query.filter_by(user_id=current_user.id).all()
    return render_template('botConnections/dashboard.html', logs=logs, connections=connections)

@bot_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bot.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = MarketingUser.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('bot.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('botConnections/login.html')

@bot_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('bot.login'))

@bot_bp.route('/platform/connect/<string:platform>', methods=['POST'])
@login_required
def connect_platform(platform):
    conn = SocialConnection.query.filter_by(platform=platform, user_id=current_user.id).first()
    if conn:
        conn.status = 'linked'
        conn.account_name = f"MarketBot_{platform[:3].upper()}"
        conn.last_sync = datetime.utcnow()
        conn.auth_token = str(uuid.uuid4())
        
        # Log the action
        log = BotConnectionLog(
            platform=platform,
            action="Handshake Established",
            status="success",
            details=f"Successfully linked {platform} account: {conn.account_name}"
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({"status": "success", "account": conn.account_name})
    return jsonify({"status": "error", "message": "Platform not found"}), 404

@bot_bp.route('/twitter-automation')
@login_required
def twitter_automation():
    conn = SocialConnection.query.filter_by(platform='Twitter', user_id=current_user.id).first()
    return render_template('botConnections/twitter_handling.html', connection=conn)

@bot_bp.route('/gmail-automation')
@login_required
def gmail_automation():
    conn = SocialConnection.query.filter_by(platform='Gmail', user_id=current_user.id).first()
    return render_template('botConnections/gmail_handling.html', connection=conn)

@bot_bp.route('/n8n-launch')
@login_required
def n8n_launch():
    # Simulation of launching n8n tunnel
    log = BotConnectionLog(
        platform="n8n",
        action="Engine Startup",
        status="success",
        details="n8n core node initialized via local tunnel."
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({"status": "success", "url": "http://localhost:5678"})
