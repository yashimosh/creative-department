# Contributing

Thanks for looking at `creative-department`. This file lays out what's in scope, what isn't, and how to contribute without friction.

## Project scope

This is a **reference implementation** for running agentic creative production with Claude. It is opinionated on purpose — brand voice gets calibrated, review is a hard gate, content goes through a registry, skills compose.

**In scope:**
- Bug fixes in existing skills
- Documentation improvements (typos, clarity, examples)
- New skills that fit the existing compositional model
- Better examples in `clients/example-brand/`
- Tooling that reduces friction (install scripts, CI, test fixtures)

**Out of scope:**
- Converting the package into a SaaS, hosted service, or platform
- Removing opinionated defaults in favor of generality
- Adding features that require Claude to run "in autopilot" without the review gates
- Visual / aesthetic overhauls that contradict the Ulm + Constructivist design direction in the package's own brand assets

If you're unsure whether a change is in scope, open an issue before opening a PR.

## How to contribute

### Bug fixes and documentation

1. Open a pull request directly. Reference the file(s) you changed.
2. Keep the PR focused — one bug or one documentation topic per PR.
3. Include a before/after if the change is a behavior fix.

### New features / new skills

1. **Open an issue first.** Describe the gap, the proposed addition, and how it composes with existing skills.
2. Wait for maintainer feedback before implementing. Feature PRs opened without a prior issue may be closed.
3. Follow the skill structure: a dedicated folder with `SKILL.md`, install/usage docs, and any wrapper scripts.

### Style and structure

- Documentation is written in the same register as the existing docs — flat, practitioner, specific. No marketing copy.
- Each skill has a `SKILL.md` front-matter block (`skill`, `type`, `status`, `last-updated`).
- Output conventions follow the `brand/exports/REG-XXXX--slug/` pattern where applicable.

## What to expect from the maintainer

- Response within 48 hours on issues and PRs when the project is active
- Friendly close on scope-violating PRs — we'll explain why, not just say no
- No roadmap promises. The project evolves based on real client work.

## Code of conduct

Be direct, be specific, be kind. The full policy is in [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
