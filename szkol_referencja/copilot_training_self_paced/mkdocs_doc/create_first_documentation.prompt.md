---
mode: 'agent'
---

# Instruction

Generate complete documentation according to best practices and
 all the assumptions and requirements described below.

# Documentation Guidelines

The documentation should be in Markdown format compatible with the MkDocs -
 it's crucial to follow the structure and naming conventions outlined below.
  The documentation will be used for a project hosted on GitLab Pages.

## Required Sections

Each section should be a separate file named after the section, placed in its own directory.
 The file name should reflect its content.

- **Introduction**  
  Describe the project, its purpose, and main business functionalities.

- **Configuration**  
  Explain how to configure the application and its business functionalities.  
  Additionally, include a table listing all properties with descriptions of their responsibilities.

- **Architecture Description**  
  Provide a C4 model architecture overview. Generate the architecture diagram using mermaid syntax.

- **Open API Documentation**  
  Include Open API documentation.

- **Index**
  Create an index file that links to all the documentation sections.  
  The index should be named `index.md` and placed in the root directory of the documentation.

## Example Documentation Structure

```
docs/
 ├─ architecture/architecture.md
 ├─ introduction/introduction.md
 ├─ open-api/open-api.md
 └─ index.md
```

## Additional Requirements

- Use clear and concise language.
- Documentation must be in English.
- Documentation should be complete, readable, and up-to-date, ready for publication on GitLab Pages.
- Act as a technical writer and follow best practices for documentation.
- Act as a software architect and provide a comprehensive overview of the system architecture.
- Act as a software developer and include detailed API documentation.

# Next Steps
- generate mkdocs.yml file based on example (mkdosc-example)[../instructions/mkdocs-example.md]