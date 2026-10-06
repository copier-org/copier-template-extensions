# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.3.4](https://github.com/pawamoy/copier-templates-extensions/releases/tag/0.3.4) - 2026-10-06

<small>[Compare with 0.3.3](https://github.com/pawamoy/copier-templates-extensions/compare/0.3.3...0.3.4)</small>

### Build

- Drop support for Python 3.10 ([c147cb7](https://github.com/pawamoy/copier-templates-extensions/commit/c147cb74ad638e71cf6c10ef821ea37af6accb3b) by Timothée Mazzucotelli).

## [0.3.3](https://github.com/pawamoy/copier-templates-extensions/releases/tag/0.3.3) - 2025-07-15

<small>[Compare with 0.3.2](https://github.com/pawamoy/copier-templates-extensions/compare/0.3.2...0.3.3)</small>

### Code Refactoring

- Expose old paths to ease migration ([4206907](https://github.com/pawamoy/copier-templates-extensions/commit/420690745a82a88d5a447e977bf1486f2690e707) by Timothée Mazzucotelli). [PR-16](https://github.com/copier-org/copier-template-extensions/pull/16)

## [0.3.2](https://github.com/pawamoy/copier-templates-extensions/releases/tag/0.3.2) - 2025-07-15

<small>[Compare with 0.3.1](https://github.com/pawamoy/copier-templates-extensions/compare/0.3.1...0.3.2)</small>

- Rename project to `copier-template-extensions` (singular template), to be proper english: Copier Template-Extensions.

## [0.3.1](https://github.com/pawamoy/copier-template-extensions/releases/tag/0.3.1) - 2025-03-10

<small>[Compare with 0.3.0](https://github.com/pawamoy/copier-template-extensions/compare/0.3.0...0.3.1)</small>

### Dependencies

- Depend on Copier 9.2+ ([43679a9](https://github.com/pawamoy/copier-template-extensions/commit/43679a9719b2d05e041e674bde1f10dee21984a6) by Timothée Mazzucotelli).

### Bug Fixes

- Add loaded module to `sys.modules` to help libraries using data from annotation scopes ([a290f27](https://github.com/pawamoy/copier-template-extensions/commit/a290f271e302db88bcc755d57c647e4f3a8043ff) by Axel H.). [PR-12](https://github.com/copier-org/copier-template-extensions/pull/12)

### Code Refactoring

- Move modules into internal folder (and simplify API docs) ([a8c0377](https://github.com/pawamoy/copier-template-extensions/commit/a8c03770298f51fa07667598fd7d0b72196aecad) by Timothée Mazzucotelli).
- Pass globals to parent constructor ([ea4567b](https://github.com/pawamoy/copier-template-extensions/commit/ea4567bcfad0f17764e17d6b7fd12a7fd7a33cba) by Timothée Mazzucotelli).
- Deprecate the "update" aspect of context hooks ([876c055](https://github.com/pawamoy/copier-template-extensions/commit/876c0554e34b630ab255111b69da74db16439dcb) by Timothée Mazzucotelli). [Issue-4](https://github.com/copier-org/copier-template-extensions/issues/4)

## [0.3.0](https://github.com/copier-org/copier-template-extensions/releases/tag/0.3.0) - 2022-09-12

<small>[Compare with 0.2.0](https://github.com/copier-org/copier-template-extensions/compare/0.2.0...0.3.0)</small>

### Build
- Require Copier v6+ (Python >= 3.7) ([6380c90](https://github.com/copier-org/copier-template-extensions/commit/6380c90a3e26c596790d9a083673dcf1dd613678) by Timothée Mazzucotelli).


## [0.2.0](https://github.com/copier-org/copier-template-extensions/releases/tag/0.2.0) - 2021-12-27

<small>[Compare with 0.1.1](https://github.com/copier-org/copier-template-extensions/compare/0.1.1...0.2.0)</small>

### Build
- Match Python cap to Copier's ([a04f938](https://github.com/copier-org/copier-template-extensions/commit/a04f93813f9795b64cbd9d21209dd5e5127b3eb4) by Timothée Mazzucotelli).

### Features
- Support Jinja2 version 3.x ([55211df](https://github.com/copier-org/copier-template-extensions/commit/55211df29c4118c2603cc18ea4a1bc4247e41176) by Timothée Mazzucotelli).


## [0.1.1](https://github.com/copier-org/copier-template-extensions/releases/tag/0.1.1) - 2021-03-29

<small>[Compare with 0.1.0](https://github.com/copier-org/copier-template-extensions/compare/0.1.0...0.1.1)</small>

### Bug Fixes
- Fix loader extension ([7d8b9e8](https://github.com/copier-org/copier-template-extensions/commit/7d8b9e8cf2de66fafc9953ff5d4ba4e210470649) by Timothée Mazzucotelli).

### Code Refactoring
- Raise error from abstract hook ([52494f8](https://github.com/copier-org/copier-template-extensions/commit/52494f8d02505027da0733a7beb9269fc2ba8c3e) by Timothée Mazzucotelli).
- Raise Copier errors from loader extension ([c136feb](https://github.com/copier-org/copier-template-extensions/commit/c136febaa4ed719f5a0919e2fa073862258e7143) by Timothée Mazzucotelli).
- Rename context module, inherit from default context class ([855284a](https://github.com/copier-org/copier-template-extensions/commit/855284ad2112feecd6b2a8dfc38dbbd397d29275) by Timothée Mazzucotelli).


## [0.1.0](https://github.com/copier-org/copier-template-extensions/releases/tag/0.1.0) - 2021-03-29

<small>[Compare with first commit](https://github.com/copier-org/copier-template-extensions/compare/e74578393a7cffe4e502640a6092e789d2cc6f29...0.1.0)</small>

### Code Refactoring
- Reorganize code ([474b617](https://github.com/copier-org/copier-template-extensions/commit/474b6173f3970c7713643b7cbc16f11f32a70e5c) by Timothée Mazzucotelli).

### Features
- Add context hook extension ([ce95212](https://github.com/copier-org/copier-template-extensions/commit/ce952126afb282cfa1fbf18366a6f857426eeaa1) by Timothée Mazzucotelli).
- Add initial contents ([e745783](https://github.com/copier-org/copier-template-extensions/commit/e74578393a7cffe4e502640a6092e789d2cc6f29) by Timothée Mazzucotelli).
