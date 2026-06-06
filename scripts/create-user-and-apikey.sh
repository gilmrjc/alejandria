#!/bin/bash
# Script to create a user account and generate an API KEY for Alejandria

set -e

cd "$(dirname "$0")/.."

# Use provided arguments or defaults
EMAIL="${1:-dev@alejandria.local}"
USERNAME="${2:-devuser}"
PASSWORD="${3:-devpassword123}"
API_KEY_NAME="${4:-Development Key}"

echo "=== Alejandria User and API Key Creation ==="
echo ""
echo "Email: $EMAIL"
echo "Username: $USERNAME"
echo "API Key Name: $API_KEY_NAME"
echo ""

echo "Creating user account using Docker Compose..."

# Create user using Python script inside Docker container
docker compose --profile dev run --rm dev uv run python -c "
import sys
import uuid
from sqlalchemy import select
from shared.auth.jwt import get_password_hash
from shared.db.models import User, Organization, ApiKey
from shared.db.session import get_db_session
from shared.auth.api_key import generate_api_key, hash_api_key

session = get_db_session()

try:
    # Check if email already exists
    existing_email = session.execute(
        select(User).where(User.email == '$EMAIL')
    ).scalar_one_or_none()

    if existing_email:
        print(f'Error: Email $EMAIL already registered')
        sys.exit(1)

    # Check if username already exists
    existing_username = session.execute(
        select(User).where(User.username == '$USERNAME')
    ).scalar_one_or_none()

    if existing_username:
        print(f'Error: Username $USERNAME already taken')
        sys.exit(1)

    # Hash password
    password_hash = get_password_hash('$PASSWORD')

    # Create user
    user = User(
        email='$EMAIL',
        username='$USERNAME',
        password_hash=password_hash,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    print(f'✓ User created: {user.email} (ID: {user.id})')

    # Create personal organization
    org = Organization(
        name=f\"{user.username}'s Personal Space\",
        slug=f\"{user.username}-personal\",
        is_personal=True,
        created_by=user.id,
    )
    session.add(org)
    session.commit()
    session.refresh(org)

    print(f'✓ Personal organization created: {org.name} (ID: {org.id})')

    # Generate API key
    plain_key = generate_api_key()
    key_hash = hash_api_key(plain_key)

    api_key = ApiKey(
        key_hash=key_hash,
        name='$API_KEY_NAME',
        user_id=user.id,
        organization_id=org.id,
        is_active=True,
    )
    session.add(api_key)
    session.commit()
    session.refresh(api_key)

    print(f'✓ API Key created: {api_key.name}')
    print('')
    print('=== YOUR API KEY ===')
    print(plain_key)
    print('=====================')
    print('')
    print('Save this API key securely! You will need it to authenticate with the MCP server.')

finally:
    session.close()
"

echo ""
echo "Account and API key created successfully!"
