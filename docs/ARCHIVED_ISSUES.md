# 📦 Archived Issues - Not Currently Planned for Implementation

This file tracks issues that are not planned for implementation in the current roadmap but are kept for future reference or alternative approaches.

## How Issues Are Archived

Issues are moved here when:
1. Technology decisions make them obsolete (e.g., choosing Firebase over PostgreSQL)
2. Feature scope changes make them unnecessary
3. Alternative implementations provide the same functionality
4. Resource constraints require deprioritization
5. Business requirements change

---

## Issue #13: Database Integration (PostgreSQL) 📦 ARCHIVED
**Archive Date:** 2025-01-31
**Archive Reason:** Using Firebase instead of PostgreSQL for data persistence
**Status:** 📦 ARCHIVED
**GitHub URL:** https://github.com/emanlaw/InternalPMTool/issues/13

**Description:**
Title: [FEATURE] Database Integration (PostgreSQL)

Description:
Replace JSON file storage with proper PostgreSQL database integration for better data management and scalability.

What I want:
- PostgreSQL database setup and configuration
- Database models for projects, cards, users, comments
- Migration from JSON to database storage
- Connection pooling and optimization
- Database backup and recovery procedures

Core Requirements:
- [ ] PostgreSQL database setup and configuration
- [ ] SQLAlchemy ORM integration with Flask
- [ ] Database models for all entities (users, projects, cards, comments)
- [ ] Migration scripts from JSON to PostgreSQL
- [ ] Database connection management and pooling
- [ ] Environment-based configuration (dev/staging/prod)

Database Schema Design:
- [ ] Users table with authentication and profile data
- [ ] Projects table with metadata and settings
- [ ] Cards/Issues table with full issue tracking
- [ ] Comments table with threaded discussion support
- [ ] Tags/Labels table for categorization
- [ ] Relationships and foreign key constraints

Performance Optimization:
- [ ] Database indexing for common queries
- [ ] Query optimization and performance monitoring
- [ ] Connection pooling configuration
- [ ] Caching layer for frequently accessed data
- [ ] Database backup and recovery procedures

Migration Strategy:
- [ ] Data export from current JSON storage
- [ ] Database schema creation and validation
- [ ] Data import with integrity checks
- [ ] Rollback procedures for failed migrations
- [ ] Testing with production-like data volumes

**Archive Notes:**
- The project has adopted Firebase as the primary database solution
- Firebase provides real-time capabilities and easier deployment
- PostgreSQL integration would require significant infrastructure changes
- Current Firebase implementation meets all data persistence needs
- This issue may be reconsidered for enterprise deployments requiring on-premise solutions

---

## Template for Archived Issues:

```
## Issue #X: [Feature Name] 📦 ARCHIVED
**Archive Date:** YYYY-MM-DD
**Archive Reason:** Brief explanation of why archived
**Status:** 📦 ARCHIVED
**GitHub URL:** https://github.com/emanlaw/InternalPMTool/issues/X

**Description:**
[Original issue description]

**Archive Notes:**
- Reason for archiving
- Alternative solutions implemented
- Conditions for potential future consideration
- Related issues or dependencies

---
```

## Archive Statistics
- **Total Archived Issues**: 1
- **Archive Reasons**:
  - Technology Decision Changes: 1 issue
  - Scope Changes: 0 issues
  - Resource Constraints: 0 issues
  - Business Requirement Changes: 0 issues