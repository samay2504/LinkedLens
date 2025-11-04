# 🤝 Contributing to AI-Powered LinkedIn Post Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)

---

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct inappropriate in a professional setting

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Google Gemini API key (for testing)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/linkedin-post-generator.git
   cd linkedin-post-generator
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/linkedin-post-generator.git
   ```

### Setup Development Environment

Run the setup script:
```bash
# Windows
.\setup.ps1

# macOS/Linux
chmod +x setup.sh
./setup.sh
```

Or follow [QUICKSTART.md](QUICKSTART.md) for manual setup.

---

## 🔄 Development Workflow

### 1. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test improvements
- `chore/` - Maintenance tasks

### 2. Make Changes

- Write clean, maintainable code
- Follow coding standards (see below)
- Add/update tests
- Update documentation

### 3. Test Your Changes

```bash
# Backend tests
cd backend
pytest -v --cov=api

# Frontend build test
cd frontend
npm run build
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add amazing feature"
```

See [Commit Messages](#commit-messages) section for format.

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create Pull Request

- Go to your fork on GitHub
- Click "Compare & pull request"
- Fill out the PR template
- Link related issues

---

## 💻 Coding Standards

### Python (Backend)

#### Style Guide
- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [Flake8](https://flake8.pycqa.org/) for linting
- Maximum line length: 88 characters (Black default)

#### Best Practices

**Type Hints:**
```python
def generate_post(topic: str) -> Dict[str, any]:
    """Generate a LinkedIn post."""
    pass
```

**Docstrings (Google Style):**
```python
def process_data(input_data: str, validate: bool = True) -> Dict:
    """
    Process input data and return results.
    
    Args:
        input_data: The data to process
        validate: Whether to validate input
    
    Returns:
        Dict containing processed results
    
    Raises:
        ValueError: If input data is invalid
    """
    pass
```

**Error Handling:**
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error("operation_failed", error=str(e))
    raise
```

**Logging:**
```python
import structlog

logger = structlog.get_logger()
logger.info("event_name", key1="value1", key2="value2")
```

### JavaScript/Vue (Frontend)

#### Style Guide
- Use ES6+ syntax
- 2 spaces for indentation
- Semicolons at end of statements
- Single quotes for strings

#### Best Practices

**Component Structure:**
```vue
<template>
  <!-- Template -->
</template>

<script setup>
// Imports
import { ref, computed } from 'vue';

// Props
const props = defineProps({
  data: Object
});

// State
const state = ref(null);

// Computed
const computed = computed(() => {
  return state.value;
});

// Methods
const doSomething = () => {
  // Implementation
};
</script>

<style scoped>
/* Styles */
</style>
```

**API Calls:**
```javascript
try {
  const response = await apiClient.post('/endpoint', data);
  return response.data;
} catch (error) {
  console.error('API Error:', error);
  throw error;
}
```

### General Guidelines

- **DRY** (Don't Repeat Yourself)
- **KISS** (Keep It Simple, Stupid)
- **SOLID** principles
- Write self-documenting code
- Comment complex logic
- Use meaningful variable names

---

## 🧪 Testing Guidelines

### Backend Testing

#### Test Structure
```python
import pytest
from httpx import AsyncClient
from api.main import app

@pytest.mark.asyncio
async def test_feature_name():
    """Test that feature works correctly."""
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Act
        response = await client.get("/endpoint")
        
        # Assert
        assert response.status_code == 200
        assert "expected_key" in response.json()
```

#### Coverage Requirements
- Minimum 80% coverage for new code
- Test happy paths and error cases
- Use mocking for external dependencies

#### Running Tests
```bash
# All tests with coverage
pytest --cov=api --cov-report=html

# Specific test file
pytest tests/test_api.py -v

# Specific test
pytest tests/test_api.py::test_name -v
```

### Frontend Testing

#### Build Test
```bash
npm run build
```

Should complete without errors.

---

## 📝 Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
# Feature
git commit -m "feat(backend): add caching for frequent topics"

# Bug fix
git commit -m "fix(frontend): resolve CORS error on API calls"

# Documentation
git commit -m "docs: update deployment guide with new steps"

# Multiple lines
git commit -m "feat(agent): improve prompt engineering

- Add more context to prompts
- Include specific formatting instructions
- Test with various topics

Closes #123"
```

### Commit Message Guidelines

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Capitalize first letter
- No period at the end
- Reference issues and PRs when applicable

---

## 🔀 Pull Request Process

### Before Submitting

- ✅ Code follows style guidelines
- ✅ Tests pass locally
- ✅ New tests added for new features
- ✅ Documentation updated
- ✅ Commit messages follow convention
- ✅ Branch is up to date with main

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How to test these changes

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] Commit messages follow convention

## Related Issues
Closes #123
```

### Review Process

1. Automated checks must pass (CI/CD)
2. At least one maintainer approval required
3. Address review comments
4. Keep PR focused and reasonably sized
5. Squash commits if requested

### After Merge

- Delete your feature branch
- Update your local main:
  ```bash
  git checkout main
  git pull upstream main
  ```

---

## 📁 Project Structure

### Adding New Features

#### Backend Route
1. Create model in `api/models/`
2. Create service in `api/services/`
3. Create route in `api/routes/`
4. Register in `api/main.py`
5. Add tests in `tests/`

#### Frontend Component
1. Create component in `src/components/`
2. Add to parent component
3. Update API service if needed
4. Test in browser

### File Organization

- Keep files focused and small
- One class per file
- Related files in same directory
- Use clear, descriptive names

---

## 🐛 Reporting Bugs

### Before Reporting

- Check existing issues
- Try latest version
- Verify it's reproducible

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 11]
- Python: [e.g., 3.11]
- Node.js: [e.g., 18.0]
- Browser: [e.g., Chrome 120]

**Additional context**
Any other information
```

---

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Other solutions considered

**Additional context**
Mockups, examples, etc.
```

---

## 📞 Getting Help

- **Documentation**: Check [README.md](README.md)
- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Chat**: [If you have a Discord/Slack]

---

## 🏆 Recognition

Contributors will be:
- Listed in contributors section
- Mentioned in release notes
- Appreciated in community

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉

Every contribution, no matter how small, makes this project better. We appreciate your time and effort!

---

**Happy Coding!** 🚀
