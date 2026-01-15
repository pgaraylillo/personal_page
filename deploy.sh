#!/bin/bash

# ===================================
# Personal Landing Page Deployment Script
# For Hostinger VPS (Ubuntu)
# ===================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# ===================================
# Check Prerequisites
# ===================================
print_info "Checking prerequisites..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed!"
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    print_success "Docker installed successfully"
else
    print_success "Docker is installed"
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed!"
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed successfully"
else
    print_success "Docker Compose is installed"
fi

# ===================================
# Environment Configuration
# ===================================
print_info "Checking environment configuration..."

if [ ! -f .env ]; then
    print_error ".env file not found!"
    echo "Creating .env from .env.example..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        print_info "Please edit .env file with your configuration:"
        echo "  - Set AI_PROVIDER (openai or anthropic)"
        echo "  - Add your API keys"
        echo "  - Configure your domain"
        read -p "Press Enter after editing .env file..."
    else
        print_error ".env.example not found!"
        exit 1
    fi
fi

# Validate required environment variables
source .env

if [ -z "$AI_PROVIDER" ]; then
    print_error "AI_PROVIDER not set in .env"
    exit 1
fi

if [ "$AI_PROVIDER" = "openai" ] && [ -z "$OPENAI_API_KEY" ]; then
    print_error "OPENAI_API_KEY not set in .env"
    exit 1
fi

if [ "$AI_PROVIDER" = "anthropic" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    print_error "ANTHROPIC_API_KEY not set in .env"
    exit 1
fi

print_success "Environment configuration validated"

# ===================================
# Build and Deploy
# ===================================
print_info "Building and deploying application..."

# Stop existing containers
if [ "$(docker ps -q -f name=portfolio)" ]; then
    print_info "Stopping existing containers..."
    docker-compose down
fi

# Build and start containers
print_info "Building Docker images..."
docker-compose build --no-cache

print_info "Starting containers..."
docker-compose up -d

# Wait for services to be healthy
print_info "Waiting for services to be healthy..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    print_success "Application deployed successfully!"
    echo ""
    echo "Services running:"
    docker-compose ps
    echo ""
    print_success "Application is accessible at: http://localhost"
else
    print_error "Deployment failed! Check logs with: docker-compose logs"
    exit 1
fi

# ===================================
# SSL Certificate Setup (Optional)
# ===================================
echo ""
print_info "SSL Certificate Setup"
echo "To enable HTTPS with Let's Encrypt, follow these steps:"
echo ""
echo "1. Install Certbot:"
echo "   sudo apt-get update"
echo "   sudo apt-get install certbot python3-certbot-nginx"
echo ""
echo "2. Stop Nginx container temporarily:"
echo "   docker-compose stop nginx"
echo ""
echo "3. Obtain SSL certificate:"
echo "   sudo certbot certonly --standalone -d $DOMAIN"
echo ""
echo "4. Create SSL directory and copy certificates:"
echo "   mkdir -p ssl"
echo "   sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ssl/"
echo "   sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ssl/"
echo "   sudo chown -R \$USER:$USER ssl/"
echo ""
echo "5. Update nginx.conf to include SSL configuration"
echo ""
echo "6. Restart containers:"
echo "   docker-compose up -d"
echo ""
echo "7. Set up auto-renewal:"
echo "   sudo certbot renew --dry-run"
echo ""

# ===================================
# Useful Commands
# ===================================
echo ""
print_info "Useful Commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Restart:          docker-compose restart"
echo "  Stop:             docker-compose down"
echo "  Update:           git pull && docker-compose up -d --build"
echo ""

print_success "Deployment complete! 🚀"
