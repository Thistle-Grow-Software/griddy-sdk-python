#!/usr/bin/env bash
set -euo pipefail

COMMENT_MARKER="<!-- docs-preview -->"
BODY="${COMMENT_MARKER}
📄 **Docs preview:** ${DEPLOY_URL}"

REPO="${GITHUB_REPOSITORY}"

# Find an existing preview comment from the bot
EXISTING_COMMENT_ID=$(
    gh api "repos/${REPO}/issues/${PR_NUMBER}/comments" \
        --jq ".[] | select(.body | startswith(\"${COMMENT_MARKER}\")) | .id" \
    | head -n 1
)

if [[ -n "${EXISTING_COMMENT_ID}" ]]; then
    gh api "repos/${REPO}/issues/comments/${EXISTING_COMMENT_ID}" \
        --method PATCH \
        --field body="${BODY}"
    echo "Updated existing comment ${EXISTING_COMMENT_ID}"
else
    gh api "repos/${REPO}/issues/${PR_NUMBER}/comments" \
        --method POST \
        --field body="${BODY}"
    echo "Created new comment"
fi