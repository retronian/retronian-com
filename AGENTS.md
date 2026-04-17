# Repository Guidelines

## Project Structure & Module Organization

This is a small Jekyll site for Retronian. Top-level pages live in `index.html`,
`about.md`, and `blog/index.html`. Blog posts are Markdown files in `_posts/`
using Jekyll front matter with fields such as `layout`, `title`, `date`,
`description`, `tags`, `note_key`, and `source_url`. Layout templates are in
`_layouts/`, reusable fragments are in `_includes/`, and static CSS/JavaScript
assets are in `assets/css/` and `assets/js/`. Generated output in `_site/`
should not be edited directly. Automation for importing and translating note.com
posts lives in `scripts/translate_note_posts.py` and
`.github/workflows/translate-note-posts.yml`.

## Build, Test, and Development Commands

- `bundle install`: install Ruby gems from `Gemfile.lock`.
- `bundle exec jekyll serve`: run the local site at `http://localhost:4000`.
- `bundle exec jekyll build`: build the static site into `_site/` and catch
  template or Markdown rendering errors.
- `DRY_RUN=1 ANTHROPIC_API_KEY=... python scripts/translate_note_posts.py`:
  exercise the note.com translator without writing new posts.

There is no dedicated automated test suite. Use `bundle exec jekyll build` as
the main validation step before opening a pull request.

## Coding Style & Naming Conventions

Use two-space indentation in HTML, YAML, CSS, and JavaScript where practical.
Keep Jekyll front matter valid YAML and quote strings that contain punctuation.
Name posts with Jekyll's required pattern: `_posts/YYYY-MM-DD-url-friendly-slug.md`.
Keep tags lowercase and hyphenated, for example `retro-handheld`. Python scripts
should follow standard PEP 8 style with clear function names and UTF-8 file IO.

## Content Guidelines

Posts are English translations of Retronian note.com articles. Preserve source
meaning, links, images, lists, and code blocks. Do not invent details or add
marketing copy. When adding posts manually, include `source_url` and `note_key`
when the content originates from note.com.

## Commit & Pull Request Guidelines

Recent history uses short, imperative commit subjects, such as `Fix: resolve
Sass encoding error and post rendering`, plus automated commits like
`Auto-translate new note.com post(s): ...`. Keep subjects concise and specific.
Pull requests should describe the content or code change, list validation
performed, link any related issue, and include screenshots for visible layout or
style changes. Do not include generated `_site/` changes unless deployment
requires them.

## Security & Configuration Tips

Never commit API keys. The translator requires `ANTHROPIC_API_KEY`, supplied
locally through the environment and in GitHub Actions through repository
secrets. Keep deployment settings aligned with GitHub Pages and the custom
domain in `CNAME`.
