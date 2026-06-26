# Security Policy

This repository is a public research archive. Do not commit service credentials,
tokens, private database URLs, `.env` files, private exports, or personally
sensitive raw data.

## Runtime Credentials

Notebooks and scripts that require external services must read credentials from
environment variables or Colab secrets:

- `NEO4J_URI`
- `NEO4J_USER`
- `NEO4J_PASSWORD`
- `EAI_USERNAME`
- `EAI_PASSWORD`

Use `.env.example` as a local template only. Real `.env` files are ignored by
git and must remain local.

## Historical Exposure

If any historical public commit exposed live credentials, rotate those
credentials before using the repository as a public academic artifact. Current
notebooks should not contain literal service passwords.

## Local Audit

Run:

```bash
python scripts/validate_repository.py
```

The audit checks notebook JSON validity and rejects common secret patterns in
tracked research files.
