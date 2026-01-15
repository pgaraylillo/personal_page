# Personal Landing Page 🚀

A modern, containerized personal landing page featuring FastAPI backend, AI-powered chatbot, and stunning responsive frontend. Built for deployment on Hostinger VPS.

## ✨ Features

- **Modern UI/UX**: Sleek design with dark/light mode support
- **AI Chatbot**: Intelligent assistant powered by OpenAI or Anthropic
- **Blog System**: Markdown-based blog with frontmatter support
- **Portfolio Showcase**: Dynamic project cards with tech stack display
- **Fully Containerized**: Docker & Docker Compose ready
- **Production Ready**: Nginx reverse proxy, health checks, SSL support
- **Responsive Design**: Mobile-first approach with Bootstrap 5

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **OpenAI/Anthropic**: AI chatbot integration
- **Markdown**: Blog post rendering
- **Pydantic**: Data validation

### Frontend
- **HTML5/CSS3/JavaScript**: Modern vanilla web technologies
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icon library
- **Google Fonts**: Inter typography

### Infrastructure
- **Docker**: Containerization
- **Nginx**: Reverse proxy and static file serving
- **Let's Encrypt**: SSL certificates (optional)

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic models
│   ├── requirements.txt     # Python dependencies
│   ├── routers/
│   │   ├── blog.py         # Blog endpoints
│   │   ├── apps.py         # Portfolio endpoints
│   │   └── chat.py         # AI chat endpoint
│   └── services/
│       └── ai_service.py   # AI integration
├── frontend/
│   ├── index.html          # Main HTML
│   ├── css/
│   │   └── styles.css      # Custom styles
│   └── js/
│       └── main.js         # Frontend logic
├── data/
│   ├── context.md          # AI chatbot context
│   ├── apps.json           # Portfolio data
│   └── blog/               # Blog posts (Markdown)
├── Dockerfile              # Backend container
├── docker-compose.yml      # Service orchestration
├── nginx.conf              # Nginx configuration
├── deploy.sh               # Deployment script
└── .env.example            # Environment template
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI or Anthropic API key

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd twilight-aldrin
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Configure your AI provider**
   
   Edit `.env`:
   ```env
   AI_PROVIDER=openai  # or 'anthropic'
   OPENAI_API_KEY=your_key_here
   ```

4. **Customize your content**
   - Edit `data/context.md` with your bio
   - Update `data/apps.json` with your projects
   - Add blog posts to `data/blog/` (Markdown format)

5. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

6. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost/api
   - API Docs: http://localhost:8000/docs

### Development Without Docker

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
Serve the `frontend/` directory with any static file server.

## 📝 Content Management

### Adding Blog Posts

Create a new Markdown file in `data/blog/`:

```markdown
---
title: "Your Post Title"
date: "2026-01-15"
author: "Your Name"
excerpt: "Brief description"
tags: "Python, FastAPI, Docker"
---

# Your Post Title

Your content here...
```

### Updating Portfolio

Edit `data/apps.json`:

```json
{
  "id": "project-id",
  "name": "Project Name",
  "description": "Project description",
  "tech_stack": ["React", "Node.js"],
  "demo_url": "https://demo.com",
  "github_url": "https://github.com/...",
  "featured": true
}
```

### Customizing AI Context

Edit `data/context.md` with your:
- Professional background
- Skills and expertise
- Projects and achievements
- Personal interests

## 🌐 Deployment to Hostinger VPS

### Automated Deployment

1. **Upload files to VPS**
   ```bash
   scp -r . user@your-vps-ip:/path/to/app
   ```

2. **SSH into VPS**
   ```bash
   ssh user@your-vps-ip
   cd /path/to/app
   ```

3. **Run deployment script**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

The script will:
- ✅ Check and install Docker/Docker Compose
- ✅ Validate environment configuration
- ✅ Build and start containers
- ✅ Provide SSL setup instructions

### SSL Certificate Setup

After deployment, enable HTTPS:

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Stop Nginx container
docker-compose stop nginx

# Obtain certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
mkdir -p ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/
sudo chown -R $USER:$USER ssl/

# Update nginx.conf for SSL (add server block for port 443)

# Restart
docker-compose up -d
```

### Manual Nginx SSL Configuration

Add to `nginx.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    # ... rest of your configuration
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AI_PROVIDER` | AI provider (`openai` or `anthropic`) | Yes |
| `OPENAI_API_KEY` | OpenAI API key | If using OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic API key | If using Anthropic |
| `OPENAI_MODEL` | OpenAI model name | No |
| `ANTHROPIC_MODEL` | Anthropic model name | No |
| `ALLOWED_ORIGINS` | CORS allowed origins | No |
| `DOMAIN` | Your domain name | For SSL |

## 📊 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

- `GET /api/blog` - List all blog posts
- `GET /api/blog/{slug}` - Get specific blog post
- `GET /api/apps` - List portfolio applications
- `POST /api/chat` - Send message to AI chatbot
- `GET /health` - Health check

## 🎨 Customization

### Theming

Edit CSS variables in `frontend/css/styles.css`:

```css
:root {
    --accent-primary: #3b82f6;
    --accent-secondary: #8b5cf6;
    /* ... more variables */
}
```

### Fonts

Change Google Fonts in `frontend/index.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;700&display=swap" rel="stylesheet">
```

## 🐛 Troubleshooting

### Container Issues

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild from scratch
docker-compose down
docker-compose up --build
```

### API Connection Issues

1. Check backend is running: `docker-compose ps`
2. Verify environment variables: `cat .env`
3. Check API health: `curl http://localhost:8000/health`

### Frontend Not Loading

1. Check Nginx logs: `docker-compose logs nginx`
2. Verify frontend files are mounted correctly
3. Clear browser cache

## 📦 Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service-name]

# Restart specific service
docker-compose restart [service-name]

# Update and redeploy
git pull
docker-compose up -d --build

# Execute command in container
docker-compose exec backend bash
```

## 🤝 Contributing

Feel free to fork and customize for your own use!

## 📄 License

MIT License - feel free to use this project for your personal portfolio.

## 🙏 Acknowledgments

- Built with ❤️ using FastAPI and Bootstrap
- AI powered by OpenAI/Anthropic
- Icons by Font Awesome
- Fonts by Google Fonts

---

**Built by Pablo Garay** | [GitHub](https://github.com/pablogaray) | [LinkedIn](https://linkedin.com/in/pablogaray)
