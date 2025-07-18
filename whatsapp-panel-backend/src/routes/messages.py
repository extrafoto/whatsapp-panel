from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.contact import Contact
from src.models.message import Message
from datetime import datetime
import requests
import os

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['POST'])
def send_message():
    """Envia uma mensagem via Z-API"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('contact_id') or not data.get('text'):
            return jsonify({
                'success': False,
                'error': 'contact_id e text são obrigatórios'
            }), 400
        
        # Buscar o contato
        contact = Contact.query.get_or_404(data['contact_id'])
        
        # Salvar a mensagem no banco local
        message = Message(
            contact_id=contact.id,
            direction='sent',
            text=data['text'],
            timestamp=datetime.utcnow()
        )
        
        # Atualizar timestamp da última mensagem do contato
        contact.last_message_timestamp = datetime.utcnow()
        
        db.session.add(message)
        db.session.commit()
        
        # Enviar via Z-API (simulado por enquanto)
        # TODO: Implementar integração real com Z-API
        zapi_response = send_to_zapi(contact.phone_number, data['text'])
        
        if not zapi_response['success']:
            # Se falhou no Z-API, remover a mensagem do banco
            db.session.delete(message)
            db.session.commit()
            return jsonify({
                'success': False,
                'error': 'Falha ao enviar mensagem via Z-API'
            }), 500
        
        return jsonify({
            'success': True,
            'data': message.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@messages_bp.route('/messages/receive', methods=['POST'])
def receive_message():
    """Webhook para receber mensagens do Z-API"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('phone_number') or not data.get('text'):
            return jsonify({
                'success': False,
                'error': 'phone_number e text são obrigatórios'
            }), 400
        
        # Buscar ou criar o contato
        contact = Contact.query.filter_by(phone_number=data['phone_number']).first()
        if not contact:
            contact = Contact(
                phone_number=data['phone_number'],
                name=data.get('name', ''),
                status='bot'
            )
            db.session.add(contact)
            db.session.flush()  # Para obter o ID
        
        # Salvar a mensagem recebida
        message = Message(
            contact_id=contact.id,
            direction='received',
            text=data['text'],
            timestamp=datetime.utcnow()
        )
        
        # Atualizar timestamp da última mensagem do contato
        contact.last_message_timestamp = datetime.utcnow()
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': message.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def send_to_zapi(phone_number, text):
    """Função auxiliar para enviar mensagem via Z-API"""
    # TODO: Implementar integração real com Z-API
    # Por enquanto, simula o envio
    
    # Configurações do Z-API (devem vir de variáveis de ambiente)
    zapi_url = os.getenv('ZAPI_URL', 'https://api.z-api.io/instances/YOUR_INSTANCE/token/YOUR_TOKEN/send-text')
    
    try:
        payload = {
            'phone': phone_number,
            'message': text
        }
        
        # Simular sucesso por enquanto
        # response = requests.post(zapi_url, json=payload, timeout=10)
        # return {'success': response.status_code == 200}
        
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

