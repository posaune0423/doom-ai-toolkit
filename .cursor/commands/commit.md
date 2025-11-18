### Command: Commit current changes in logical groups (simple)

Do exactly this, non-interactively, from repo root.

1. Ignore when staging:
   - Follow .gitignore strictly. Additionally, ignore: .cursor/\*\* (except this file), .env

2. Define groups and scopes:
   - infra → requirements.txt, docker/**, docker-compose.yml, README.md, .vscode/**
   - core → toolkit/**, jobs/**, *.py (root level scripts)
   - scripts → scripts/**, notebooks/**
   - config → config/**, extensions/**/config/**
   - data → dataset/**, output/**
   - ui → ui/**
   - docs → docs/**, *.md
   - tests → testing/**

3. For each group that has changes, stage and commit (by intent/responsibility, not only folder):
   - Decide values:
     - ${emoji}:{fix=🐛, feat=✨, docs=📝, style=💄, refactor=♻️, perf=🚀, test=💚, chore=🍱}
     - ${type} in {fix, feat, docs, style, refactor, perf, test, chore}
     - ${scope} = group name (e.g., infra|core|scripts|config|data|ai|docs|tests)
     - ${summary} = 1-line imperative (<=72 chars)
     - ${body} = 1–3 bullets (optional)
   - Commands:
     - git add -A -- -- ${file1} ${file2} ${fileN}
     - git commit --no-verify --no-gpg-sign -m "${emoji} ${type}(${scope}): ${summary}" -m "${body}"

4. Commit order: chore → docs → style → refactor → perf → feat → fix → test

5. Final check:
   - git -c core.pager=cat status --porcelain=v1 | cat

Message template:
Title: "${emoji} ${type}(${scope}): ${summary}"
Body: "- ${changes}\n- ${reasonImpact}"

Example:
git add -A -- -- src/service/generation_service.py src/models/config.py
git commit --no-verify --no-gpg-sign -m "✨ feat(core): 画像生成サービスの設定管理機能を追加" -m "- 設定モデルの統合\n- バリデーション機能の実装"
