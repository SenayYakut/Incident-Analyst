# Contributing to Autonomous Incident Analyst

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Git
- Docker (optional, for containerized development)

### Development Setup

1. **Fork and Clone**
   ```bash
   git fork <repository-url>
   git clone <your-fork-url>
   cd autonomous-incident-analyst
   ```

2. **Install Dependencies**
   ```bash
   # Backend
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

3. **Set Up Environment**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Add your YOU_API_KEY if available
   
   # Frontend
   cp frontend/.env.example frontend/.env.local
   ```

4. **Run Tests**
   ```bash
   # Start backend in one terminal
   cd backend && uvicorn main:app --reload
   
   # Run API tests in another terminal
   ./test-api.sh
   ```

## Development Workflow

### Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make Your Changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test Your Changes**
   ```bash
   # Backend tests
   cd backend
   python -m pytest  # If tests exist
   
   # API tests
   ./test-api.sh
   
   # Frontend build
   cd frontend
   npm run build
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature" 
   # or
   git commit -m "fix: resolve bug in incident analysis"
   ```

### Commit Message Convention

We follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add confidence score to incident analysis
fix: resolve CORS issue in production
docs: update API endpoint documentation
refactor: simplify memory retrieval logic
```

## Code Guidelines

### Backend (Python)

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and single-purpose

Example:
```python
async def analyze_incident(
    logs: str,
    metrics: str = "",
    similar_incidents: List[dict] = None
) -> dict:
    """
    Analyze an incident using LLM.
    
    Args:
        logs: System logs to analyze
        metrics: Optional metrics data
        similar_incidents: Past similar incidents for context
        
    Returns:
        dict: Analysis with root causes and suggested fixes
    """
    # Implementation
```

### Frontend (TypeScript/React)

- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable

Example:
```typescript
interface AnalysisProps {
  analysis: Analysis | null;
  loading: boolean;
}

export function AnalysisCard({ analysis, loading }: AnalysisProps) {
  // Implementation
}
```

## Testing

### Backend Testing

- Test all API endpoints
- Verify error handling
- Test with and without LLM API key
- Check incident memory operations

### Frontend Testing

- Test UI interactions
- Verify API integration
- Check responsive design
- Test error states

### Integration Testing

Run the full test suite:
```bash
./test-api.sh
```

## Documentation

### When to Update Documentation

- Adding new features
- Changing API endpoints
- Modifying configuration options
- Updating deployment process

### Documentation Files

- `README.md` - Main project documentation
- `CONTRIBUTING.md` - This file
- API docstrings - In-code documentation
- `render.yaml` - Deployment configuration

## Pull Request Process

1. **Update Documentation**
   - Update README if needed
   - Add/update API documentation
   - Update CHANGELOG if applicable

2. **Ensure Tests Pass**
   - Run all tests locally
   - Fix any failing tests
   - Add new tests for new features

3. **Submit Pull Request**
   - Provide clear description
   - Reference any related issues
   - Include screenshots for UI changes
   - Wait for review

4. **Address Review Comments**
   - Respond to feedback
   - Make requested changes
   - Update PR description if scope changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] API tests pass
- [ ] Frontend builds successfully

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #issue_number
```

## Feature Requests

### Suggesting Features

1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Use case/motivation
   - Proposed implementation (optional)
   - Examples (if applicable)

### Feature Priority

High priority:
- Bug fixes
- Performance improvements
- Security issues

Medium priority:
- New analysis patterns
- UI improvements
- Better error handling

Low priority:
- Nice-to-have features
- Cosmetic changes

## Bug Reports

### Reporting Bugs

Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, versions, etc.)
- Relevant logs or error messages

Example:
```markdown
## Bug Description
Frontend cannot connect to backend

## Steps to Reproduce
1. Start backend on port 8000
2. Start frontend on port 3000
3. Submit incident
4. See error in console

## Expected Behavior
Incident should be submitted successfully

## Actual Behavior
CORS error in browser console

## Environment
- OS: macOS 14.0
- Node: 20.11.0
- Python: 3.11.0
- Browser: Chrome 120.0
```

## Areas for Contribution

### Good First Issues

- Add more error patterns to fallback analysis
- Improve UI error messages
- Add loading states
- Write additional tests

### Medium Complexity

- Implement incident filtering/search
- Add export functionality
- Create incident templates
- Improve similarity matching algorithm

### Advanced

- Add database support (PostgreSQL, MongoDB)
- Implement user authentication
- Add real-time updates (WebSocket)
- Create incident visualization dashboard
- Implement vector embeddings for better similarity search

## Code Review

### As a Reviewer

- Be constructive and respectful
- Explain reasoning for suggestions
- Approve when satisfied
- Test changes locally if possible

### As a Contributor

- Be open to feedback
- Ask questions if unclear
- Don't take criticism personally
- Update PR based on feedback

## Community

### Communication

- GitHub Issues - Bug reports and features
- GitHub Discussions - Questions and ideas
- Pull Requests - Code contributions

### Code of Conduct

- Be respectful and inclusive
- Help newcomers
- Give constructive feedback
- Focus on the code, not the person

## Questions?

If you have questions:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with the "question" label
4. Join discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you for contributing to Autonomous Incident Analyst! Every contribution, no matter how small, helps make this project better.
