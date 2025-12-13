# GitHub Token Setup Guide

This document provides instructions for creating and managing GitHub tokens for the TheosResearch.org repository.

## What is a GitHub Token?

A GitHub Personal Access Token (PAT) is a secure alternative to using your password when authenticating to GitHub via the command line, API, or third-party applications. Tokens can be scoped to specific permissions and can be revoked at any time.

## Types of GitHub Tokens

### 1. GITHUB_TOKEN (Automatic)
- **Used by:** GitHub Actions workflows
- **Scope:** Automatically generated for each workflow run
- **Permissions:** Defined in the workflow file (see `.github/workflows/static.yml`)
- **No setup required:** This token is automatically available in workflows

### 2. Personal Access Token (PAT)
- **Used by:** Manual repository operations, API access, third-party tools
- **Scope:** User-defined permissions
- **Lifetime:** Can be set to expire or no expiration
- **Requires manual creation:** Follow the steps below

## Creating a New Personal Access Token

### Step 1: Access GitHub Settings
1. Log in to [GitHub.com](https://github.com)
2. Click your profile picture in the top-right corner
3. Select **Settings** from the dropdown menu
4. Scroll down the left sidebar and click **Developer settings**
5. Click **Personal access tokens** → **Tokens (classic)** or **Fine-grained tokens**

### Step 2: Generate New Token

#### For Classic Token:
1. Click **Generate new token** → **Generate new token (classic)**
2. Give your token a descriptive name (e.g., "TheosResearch.org Management")
3. Set an expiration date (recommended: 90 days for security)
4. Select the following scopes based on your needs:

   **For repository management:**
   - ✅ `repo` (Full control of private repositories)
     - Includes: repo:status, repo_deployment, public_repo, repo:invite, security_events

   **For GitHub Pages:**
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `write:packages` (Upload packages to GitHub Package Registry)

   **For repository administration:**
   - ✅ `admin:repo_hook` (Full control of repository hooks)
   - ✅ `delete_repo` (Delete repositories - use with caution)

5. Click **Generate token** at the bottom
6. **IMPORTANT:** Copy the token immediately - you won't be able to see it again!

#### For Fine-grained Token (Recommended for better security):
1. Click **Generate new token** → **Generate new token (fine-grained)**
2. Give your token a descriptive name
3. Set expiration (recommended: 90 days)
4. Under **Repository access**, select:
   - **Only select repositories** → Choose `TheosResearch.org`
5. Under **Permissions**, select:
   - **Repository permissions:**
     - Contents: Read and write
     - Pages: Read and write
     - Workflows: Read and write
     - Metadata: Read-only (automatically set)
6. Click **Generate token**
7. **IMPORTANT:** Copy the token immediately!

### Step 3: Store Your Token Securely

⚠️ **SECURITY WARNING:** Never commit your token to a repository or share it publicly!

**Recommended storage methods:**
1. **Password Manager:** Store in 1Password, LastPass, or similar
2. **Environment Variable:** Add to your `.bashrc` or `.zshrc`:
   ```bash
   export GITHUB_TOKEN="your_token_here"
   ```
3. **Git Credential Manager:** Let Git store it securely for you

## Using Your Token

### Command Line (Git)
When prompted for a password, use your token instead:

```bash
Username: your-github-username
Password: your-personal-access-token
```

Or use it directly in the URL (not recommended for security):
```bash
git clone https://your-personal-access-token@github.com/SirRicSteel/TheosResearch.org.git
```

### GitHub API
Include in the Authorization header:

```bash
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

## Current Repository Token Usage

### GitHub Actions Workflow
The repository uses an automatic `GITHUB_TOKEN` in `.github/workflows/static.yml` with these permissions:

```yaml
permissions:
  contents: read      # Read repository contents
  pages: write        # Deploy to GitHub Pages
  id-token: write     # Generate ID tokens
```

This token is automatically managed by GitHub and requires no manual setup.

## Revoking a Token

If a token is compromised or no longer needed:

1. Go to **Settings** → **Developer settings** → **Personal access tokens**
2. Find the token in the list
3. Click **Delete** or **Revoke**
4. Confirm the action

The token will be immediately invalidated.

## Troubleshooting

### "Authentication failed" errors
- Verify your token hasn't expired
- Check that the token has the required scopes
- Ensure you're using the token (not your password)

### "Resource not accessible by integration" in Actions
- Check the workflow permissions in `.github/workflows/static.yml`
- Verify repository settings allow Actions to access resources

### Token not working after creation
- Make sure you copied the entire token
- Check for extra spaces or characters
- Verify the token hasn't been revoked

## Best Practices

1. ✅ Use fine-grained tokens with minimal required permissions
2. ✅ Set expiration dates on all tokens
3. ✅ Use descriptive names to track token purposes
4. ✅ Rotate tokens regularly (every 90 days recommended)
5. ✅ Revoke unused tokens immediately
6. ❌ Never commit tokens to repositories
7. ❌ Never share tokens in emails, chat, or documentation
8. ❌ Avoid tokens with no expiration date

## Additional Resources

- [GitHub Documentation: Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub Documentation: About authentication to GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
- [GitHub Actions: Automatic token authentication](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)

---

**Last Updated:** December 13, 2025
