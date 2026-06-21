# GitHub Linguist & PyPI Release Guide for AAYU

## 1️⃣ GitHub Linguist Submission

### What is GitHub Linguist?
Linguist is GitHub's library for detecting and highlighting programming languages. Adding AAYU to Linguist means `.aayu` files will be automatically recognized and syntax-highlighted on GitHub.

### Steps to Submit:

1. **Fork the Linguist Repository**
   ```bash
   git clone https://github.com/github-linguist/linguist.git
   cd linguist
   git checkout -b add-aayu-language
   ```

2. **Copy the AAYU Language Definition**
   ```bash
   cp ../Linguist-Aayu.yml lib/linguist/languages/Aayu.yml
   ```

3. **Add Language Samples** (Optional but recommended)
   ```bash
   mkdir -p samples/AAYU
   cp ../test.aayu samples/AAYU/test.aayu
   cp ../apm-test/main.aayu samples/AAYU/main.aayu
   cp ../apm-test/test_ml.aayu samples/AAYU/test_ml.aayu
   ```

4. **Test Locally**
   ```bash
   bundle install
   bundle exec rake test
   ```

5. **Create Pull Request**
   - Push to your fork
   - Create PR to `github-linguist/linguist`
   - Reference AAYU GitHub repo in the description
   - Include language samples and use cases

### Example PR Description:
```markdown
# Add AAYU Programming Language Support

This PR adds support for **AAYU**, the Intent-to-Silicon Programming Language.

## About AAYU
- **Repository**: https://github.com/Minato95-ayu/INTENT-TO-SILICON
- **File Extension**: `.aayu`
- **Use Case**: Intent-driven, full-stack programming language with built-in web framework, SQLite, RBAC, and Workflows
- **Target Audience**: Full-stack developers, AI/ML engineers, enterprise application builders

## Language Features
- Deterministic Architecture Definition Language (ADL)
- Native Intent Engine (AI-powered code generation)
- Built-in HTTP framework, database ORM, authentication, RBAC
- Workflow and state machine support
- Syntax similar to Python/Ruby with domain-specific extensions

## Sample Code
See attached `.aayu` examples in `samples/AAYU/`

## Files Changed
- `lib/linguist/languages/Aayu.yml` - Language definition
- `samples/AAYU/*.aayu` - Example code samples
```

---

## 2️⃣ PyPI Release

### Prerequisites
```bash
pip install twine build setuptools wheel
```

### Step 1: Update Version in pyproject.toml
```toml
[project]
version = "1.0.0"  # Change to your release version
```

### Step 2: Create Release Notes
Create `RELEASE_NOTES.md` documenting:
- New features
- Bug fixes
- Breaking changes
- Upgrade instructions

### Step 3: Build Distribution Locally
```bash
python -m build
```

This generates:
- `dist/aayu-lang-1.0.0.tar.gz` (source distribution)
- `dist/aayu_lang-1.0.0-py3-none-any.whl` (wheel)

### Step 4: Verify Distribution
```bash
twine check dist/*
```

### Step 5: Upload to Test PyPI (Optional)
```bash
twine upload --repository testpypi dist/*
```

Then test install:
```bash
pip install --index-url https://test.pypi.org/simple/ aayu-lang
```

### Step 6: Upload to Production PyPI

**Option A: Using GitHub Actions (Recommended)**
1. Create a GitHub Release:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
2. Go to GitHub → Releases → Create Release from tag
3. The workflow `publish-pypi.yml` will automatically build and upload

**Option B: Manual Upload**
```bash
twine upload dist/*
```

You'll be prompted for PyPI credentials. Alternatively, create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # Your PyPI token
```

Then:
```bash
twine upload dist/*
```

### Step 7: Verify Package
After upload, verify on PyPI:
```
https://pypi.org/project/aayu-lang/
```

Install from PyPI:
```bash
pip install aayu-lang
```

---

## 3️⃣ CI/CD Setup

The repository already has:
- ✅ `publish-pypi.yml` - Automatic PyPI publishing on release

### Future Enhancements
- Test PyPI upload on PR
- Automated changelog generation
- GitHub release creation from Git tags
- Package security scanning

---

## 📋 Checklist Before Release

- [ ] All tests passing
- [ ] Version bumped in `pyproject.toml`
- [ ] `CHANGELOG.md` updated
- [ ] README.md current
- [ ] No hardcoded API keys/secrets
- [ ] License specified (MIT)
- [ ] Package metadata complete
- [ ] Linguist PR submitted (if first-time language addition)
- [ ] Git tag created (`git tag vX.Y.Z`)
- [ ] GitHub Release created with notes

---

## 📚 Resources

- [Linguist Documentation](https://github.com/github-linguist/linguist)
- [PyPI Packaging Guide](https://packaging.python.org/)
- [PEP 517 - Build System Interface](https://www.python.org/dev/peps/pep-0517/)
- [PEP 621 - Project Metadata](https://www.python.org/dev/peps/pep-0621/)

---

## 🚀 Quick Commands

```bash
# Build locally
python -m build

# Check distribution
twine check dist/*

# Test install locally
pip install --index-url https://test.pypi.org/simple/ aayu-lang

# Create release
git tag v1.0.0
git push origin v1.0.0

# Upload to PyPI
twine upload dist/*
```
