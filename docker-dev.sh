#!/bin/bash

# Docker Development Helper Script for Azeroth Herald

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}Azeroth Herald - Docker Development Helper${NC}"
    echo -e "${GREEN}[INFO]${NC} $1"
    echo "=============================================="
}

# Function to check if .env exists
print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        echo -e "${RED}Error: .env file not found!${NC}"
        echo "Please create a .env file with your Discord bot token and channel ID."
        echo "Example:"
        echo "DISCORD_TOKEN=your_bot_token_here"
        echo "TARGET_CHANNEL_ID=your_channel_id_here"
        echo "RAIDER_IO_API_KEY=your_api_key_here (optional)"
        exit 1
    fi
    echo -e "${GREEN}✓ .env file found${NC}"
}

case "$1" in
    "dev")
        print_status "Starting development environment with hot reload..."
        docker compose -f docker-compose.yml up --build bot-dev
        ;;
    "prod")
        print_status "Starting production environment..."
        docker compose -f docker-compose.yml up --build bot-prod
        ;;
    "build")
        print_status "Building Docker images..."
        docker compose -f docker-compose.yml build
        ;;
    "stop")
        print_status "Stopping all containers..."
        docker compose -f docker-compose.yml down
        docker compose down
        ;;
    "logs")
        service=${2:-bot-dev}
        print_status "Showing logs for $service..."
        docker compose -f docker-compose.yml logs -f $service
        ;;
    "shell")
        service=${2:-bot-dev}
        print_status "Opening shell in $service..."
        docker compose -f docker-compose.yml exec $service /bin/bash
        ;;
    "clean")
        print_status "Cleaning up Docker resources..."
        docker compose -f docker-compose.yml down -v
        docker compose down -v
        docker system prune -f
        ;;
    *)
        echo "Usage: $0 {dev|prod|build|stop|logs|shell|clean}"
        echo ""
        echo "Commands:"
        echo "  dev     - Start development environment with hot reload"
        echo "  prod    - Start production-like environment"
        echo "  build   - Build Docker images"
        echo "  stop    - Stop all containers"
        echo "  logs    - Show container logs (optionally specify service name)"
        echo "  shell   - Open shell in container (optionally specify service name)"
        echo "  clean   - Stop containers and clean up Docker resources"
        echo ""
        echo "Examples:"
        echo "  $0 dev"
        echo "  $0 logs bot-dev"
        echo "  $0 shell bot-prod"
        exit 1
        ;;
esac

        echo -e "${RED}Error: .env file not found!${NC}"

        echo "Please create a .env file with your Discord bot token and channel ID."print_error() {

        echo "Example:"    echo -e "${RED}[ERROR]${NC} $1"

        echo "DISCORD_TOKEN=your_bot_token_here"}

        echo "TARGET_CHANNEL_ID=your_channel_id_here"

        echo "RAIDER_IO_API_KEY=your_api_key_here (optional)"# Check if .env file exists

        exit 1if [ ! -f .env ]; then

    fi    print_warning ".env file not found. Creating from .env.example..."

    echo -e "${GREEN}✓ .env file found${NC}"    cp .env.example .env

}    print_warning "Please edit .env file with your actual values before running the bot!"

fi

# Function to build images

build_images() {case "$1" in

    echo -e "${YELLOW}Building Docker images...${NC}"    "dev")

    docker compose build        print_status "Starting development environment with hot reload..."

    echo -e "${GREEN}✓ Images built successfully${NC}"        docker compose -f docker-compose.yml up --build bot-dev

}        ;;

    "prod")

# Main menu        print_status "Starting production environment..."

show_menu() {        docker compose -f docker-compose.yml up --build azeroth-herald-prod

    echo ""        ;;

    echo "Available commands:"    "build")

    echo "1. dev     - Run development server with hot reload"        print_status "Building Docker images..."

    echo "2. prod    - Run production-like server"        docker compose -f docker-compose.yml build

    echo "3. simple  - Run simple development server (no file watching)"        ;;

    echo "4. build   - Build Docker images"    "stop")

    echo "5. logs    - Show bot logs"        print_status "Stopping all containers..."

    echo "6. stop    - Stop all containers"        docker compose -f docker-compose.yml down

    echo "7. clean   - Stop and remove all containers"        docker compose down

    echo "8. shell   - Open shell in development container"        ;;

    echo ""    "logs")

}        service=${2:-bot-dev}

        print_status "Showing logs for $service..."

case "$1" in        docker compose -f docker-compose.yml logs -f $service

    "dev")        ;;

        check_env    "shell")

        echo -e "${YELLOW}Starting development server with hot reload...${NC}"        service=${2:-bot-dev}

        docker compose --profile dev up --build        print_status "Opening shell in $service..."

        ;;        docker compose -f docker-compose.yml exec $service /bin/bash

    "prod")        ;;

        check_env    "clean")

        echo -e "${YELLOW}Starting production-like server...${NC}"        print_status "Cleaning up Docker resources..."

        docker compose --profile prod up --build        docker compose -f docker-compose.yml down -v

        ;;        docker compose down -v

    "simple")        docker system prune -f

        check_env        ;;

        echo -e "${YELLOW}Starting simple development server...${NC}"    *)

        docker compose --profile simple up --build        echo "Usage: $0 {dev|prod|build|stop|logs|shell|clean}"

        ;;        echo ""

    "build")        echo "Commands:"

        check_env        echo "  dev     - Start development environment with hot reload"

        build_images        echo "  prod    - Start production-like environment"

        ;;        echo "  build   - Build Docker images"

    "logs")        echo "  stop    - Stop all containers"

        echo -e "${YELLOW}Showing bot logs (Ctrl+C to exit)...${NC}"        echo "  logs    - Show container logs (optionally specify service name)"

        docker compose logs -f        echo "  shell   - Open shell in container (optionally specify service name)"

        ;;        echo "  clean   - Stop containers and clean up Docker resources"

    "stop")        echo ""

        echo -e "${YELLOW}Stopping all containers...${NC}"        echo "Examples:"

        docker compose down        echo "  $0 dev"

        echo -e "${GREEN}✓ All containers stopped${NC}"        echo "  $0 logs bot-dev"

        ;;        echo "  $0 shell bot-prod"

    "clean")        exit 1

        echo -e "${YELLOW}Stopping and removing all containers...${NC}"        ;;

        docker compose down --remove-orphansesac
        echo -e "${GREEN}✓ All containers stopped and removed${NC}"
        ;;
    "shell")
        echo -e "${YELLOW}Opening shell in development container...${NC}"
        docker compose --profile dev run --rm bot-dev bash
        ;;
    *)
        show_menu
        echo "Usage: $0 {dev|prod|simple|build|logs|stop|clean|shell}"
        echo ""
        echo "Examples:"
        echo "  $0 dev     # Start development server with hot reload"
        echo "  $0 prod    # Start production-like server"
        echo "  $0 logs    # View bot logs"
        echo "  $0 stop    # Stop all containers"
        ;;
esac