# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in VOLVO MDC, please report it responsibly:

### Internal Reporting (VOLVO Employees)
- Contact: Nawoar Ekkou
- Department: Manufacturing Technology Division
- Location: VOLVO Cars Torslanda

### External Reporting
- **DO NOT** create public GitHub issues for security vulnerabilities
- Email security reports to the development team
- Include detailed steps to reproduce the issue
- Provide information about potential impact

## Security Considerations

### Authentication
- Default credentials should be changed in production
- Implement strong password policies
- Consider multi-factor authentication for sensitive environments

### File Uploads
- Application validates file types and sizes
- Uploaded files are processed in a sandboxed environment
- Consider implementing virus scanning for production use

### Data Protection
- All operations are logged for audit purposes
- Generated codes may contain sensitive manufacturing information
- Ensure proper access controls are in place

### Network Security
- Use HTTPS in production environments
- Implement proper firewall rules
- Consider VPN access for remote usage

## Best Practices

1. **Regular Updates**: Keep dependencies updated
2. **Access Control**: Limit access to authorized personnel only
3. **Monitoring**: Implement logging and monitoring
4. **Backup**: Regular backup of database.json
5. **Environment**: Separate development and production environments

---

© 2025 VOLVO Cars. All rights reserved.  
Made by: Nawoar Ekkou
