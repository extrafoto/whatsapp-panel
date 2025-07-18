from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.contact import Contact
from datetime import datetime
import os
import json

sheets_bp = Blueprint('sheets', __name__)

@sheets_bp.route('/sheets/sync', methods=['POST'])
def sync_with_sheets():
    """Sincroniza os dados com o Google Sheets"""
    try:
        # TODO: Implementar integração real com Google Sheets API
        # Por enquanto, simula a sincronização
        
        contacts = Contact.query.all()
        
        # Simular leitura do Google Sheets
        sheets_data = get_sheets_data()
        
        # Atualizar status dos contatos baseado no Sheets
        updated_contacts = []
        for contact in contacts:
            sheets_status = sheets_data.get(contact.phone_number)
            if sheets_status and sheets_status != contact.status:
                contact.status = sheets_status
                contact.updated_at = datetime.utcnow()
                updated_contacts.append(contact)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'updated_contacts': len(updated_contacts),
                'contacts': [contact.to_dict() for contact in updated_contacts]
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sheets_bp.route('/sheets/update-status', methods=['POST'])
def update_status_in_sheets():
    """Atualiza o status de um contato no Google Sheets"""
    try:
        data = request.get_json()
        
        if not data.get('phone_number') or not data.get('status'):
            return jsonify({
                'success': False,
                'error': 'phone_number e status são obrigatórios'
            }), 400
        
        # TODO: Implementar integração real com Google Sheets API
        # Por enquanto, simula a atualização
        
        success = update_sheets_status(data['phone_number'], data['status'])
        
        if success:
            # Atualizar também no banco local
            contact = Contact.query.filter_by(phone_number=data['phone_number']).first()
            if contact:
                contact.status = data['status']
                contact.updated_at = datetime.utcnow()
                db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Status atualizado no Google Sheets'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Falha ao atualizar no Google Sheets'
            }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_sheets_data():
    """Função auxiliar para ler dados do Google Sheets"""
    # TODO: Implementar integração real com Google Sheets API
    # Por enquanto, retorna dados simulados
    
    return {
        '5511999999999': 'bot',
        '5511888888888': 'humano',
        '5511777777777': 'bot'
    }

def update_sheets_status(phone_number, status):
    """Função auxiliar para atualizar status no Google Sheets"""
    # TODO: Implementar integração real com Google Sheets API
    # Por enquanto, simula sucesso
    
    try:
        # Aqui seria feita a chamada para a API do Google Sheets
        # ou para um endpoint do n8n que faz essa atualização
        
        # Configurações do Google Sheets (devem vir de variáveis de ambiente)
        sheets_id = os.getenv('GOOGLE_SHEETS_ID', '')
        sheets_range = os.getenv('GOOGLE_SHEETS_RANGE', 'A:C')
        
        # Simular sucesso por enquanto
        return True
    except Exception as e:
        print(f"Erro ao atualizar Google Sheets: {e}")
        return False

