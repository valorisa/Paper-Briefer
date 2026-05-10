# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability in paper-briefer, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainer or use GitHub's private vulnerability reporting feature
3. Include steps to reproduce the issue

Since this tool processes ZIP files, potential attack vectors include:
- Zip bombs (mitigated by file count/size limits)
- Path traversal in ZIP entries (mitigated by sanitizing extracted paths)
- Malformed markdown triggering regex catastrophic backtracking

We aim to acknowledge reports within 48 hours and provide a fix within 7 days for confirmed vulnerabilities.
