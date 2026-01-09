# BotConnections | Marketing Automation Command Center

This dashboard is designed for the **Marketing Team** to manage automated social media postings and device connections across multiple channels.

## 🚀 Key Features
- **WhatsApp Multi-Device Sync**: Connect multiple devices using QR code scanning (Baileys/WA-Automate).
- **Instagram Automation**: Schedule postings, stories, and carousel updates.
- **Telegram Broadcasting**: Manage bot tokens and push mass updates to channels.
- **Twitter (X) Threading**: Automated news sharing via Twitter API v2.
- **n8n Connectivity**: Integrated low-code automation for cross-platform workflows.

## 🛠️ Open-Source Integration
To fully functionalize this UI, we recommend the following open-source engines:

### 1. WhatsApp (Linked Devices)
Use **[Baileys](https://github.com/adiwajshing/Baileys)** or **[whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js)**.
- **Functionality**: Local node.js server starts a session, exports a QR for the UI, and handles webhooks for incoming/outgoing messages.
- **n8n Node**: [n8n-nodes-whatsapp-web](https://github.com/idvorkin/n8n-nodes-whatsapp-web)

### 2. Instagram & Twitter
Integrated via **[n8n](https://n8n.io)** official nodes for:
- Instagram Graph API (Business accounts).
- Twitter V2 API.

### 3. Telegram
Use the standard **[grammY](https://grammy.dev/)** framework or **[telegraf](https://github.com/telegraf/telegraf)**.
- Easily connect via BotFather API Token in the dashboard settings.

## ⚙️ n8n Workflow Resources
We've included conceptual resources for n8n:
1. **Trigger**: Google Sheets (Marketing Content List).
2. **Logic**: AI Content Generator (OpenAI/Gemini).
3. **Action**: Batch post to WhatsApp, Instagram, and Telegram simultaneously.

### How to Deploy n8n:
```bash
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```
Once n8n is running, import the workflows from the `/automation/workflows` directory (Coming Soon).

## 🎨 UI/UX Specifications
- **Theme**: Hitech Dark Glismorphism.
- **Typography**: Outfit & Space Grotesk.
- **Icons**: FontAwesome 6 Pro.
- **Animations**: CSS transitions + Blur Backdrop Filters.

---
*Maintained by Engineering & Teleportz Marketing Team*
