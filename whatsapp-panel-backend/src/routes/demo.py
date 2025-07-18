from flask import Blueprint, jsonify
from src.models.user import db
from src.models.contact import Contact
from src.models.message import Message
from datetime import datetime, timedelta

demo_bp = Blueprint('demo', __name__)

@demo_bp.route('/demo/populate', methods=['POST'])
def populate_demo_data():
    """Popula o banco com dados de demonstração"""
    try:
        # Limpar dados existentes
        Message.query.delete()
        Contact.query.delete()
        
        # Criar contatos de demonstração
        contacts_data = [
            {
                'phone_number': '5511999999999',
                'name': 'João Silva',
                'status': 'bot'
            },
            {
                'phone_number': '5511888888888',
                'name': 'Maria Santos',
                'status': 'humano'
            },
            {
                'phone_number': '5511777777777',
                'name': 'Pedro Costa',
                'status': 'bot'
            },
            {
                'phone_number': '5511666666666',
                'name': 'Ana Oliveira',
                'status': 'humano'
            }
        ]
        
        contacts = []
        for contact_data in contacts_data:
            contact = Contact(
                phone_number=contact_data['phone_number'],
                name=contact_data['name'],
                status=contact_data['status'],
                last_message_timestamp=datetime.utcnow() - timedelta(minutes=30)
            )
            db.session.add(contact)
            contacts.append(contact)
        
        db.session.flush()  # Para obter os IDs dos contatos
        
        # Criar mensagens de demonstração
        messages_data = [
            # Mensagens para João Silva
            {
                'contact_id': contacts[0].id,
                'direction': 'received',
                'text': 'Olá, preciso de ajuda com meu pedido',
                'timestamp': datetime.utcnow() - timedelta(minutes=30)
            },
            {
                'contact_id': contacts[0].id,
                'direction': 'sent',
                'text': 'Olá! Como posso ajudá-lo?',
                'timestamp': datetime.utcnow() - timedelta(minutes=29)
            },
            {
                'contact_id': contacts[0].id,
                'direction': 'received',
                'text': 'Meu pedido não chegou ainda',
                'timestamp': datetime.utcnow() - timedelta(minutes=28)
            },
            {
                'contact_id': contacts[0].id,
                'direction': 'sent',
                'text': 'Vou verificar o status do seu pedido agora mesmo!',
                'timestamp': datetime.utcnow() - timedelta(minutes=27)
            },
            
            # Mensagens para Maria Santos
            {
                'contact_id': contacts[1].id,
                'direction': 'received',
                'text': 'Boa tarde! Gostaria de saber sobre os produtos',
                'timestamp': datetime.utcnow() - timedelta(hours=1)
            },
            {
                'contact_id': contacts[1].id,
                'direction': 'sent',
                'text': 'Boa tarde! Temos várias opções disponíveis. O que você procura?',
                'timestamp': datetime.utcnow() - timedelta(hours=1, minutes=-1)
            },
            {
                'contact_id': contacts[1].id,
                'direction': 'received',
                'text': 'Estou interessada em notebooks',
                'timestamp': datetime.utcnow() - timedelta(minutes=58)
            },
            
            # Mensagens para Pedro Costa
            {
                'contact_id': contacts[2].id,
                'direction': 'received',
                'text': 'Olá, como faço para cancelar meu pedido?',
                'timestamp': datetime.utcnow() - timedelta(hours=2)
            },
            {
                'contact_id': contacts[2].id,
                'direction': 'sent',
                'text': 'Para cancelar seu pedido, preciso do número do pedido. Pode me informar?',
                'timestamp': datetime.utcnow() - timedelta(hours=2, minutes=-2)
            },
            
            # Mensagens para Ana Oliveira
            {
                'contact_id': contacts[3].id,
                'direction': 'received',
                'text': 'Bom dia! Vocês fazem entrega no interior?',
                'timestamp': datetime.utcnow() - timedelta(hours=3)
            },
            {
                'contact_id': contacts[3].id,
                'direction': 'sent',
                'text': 'Bom dia! Sim, fazemos entrega para todo o Brasil. Para qual cidade seria?',
                'timestamp': datetime.utcnow() - timedelta(hours=3, minutes=-1)
            }
        ]
        
        for message_data in messages_data:
            message = Message(
                contact_id=message_data['contact_id'],
                direction=message_data['direction'],
                text=message_data['text'],
                timestamp=message_data['timestamp']
            )
            db.session.add(message)
            
            # Atualizar o timestamp da última mensagem do contato
            contact = Contact.query.get(message_data['contact_id'])
            if contact:
                contact.last_message_timestamp = message_data['timestamp']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Dados de demonstração criados com sucesso',
            'data': {
                'contacts_created': len(contacts),
                'messages_created': len(messages_data)
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@demo_bp.route('/demo/clear', methods=['POST'])
def clear_demo_data():
    """Limpa todos os dados de demonstração"""
    try:
        Message.query.delete()
        Contact.query.delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Dados de demonstração removidos com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

