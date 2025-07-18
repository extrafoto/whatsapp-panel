from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.contact import Contact
from src.models.message import Message
from datetime import datetime

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/contacts', methods=['GET'])
def get_contacts():
    """Retorna todos os contatos"""
    try:
        contacts = Contact.query.order_by(Contact.last_message_timestamp.desc()).all()
        return jsonify({
            'success': True,
            'data': [contact.to_dict() for contact in contacts]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@contacts_bp.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Retorna um contato específico"""
    try:
        contact = Contact.query.get_or_404(contact_id)
        return jsonify({
            'success': True,
            'data': contact.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@contacts_bp.route('/contacts', methods=['POST'])
def create_contact():
    """Cria um novo contato"""
    try:
        data = request.get_json()
        
        # Verificar se o contato já existe
        existing_contact = Contact.query.filter_by(phone_number=data['phone_number']).first()
        if existing_contact:
            return jsonify({
                'success': False,
                'error': 'Contato já existe'
            }), 400
        
        contact = Contact(
            phone_number=data['phone_number'],
            name=data.get('name', ''),
            status=data.get('status', 'bot')
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': contact.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@contacts_bp.route('/contacts/<int:contact_id>/status', methods=['PUT'])
def update_contact_status(contact_id):
    """Atualiza o status do bot para um contato"""
    try:
        contact = Contact.query.get_or_404(contact_id)
        data = request.get_json()
        
        if 'status' not in data or data['status'] not in ['bot', 'humano']:
            return jsonify({
                'success': False,
                'error': 'Status deve ser "bot" ou "humano"'
            }), 400
        
        contact.status = data['status']
        contact.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': contact.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@contacts_bp.route('/contacts/<int:contact_id>/messages', methods=['GET'])
def get_contact_messages(contact_id):
    """Retorna todas as mensagens de um contato"""
    try:
        contact = Contact.query.get_or_404(contact_id)
        messages = Message.query.filter_by(contact_id=contact_id).order_by(Message.timestamp.asc()).all()
        
        return jsonify({
            'success': True,
            'data': {
                'contact': contact.to_dict(),
                'messages': [message.to_dict() for message in messages]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

