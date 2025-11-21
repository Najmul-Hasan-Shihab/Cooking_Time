# Contributing to Recipe Website

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## 🎯 Getting Started

### 1. Set Up Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd Recipe_website

# Copy environment variables
cp .env.example .env

# Start development environment
docker-compose up
```

### 2. Create a Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or changes

## 📝 Development Workflow

### 1. Make Your Changes

- Follow the [Code Style Guide](CODESTYLE.md)
- Write clean, readable code
- Add tests for new functionality
- Update documentation as needed

### 2. Test Your Changes

#### Backend Tests
```bash
cd backend
python manage.py test
```

#### Frontend Tests
```bash
cd frontend
npm test
```

#### Manual Testing
- Test in development environment (`docker-compose up`)
- Verify changes in browser
- Check API endpoints with tools like Postman or curl

### 3. Commit Your Changes

Follow the commit message format from [CODESTYLE.md](CODESTYLE.md):

```bash
git add .
git commit -m "feat(recipes): add ingredient search functionality"
```

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what was changed and why
- Reference to related issues (e.g., "Closes #123")
- Screenshots for UI changes

## 🔍 Pull Request Guidelines

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
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manually tested

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #<issue-number>
```

### Review Process

1. At least one approval required before merging
2. All CI checks must pass
3. Address reviewer feedback
4. Keep PR scope focused and manageable

## 🐛 Reporting Bugs

### Before Submitting

- Check if the bug has already been reported
- Verify it's reproducible in the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Version: [e.g., 1.0.0]

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of what you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Mockups, examples, or references
```

## 📚 Development Guidelines

### Backend (Django)

1. **Models**
   - Use MongoEngine for MongoDB models
   - Add proper validation
   - Include docstrings

2. **Views/ViewSets**
   - Keep views thin
   - Use serializers for validation
   - Add proper error handling

3. **API Endpoints**
   - Follow REST conventions
   - Version your API (e.g., `/api/v1/`)
   - Document with OpenAPI/Swagger

4. **Testing**
   - Write unit tests for models
   - Write integration tests for APIs
   - Aim for >80% code coverage

### Frontend (React)

1. **Components**
   - Create reusable components
   - Use TypeScript for type safety
   - Keep components focused and small

2. **State Management**
   - Use React hooks for local state
   - Use context or state library for global state
   - Keep state as close to where it's used as possible

3. **Styling**
   - Use TailwindCSS utilities
   - Follow mobile-first approach
   - Ensure accessibility (a11y)

4. **Testing**
   - Write tests for complex components
   - Test user interactions
   - Use React Testing Library

## 🔒 Security

### Reporting Security Issues

**Do NOT open public issues for security vulnerabilities.**

Instead:
1. Email security concerns to [security@example.com]
2. Include detailed description
3. Provide steps to reproduce
4. Suggest a fix if possible

### Security Best Practices

- Never commit secrets or API keys
- Sanitize user input
- Use parameterized queries
- Implement rate limiting
- Follow OWASP guidelines

## 📋 Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `priority: high` - High priority
- `priority: low` - Low priority
- `phase-0` through `phase-10` - Project phases

## 🎨 Design Contributions

### UI/UX Contributions

1. Follow the card-based design system
2. Maintain consistency with existing components
3. Consider mobile responsiveness
4. Include hover states and animations
5. Ensure accessibility standards

### Design Resources

- Color palette: [To be defined]
- Typography: [To be defined]
- Component library: [To be defined]

## 📞 Communication

### Channels

- GitHub Issues - Bug reports and feature requests
- GitHub Discussions - General questions and ideas
- Pull Requests - Code reviews and discussions

### Best Practices

- Be respectful and constructive
- Provide context and examples
- Stay on topic
- Help others when you can

## 📜 Code of Conduct

### Our Standards

- Be welcoming and inclusive
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## ✅ Checklist Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added and passing
- [ ] No new warnings
- [ ] Commit messages follow convention
- [ ] PR description is clear

## 🙏 Thank You!

Your contributions make this project better. We appreciate your time and effort!

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
