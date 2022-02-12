#!/bin/bash
export DATABASE_URL="postgresql://postgres:1701@localhost:5432/agency"
export DATABASE_TEST_URL="postgresql://postgres:1701@localhost:5432/agency_test"
export AUTH0_DOMAIN="fsnd3469.us.auth0.com"
export API_AUDIENCE="agency"
export ALGORITHMS="RS256" 
export CLIENT_ID="xF3XrLq6kJVBcZbl46cSdpewX8BsP8q7"
export CLIENT_SECRET="5N4eoisQ08u3ljfPMymhx-_-exv6xPRYVZjkwGH-mBYNXdlLpTzZcKzaJ-JPC6HP"
echo "setup.sh script executed successfully!"