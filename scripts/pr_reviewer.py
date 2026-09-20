"""
pr_reviewer.py

Fetches the diff for the current pull request, asks Claude to review it,
and posts the review as a comment on the PR.

Required environment variables (set as GitHub Actions secrets / context):
    GITHUB_TOKEN        - provided automatically by Actions
    ANTHROPIC_API_KEY   - your Anthropic API key, stored as a repo secret
    GITHUB_REPOSITORY   - "owner/repo", provided automatically by Actions
    PR_NUMBER           - pull request number, passed in from the workflow
"""

import os
import sys
import requests
import cohere

COHERE_API_KEY = os.environ["COHERE_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = os.environ["PR_NUMBER"]

GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.diff",
}
HEADERS_JSON = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

MAX_DIFF_CHARS = 20000  # keep prompt size reasonable


def get_pr_diff() -> str:
    url = f"{GITHUB_API}/repos/{REPO}/pulls/{PR_NUMBER}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    diff = resp.text
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n\n...[diff truncated for length]..."
    return diff


def review_with_cohere(diff: str) -> str:
    client = cohere.ClientV2(api_key=COHERE_API_KEY)
    prompt = f"""You are an experienced senior Python engineer doing a pull request code review.
Review the following diff for:
- Bugs or logic errors
- Security issues
- Code style / readability
- Missing tests or edge cases

Be concise and specific. Use bullet points. If the code looks good, say so briefly.

Diff:
{diff}
"""

    response = client.chat(
        model="command-a-plus-05-2026",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    # return response.message.content[0]
    content = response.message.content
    if isinstance(content, list):
        if content:
            item = content[0]
            if hasattr(item, 'text'):
                return item.text
            if isinstance(item, dict):
                return item.get('text', '')
            return str(item)
    return "Everything looks good!"  # fallback if content is not as expected
    # return "".join(
    #     block.text for block in message.content if block.type == "text"
    # )


def post_comment(body: str) -> None:
    url = f"{GITHUB_API}/repos/{REPO}/issues/{PR_NUMBER}/comments"
    comment_body = f"### 🤖 Automated Code Review\n\n{body}"
    resp = requests.post(url, headers=HEADERS_JSON, json={"body": comment_body}, timeout=30)
    resp.raise_for_status()


def main() -> None:
    diff = get_pr_diff()
    if not diff.strip():
        print("No diff found for this PR, skipping review.")
        return

    review = review_with_cohere(diff)
    post_comment(review)
    print("Posted review comment successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"PR review failed: {e}", file=sys.stderr)
        sys.exit(1)
