#!/bin/bash

# Takes two arguments: GitHub user name and CRSid
if [ $# -ne 2 ]; then
    echo "Usage: $0 <user-name> <crsid>"
    echo "Example: $0 johnsmith abc123"
    exit 1
fi

USER_NAME=$1
CRSID=$2
REPO_URL="https://github.com/${USER_NAME}/packaging-publishing-${CRSID}"

echo "Setting up remote for: $REPO_URL"

# We set the remote URL to be you newly forked repo (this will update if it already exists)
git remote set-url origin "$REPO_URL" 2>/dev/null || git remote add origin "$REPO_URL"
if [ $? -ne 0 ]; then
    echo "Error: Failed to set remote URL"
    exit 1
fi

# Now rename the current branch, called basic, to main
git branch -M main
if [ $? -ne 0 ]; then
    echo "Error: Failed to rename branch to main"
    exit 1
fi

# Force push to the forked repo, overwriting any existing content
echo "Pushing to $REPO_URL..."
git push -f -u origin main
if [ $? -ne 0 ]; then
    echo "Error: Failed to push to remote repository"
    echo "Make sure the repository exists and you have access to it"
    exit 1
fi

echo "Done! Successfully pushed to $REPO_URL."
echo "Deleting update-fork.sh script."
rm -- "$0"
echo "Script deleted. Have a nice day."