# Deployment Configuration Files

This directory contains production deployment templates for Eneo.

## 📁 Files

- `docker-compose.yml` - Production Docker Compose configuration with Traefik
- `env_backend.template` - Backend environment template
- `env_frontend.template` - Frontend environment template
- `env_db.template` - Database environment template

## 🚀 Quick Start

1. **Download files** (if not cloning repo):
   ```bash
   mkdir eneo-deployment && cd eneo-deployment
   curl -LO https://raw.githubusercontent.com/sundsvallai/eneo/main/docs/deployment/{docker-compose.yml,env_backend.template,env_frontend.template,env_db.template}
   ```

2. **Create environment files**:
   ```bash
   cp env_backend.template env_backend.env
   cp env_frontend.template env_frontend.env
   cp env_db.template env_db.env
   ```

3. **Configure** (marked with comments in templates):
   - Replace `your-domain.com` in all files
   - Add at least one AI provider API key
   - Generate JWT_SECRET: `openssl rand -hex 32`
   - Set secure database password

4. **Deploy**:
   ```bash
   docker network create proxy_tier
   docker compose up -d
   ```

## ⚠️ Important Notes

- **Security**: Generate unique secrets, never use defaults
- **Domains**: Update all occurrences of `your-domain.com`
- **Ports**: Production uses port 8000 (not 8123 like development)
- **SSL**: Traefik auto-manages certificates via Let's Encrypt

For detailed instructions, see [DEPLOYMENT.md](../DEPLOYMENT.md)