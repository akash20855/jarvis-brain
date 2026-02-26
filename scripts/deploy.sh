#!/bin/bash

# ════════════════════════════════════════════════════════════════════════
# JARVIS BRAIN - Cloud Deployment Script
# ════════════════════════════════════════════════════════════════════════

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/." && pwd)"
cd "$PROJECT_ROOT/.."

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     JARVIS BRAIN - CLOUD DEPLOYMENT                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check for AWS CLI
if ! command -v aws &> /dev/null; then
    log_error "AWS CLI not installed. Install from https://aws.amazon.com/cli/"
    exit 1
fi
log_success "AWS CLI found"
echo ""

# Get S3 bucket
if [ -z "$AWS_BUCKET" ]; then
    read -p "Enter AWS S3 bucket name: " AWS_BUCKET
fi

if [ -z "$AWS_BUCKET" ]; then
    log_error "Bucket name required"
    exit 1
fi

log_info "Using S3 bucket: s3://$AWS_BUCKET"
echo ""

# Build distribution
log_info "Building distribution..."
if [ -d "jarvis_env" ]; then
    source jarvis_env/bin/activate
    python3 setup.py sdist bdist_wheel > /dev/null 2>&1
else
    python3 setup.py sdist bdist_wheel > /dev/null 2>&1
fi
log_success "Distribution built"
echo ""

# Upload to S3
log_info "Uploading to S3: s3://$AWS_BUCKET/jarvis-brain/"
aws s3 sync dist/ "s3://$AWS_BUCKET/jarvis-brain/" --region us-east-1
log_success "Upload complete"
echo ""

# Upload source code
log_info "Uploading source code..."
tar -czf jarvis-brain-source.tar.gz core/ agents/ modules/ tests/ examples/ --exclude='__pycache__' --exclude='*.pyc'
aws s3 cp jarvis-brain-source.tar.gz "s3://$AWS_BUCKET/jarvis-brain/source/"
rm jarvis-brain-source.tar.gz
log_success "Source code uploaded"
echo ""

log_success "Cloud deployment complete!"
echo -e "${YELLOW}Access your files at: https://$AWS_BUCKET.s3.amazonaws.com/jarvis-brain/${NC}"
echo ""
