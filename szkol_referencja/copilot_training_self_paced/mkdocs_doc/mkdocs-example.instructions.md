---
applyTo: 'mkdocs.yml'
---
# Example of mkdocs.yml
```yml
site_name: Application Name 
site_url: https://gitlab.czk.comarch/toss/inv/application-path
repo_name: toss/inv/application-path
repo_url: https://gitlab.czk.comarch/toss/inv/application-path
  name: material
  palette:
    - scheme: default
      toggle:
        icon: material/weather-sunny
        name: Switch to dark mode
    - scheme: slate
      toggle:
        icon: material/weather-night
        name: Switch to light mode
  features:
    - navigation.sections
  language: en
nav:
  - Home: index.md
  - Introduction: introduction.md
  - Configuration: configuration.md
  - Architecture: architecture.md
  - Swagger API: swagger-api.md
markdown_extensions:
  - toc:
      permalink: true
  - attr_list
  - footnotes
  - admonition
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format

plugins:
  - search
  - swagger-ui-tag
```