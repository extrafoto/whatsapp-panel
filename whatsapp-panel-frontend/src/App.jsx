import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Switch } from '@/components/ui/switch.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { MessageCircle, Send, Bot, User, Phone, RefreshCw } from 'lucide-react'
import ApiService from './services/api.js'
import './App.css'

function App() {
  const [contacts, setContacts] = useState([])
  const [selectedContact, setSelectedContact] = useState(null)
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Carregar contatos
  const loadContacts = async () => {
    try {
      setLoading(true)
      const response = await ApiService.getContacts()
      if (response.success) {
        setContacts(response.data)
      }
    } catch (error) {
      console.error('Erro ao carregar contatos:', error)
      setError('Erro ao carregar contatos')
      // Fallback para dados simulados se a API não estiver disponível
      const mockContacts = [
        {
          id: 1,
          phone_number: '5511999999999',
          name: 'João Silva',
          status: 'bot',
          last_message_timestamp: new Date().toISOString()
        },
        {
          id: 2,
          phone_number: '5511888888888',
          name: 'Maria Santos',
          status: 'humano',
          last_message_timestamp: new Date(Date.now() - 3600000).toISOString()
        },
        {
          id: 3,
          phone_number: '5511777777777',
          name: 'Pedro Costa',
          status: 'bot',
          last_message_timestamp: new Date(Date.now() - 7200000).toISOString()
        }
      ]
      setContacts(mockContacts)
    } finally {
      setLoading(false)
    }
  }

  // Carregar mensagens de um contato
  const loadMessages = async (contactId) => {
    try {
      const response = await ApiService.getContactMessages(contactId)
      if (response.success) {
        setMessages(response.data.messages)
      }
    } catch (error) {
      console.error('Erro ao carregar mensagens:', error)
      // Fallback para dados simulados
      const mockMessages = [
        {
          id: 1,
          contact_id: contactId,
          direction: 'received',
          text: 'Olá, preciso de ajuda com meu pedido',
          timestamp: new Date(Date.now() - 1800000).toISOString()
        },
        {
          id: 2,
          contact_id: contactId,
          direction: 'sent',
          text: 'Olá! Como posso ajudá-lo?',
          timestamp: new Date(Date.now() - 1700000).toISOString()
        },
        {
          id: 3,
          contact_id: contactId,
          direction: 'received',
          text: 'Meu pedido não chegou ainda',
          timestamp: new Date(Date.now() - 1600000).toISOString()
        }
      ]
      setMessages(mockMessages)
    }
  }

  useEffect(() => {
    loadContacts()
  }, [])

  useEffect(() => {
    if (selectedContact) {
      loadMessages(selectedContact.id)
    }
  }, [selectedContact])

  const handleStatusToggle = async (contactId, newStatus) => {
    try {
      const status = newStatus ? 'humano' : 'bot'
      const contact = contacts.find(c => c.id === contactId)
      
      // Atualizar localmente primeiro
      setContacts(contacts.map(contact => 
        contact.id === contactId 
          ? { ...contact, status }
          : contact
      ))

      // Atualizar no backend
      await ApiService.updateContactStatus(contactId, status)
      
      // Atualizar no Google Sheets
      if (contact) {
        await ApiService.updateStatusInSheets(contact.phone_number, status)
      }
    } catch (error) {
      console.error('Erro ao atualizar status:', error)
      setError('Erro ao atualizar status do bot')
      // Reverter mudança local em caso de erro
      loadContacts()
    }
  }

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !selectedContact) return

    try {
      setLoading(true)
      
      // Adicionar mensagem localmente primeiro
      const tempMessage = {
        id: Date.now(),
        contact_id: selectedContact.id,
        direction: 'sent',
        text: newMessage,
        timestamp: new Date().toISOString()
      }
      
      setMessages([...messages, tempMessage])
      setNewMessage('')

      // Enviar via API
      const response = await ApiService.sendMessage(selectedContact.id, newMessage)
      
      if (response.success) {
        // Recarregar mensagens para obter a mensagem com ID correto
        loadMessages(selectedContact.id)
      }
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error)
      setError('Erro ao enviar mensagem')
    } finally {
      setLoading(false)
    }
  }

  const handleSyncSheets = async () => {
    try {
      setLoading(true)
      const response = await ApiService.syncWithSheets()
      if (response.success) {
        loadContacts() // Recarregar contatos após sincronização
        setError('')
      }
    } catch (error) {
      console.error('Erro ao sincronizar com Sheets:', error)
      setError('Erro ao sincronizar com Google Sheets')
    } finally {
      setLoading(false)
    }
  }

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Lista de Contatos */}
      <div className="w-1/3 bg-white border-r border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <h1 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
              <MessageCircle className="w-6 h-6 text-green-600" />
              Painel WhatsApp
            </h1>
            <Button
              variant="outline"
              size="sm"
              onClick={handleSyncSheets}
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </Button>
          </div>
          {error && (
            <div className="text-sm text-red-600 bg-red-50 p-2 rounded">
              {error}
            </div>
          )}
        </div>
        
        <ScrollArea className="h-[calc(100vh-120px)]">
          {contacts.map((contact) => (
            <div
              key={contact.id}
              className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition-colors ${
                selectedContact?.id === contact.id ? 'bg-blue-50 border-blue-200' : ''
              }`}
              onClick={() => setSelectedContact(contact)}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-gray-600" />
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{contact.name}</h3>
                    <p className="text-sm text-gray-500 flex items-center gap-1">
                      <Phone className="w-3 h-3" />
                      {contact.phone_number}
                    </p>
                  </div>
                </div>
                <Badge variant={contact.status === 'bot' ? 'default' : 'secondary'}>
                  {contact.status === 'bot' ? (
                    <><Bot className="w-3 h-3 mr-1" /> Bot</>
                  ) : (
                    <><User className="w-3 h-3 mr-1" /> Humano</>
                  )}
                </Badge>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">
                  {formatTime(contact.last_message_timestamp)}
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500">
                    {contact.status === 'bot' ? 'Automático' : 'Manual'}
                  </span>
                  <Switch
                    checked={contact.status === 'humano'}
                    onCheckedChange={(checked) => handleStatusToggle(contact.id, checked)}
                    size="sm"
                  />
                </div>
              </div>
            </div>
          ))}
        </ScrollArea>
      </div>

      {/* Área de Conversa */}
      <div className="flex-1 flex flex-col">
        {selectedContact ? (
          <>
            {/* Header da Conversa */}
            <div className="p-4 bg-white border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-gray-600" />
                  </div>
                  <div>
                    <h2 className="font-semibold text-gray-900">{selectedContact.name}</h2>
                    <p className="text-sm text-gray-500">{selectedContact.phone_number}</p>
                  </div>
                </div>
                
                <Card className="p-3">
                  <div className="flex items-center gap-2">
                    {selectedContact.status === 'bot' ? (
                      <Bot className="w-4 h-4 text-blue-600" />
                    ) : (
                      <User className="w-4 h-4 text-green-600" />
                    )}
                    <span className="text-sm font-medium">
                      {selectedContact.status === 'bot' ? 'Bot Ativo' : 'Atendimento Manual'}
                    </span>
                    <Switch
                      checked={selectedContact.status === 'humano'}
                      onCheckedChange={(checked) => handleStatusToggle(selectedContact.id, checked)}
                    />
                  </div>
                </Card>
              </div>
            </div>

            {/* Mensagens */}
            <ScrollArea className="flex-1 p-4">
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.direction === 'sent' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.direction === 'sent'
                          ? 'bg-green-500 text-white'
                          : 'bg-white border border-gray-200 text-gray-900'
                      }`}
                    >
                      <p className="text-sm">{message.text}</p>
                      <p className={`text-xs mt-1 ${
                        message.direction === 'sent' ? 'text-green-100' : 'text-gray-500'
                      }`}>
                        {formatTime(message.timestamp)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>

            {/* Campo de Envio */}
            <div className="p-4 bg-white border-t border-gray-200">
              <div className="flex gap-2">
                <Input
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Digite sua mensagem..."
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  className="flex-1"
                  disabled={loading}
                />
                <Button 
                  onClick={handleSendMessage} 
                  disabled={!newMessage.trim() || loading}
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center bg-gray-50">
            <div className="text-center">
              <MessageCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-gray-600 mb-2">
                Selecione um contato
              </h2>
              <p className="text-gray-500">
                Escolha um contato da lista para iniciar a conversa
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

