# AAYU Release Checklist

## Pre-Release Tasks

### Code Quality
- [ ] All tests passing (`pytest`)
- [ ] No linting errors (`flake8`, `black`)
- [ ] Type checking clean (`mypy`)
- [ ] Code coverage adequate
- [ ] Security scan passed
- [ ] No hardcoded secrets/API keys

### Documentation
- [ ] README.md updated and complete
- [ ] CHANGELOG.md entry added for this release
- [ ] API documentation current
- [ ] Examples in `grammar_examples/` working
- [ ] Getting started guide updated
- [ ] Contributing guidelines current

### Version Management
- [ ] Version bumped in:
  - [ ] `pyproject.toml` (version field)
  - [ ] `setup.py` (version field)
  - [ ] `vscode-aayu/package.json` (if releasing extension)
  - [ ] Documentation site
- [ ] Changelog lists all changes for this version

### Package Configuration
- [ ] `MANIFEST.in` properly configured
- [ ] `pyproject.toml` metadata complete
- [ ] `setup.py` consistent with `pyproject.toml`
- [ ] Package dependencies accurate
- [ ] Entry points correct (CLI commands)
- [ ] License file included

### GitHub & Linguist
- [ ] Linguist PR submitted (if language addition)
- [ ] Repository settings properly configured
- [ ] GitHub Pages enabled
- [ ] CI/CD workflows passing
- [ ] Branch protection rules set

### Extension (if applicable)
- [ ] VS Code extension icons correct
- [ ] Extension metadata updated
- [ ] Extension tests passing
- [ ] `vscode-aayu` ready for marketplace
- [ ] VSIX file generated and tested

## Release Day

### 1. Build Verification
```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build distribution
python -m build

# Verify
twine check dist/*
```

### 2. Create Git Tag
```bash
git tag -a v1.0.0 -m "Release AAYU v1.0.0"
git push origin v1.0.0
```

### 3. Create GitHub Release
- Go to: https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/new
- Tag: `v1.0.0`
- Title: `AAYU v1.0.0 - <Release Name>`
- Description: Include:
  - Major features
  - Bug fixes
  - Breaking changes
  - Installation instructions
  - Thank you acknowledgments

### 4. Monitor CI/CD
- [ ] `publish-pypi.yml` workflow triggered
- [ ] Build successful
- [ ] Package uploaded to PyPI
- [ ] Verify on https://pypi.org/project/aayu-lang/

### 5. Post-Release Verification
```bash
# Install from PyPI
pip install aayu-lang==1.0.0

# Run sanity checks
aayu --version
aayu --help
```

### 6. Announcements
- [ ] Update website with release info
- [ ] Tweet/social media announcement
- [ ] Share on relevant forums/platforms
- [ ] Update GitHub discussions
- [ ] Email notification to subscribers (if applicable)

### 7. Extension Release (VS Code)
```bash
cd vscode-aayu
npm version patch
vsce publish
```

## Post-Release

### Immediate
- [ ] Close release milestone
- [ ] Merge release branch
- [ ] Delete release branch
- [ ] Create `development` branch for next version
- [ ] Update version to next dev version

### Short-term (1-2 weeks)
- [ ] Monitor bug reports
- [ ] Check PyPI download stats
- [ ] Verify documentation pages work
- [ ] Confirm VS Code marketplace listing
- [ ] GitHub Linguist approval/merge

### Medium-term (1 month)
- [ ] Community feedback collected
- [ ] Performance benchmarks run
- [ ] Security audit complete
- [ ] Plan next release

## Release Versions

### Semantic Versioning
- **MAJOR** (X.0.0): Breaking changes, major features
- **MINOR** (X.Y.0): New features, backwards compatible
- **PATCH** (X.Y.Z): Bug fixes, minor improvements

Example versions:
- `1.0.0` - Initial release
- `1.1.0` - New features added
- `1.1.1` - Bug fix
- `2.0.0` - Major rewrite/breaking changes

## Key Files Checklist

### Root Directory
- [ ] `setup.py` - updated
- [ ] `pyproject.toml` - updated
- [ ] `MANIFEST.in` - includes all necessary files
- [ ] `README.md` - current
- [ ] `CHANGELOG.md` - updated
- [ ] `LICENSE` - valid

### GitHub
- [ ] `.github/workflows/publish-pypi.yml` - configured
- [ ] `.github/workflows/deploy.yml` - passing
- [ ] Repository settings correct
- [ ] Branch protections set

### Documentation
- [ ] `docs/` - all guides current
- [ ] `website/` - all pages deploy
- [ ] Examples updated

### Tests
- [ ] `tests/` - all passing
- [ ] Coverage adequate
- [ ] Integration tests work

## Emergency: Yank Release

If critical bug found after release:

```bash
# Yank from PyPI (mark as unsafe)
pip install twine
twine upload --skip-existing dist/aayu-lang-1.0.0.tar.gz --config-file ~/.pypirc

# Create hotfix release
git tag v1.0.1
git push origin v1.0.1
```

---

## Contact & Support

- **Maintainer**: AAYU Team
- **Email**: support@aayu.org
- **Issues**: https://github.com/Minato95-ayu/INTENT-TO-SILICON/issues
- **Discussions**: https://github.com/Minato95-ayu/INTENT-TO-SILICON/discussions
