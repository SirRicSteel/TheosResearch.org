# How to Get a GitHub Personal Access Token

This guide explains how to create a GitHub Personal Access Token (PAT) for accessing and contributing to the THEOS Research repository.

## What is a Personal Access Token?

A Personal Access Token (PAT) is a secure way to authenticate with GitHub instead of using your password. It's required for:
- Cloning private repositories
- Pushing changes to repositories
- Using GitHub API
- Authenticating with Git from command line tools

## Getting a Token from Desktop

### Step 1: Sign in to GitHub
1. Go to [github.com](https://github.com)
2. Sign in with your username and password

### Step 2: Navigate to Settings
1. Click your profile picture in the top-right corner
2. Select **Settings** from the dropdown menu

### Step 3: Access Developer Settings
1. Scroll down in the left sidebar
2. Click **Developer settings** (at the bottom)

### Step 4: Generate New Token
1. Click **Personal access tokens** in the left sidebar
2. Choose **Tokens (classic)** or **Fine-grained tokens** (recommended)
   - **Fine-grained tokens** offer more granular control
   - **Classic tokens** are simpler but have broader permissions
3. Click **Generate new token** (or **Generate new token (classic)**)

### Step 5: Configure Token Settings
1. **Note**: Give your token a descriptive name (e.g., "THEOS Research Access")
2. **Expiration**: Select when the token should expire (30/60/90 days, or custom)
3. **Select scopes**: Choose the permissions you need:
   - For basic repository access: check **repo** (full control of private repositories)
   - For public repositories only: check **public_repo**
   - For reading discussions: check **read:discussion**

### Step 6: Generate and Save
1. Click **Generate token** at the bottom
2. **IMPORTANT**: Copy the token immediately! You won't be able to see it again
3. Store it securely (password manager recommended)

## Getting a Token from Mobile

### Using Mobile Web Browser

#### Step 1: Access GitHub Mobile Site
1. Open your mobile browser (Safari, Chrome, etc.)
2. Go to [github.com](https://github.com)
3. Sign in if not already logged in

#### Step 2: Request Desktop Site (Important!)
- **On iPhone/iPad (Safari)**:
  1. Tap the **aA** icon in the address bar
  2. Tap **Request Desktop Website**
  
- **On Android (Chrome)**:
  1. Tap the three dots menu (⋮) in the top-right
  2. Check **Desktop site**

#### Step 3: Navigate to Settings
1. Tap your profile picture in the top-right corner
2. Tap **Settings**

#### Step 4: Access Developer Settings
1. Scroll down to the bottom of the settings page
2. Tap **Developer settings**

#### Step 5: Generate Token
1. Tap **Personal access tokens**
2. Tap **Tokens (classic)** or **Fine-grained tokens**
3. Tap **Generate new token**
4. You may need to enter your password again

#### Step 6: Configure and Save
1. Enter a descriptive note (e.g., "Mobile Access Token")
2. Select expiration period
3. Select scopes/permissions needed:
   - **repo**: Full control of repositories
   - **public_repo**: Access to public repositories only
4. Scroll down and tap **Generate token**
5. **IMMEDIATELY COPY** the token - long-press to select all, then copy
6. Paste it somewhere safe (Notes app, password manager)

### Using GitHub Mobile App

**Note**: The official GitHub mobile app does not currently support creating Personal Access Tokens. You must use the mobile web browser with desktop site mode as described above.

## Common Scopes and Their Uses

| Scope | Description | Use Case |
|-------|-------------|----------|
| `repo` | Full control of private repositories | Pushing, pulling, and managing private repos |
| `public_repo` | Access to public repositories | Contributing to public repos |
| `read:org` | Read-only access to organization membership | Viewing organization details |
| `workflow` | Update GitHub Action workflows | Managing CI/CD pipelines |
| `write:discussion` | Write access to discussions | Participating in repository discussions |

## Using Your Token

### With Git Command Line
When Git asks for your password, use your token instead:

```bash
Username: your-github-username
Password: ghp_your_token_here
```

### Cloning with Token
```bash
git clone https://YOUR_TOKEN@github.com/SirRicSteel/TheosResearch.org.git
```

### With GitHub CLI
```bash
echo YOUR_TOKEN | gh auth login --with-token
```

## Security Best Practices

1. **Never share your token**: Treat it like a password
2. **Use minimal permissions**: Only select scopes you actually need
3. **Set expiration dates**: Don't create tokens that never expire
4. **Rotate regularly**: Generate new tokens periodically
5. **Delete unused tokens**: Remove old tokens you're no longer using
6. **Use fine-grained tokens**: When possible, use the newer fine-grained tokens for better security
7. **Don't commit tokens**: Never include tokens in code or commits

## Troubleshooting

### "Token not found" or "Bad credentials"
- Make sure you copied the entire token
- Verify you're using the token as your password, not your GitHub password
- Check if the token has expired

### Can't see Developer Settings
- Make sure you're signed in
- Request desktop site on mobile (critical step!)
- Ensure you have appropriate account permissions

### Token permissions insufficient
- Go back to your token settings
- Edit the token to add more scopes
- Or generate a new token with the necessary permissions

## Revoking a Token

If your token is compromised or you no longer need it:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Find the token in the list
3. Click **Delete** or **Revoke**
4. Confirm the deletion

## Need Help?

If you're still having trouble getting a token, please:
1. Check GitHub's official documentation: [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
2. Contact the repository maintainer at: frederick.stalnecker@theosresearch.org
3. Open an issue in this repository describing your problem

---

**Last Updated**: December 2025  
**Repository**: [THEOS Research Organization](https://github.com/SirRicSteel/TheosResearch.org)
