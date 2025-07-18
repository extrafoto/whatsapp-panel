const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Erro na requisição');
      }
      
      return data;
    } catch (error) {
      console.error('Erro na API:', error);
      throw error;
    }
  }

  // Contatos
  async getContacts() {
    return this.request('/contacts');
  }

  async getContact(contactId) {
    return this.request(`/contacts/${contactId}`);
  }

  async createContact(contactData) {
    return this.request('/contacts', {
      method: 'POST',
      body: JSON.stringify(contactData),
    });
  }

  async updateContactStatus(contactId, status) {
    return this.request(`/contacts/${contactId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  async getContactMessages(contactId) {
    return this.request(`/contacts/${contactId}/messages`);
  }

  // Mensagens
  async sendMessage(contactId, text) {
    return this.request('/messages', {
      method: 'POST',
      body: JSON.stringify({ contact_id: contactId, text }),
    });
  }

  async receiveMessage(phoneNumber, text, name = '') {
    return this.request('/messages/receive', {
      method: 'POST',
      body: JSON.stringify({ phone_number: phoneNumber, text, name }),
    });
  }

  // Google Sheets
  async syncWithSheets() {
    return this.request('/sheets/sync', {
      method: 'POST',
    });
  }

  async updateStatusInSheets(phoneNumber, status) {
    return this.request('/sheets/update-status', {
      method: 'POST',
      body: JSON.stringify({ phone_number: phoneNumber, status }),
    });
  }
}

export default new ApiService();

