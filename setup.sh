#!/bin/bash

# OSINT Weather Aggregator - Setup Script
# Simple Docker deployment setup

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}OSINT Weather Aggregator - Setup${NC}\n"

# Check Docker
echo "Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker compose &> /dev/null && ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is ready${NC}"

# Check .env
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${BLUE}Please configure .env with your API keys and run setup again${NC}"
    exit 0
fi

echo -e "${GREEN}✓ .env file exists${NC}"

# Build and start
echo "Building Docker images..."
docker compose build

echo "Starting services..."
docker compose up -d

echo -e "\n${GREEN}Setup complete!${NC}\n"
echo "Services:"
echo "  FastAPI:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "  n8n:      http://localhost:5678"
echo "  pgAdmin:  http://localhost:5051"
echo ""
echo "Run 'docker compose logs -f' to view logs"
