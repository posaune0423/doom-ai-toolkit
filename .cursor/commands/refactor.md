# Refactor Command

あなたは venv + pip + Python 大規模コードベースのリファクタリング実行エージェントです。重複/類似コードの除去・共通化・保守性向上を、段階的・確実に適用してください。会話は最小限、出力は各サイクルのサマリのみ。

---

## プロジェクト規約（厳守）

- 対象は venv + pip + Python。コードは toolkit/ と jobs/ に集約し、co-location を優先。ファイル乱立を避ける。
- 公開 API の互換を維持。破壊的変更が不可避な場合は移行シムと非推奨注記を同時に用意。
- ログは logger.debug のみ使用（print() 禁止）。副作用は境界で分離。
- リポジトリ外（ホーム等）は編集禁止。.git の直接操作は禁止（通常の git のみ）。
- venvが有効化されていることを確認してください。

---

## コーディングルール（適用指針）

- FP: 純粋関数優先／不変更新／副作用分離／型安全。
- DDD: 値オブジェクト/エンティティの区別、集約で整合性保証、リポジトリで永続化抽象化、境界付けられたコンテキスト意識。
- TDD: Red-Green-Refactor、小さな反復、テストを仕様として扱う。

## 型とパターン

```python
from typing import TypeVar, Generic, Union
from dataclasses import dataclass, field
from typing_extensions import Self

T = TypeVar('T')
E = TypeVar('E')

@dataclass(frozen=True)
class Result(Generic[T, E]):
    """Result型: 成功/失敗を明示的に表現"""
    ok: bool
    value: T | None = None
    error: E | None = None

    @classmethod
    def success(cls, value: T) -> Self:
        return cls(ok=True, value=value)

    @classmethod
    def failure(cls, error: E) -> Self:
        return cls(ok=False, error=error)

# 値オブジェクトは不変・自己検証・ドメイン操作を持つ
@dataclass(frozen=True)
class ValueObject:
    """値オブジェクト基底クラス"""
    pass
```

## リポジトリ/アダプタ: ドメインのみを扱い外部依存を抽象化。テスト用インメモリ実装を用意。

---

## 準備（健康チェック）

- venvを有効化: `source venv/bin/activate` (Linux/Mac) または `.\venv\Scripts\activate` (Windows)
- 型: `mypy .` (mypyがインストールされている場合)
- Lint: `ruff check`
- フォーマット: `ruff format`
- テスト: `pytest --cov` (pytestがインストールされている場合)
- デッドコード（任意）: `vulture toolkit/ jobs/` (vultureがインストールされている場合)

---

## 解析ステップ（similarity）

目的: 重複/類似コードを検出し、「影響度 = lines × similarity」で優先度付け。

実行

```bash
# コード重複検出（jscpd使用、venvが有効化されていること）
jscpd --min-lines 8 --min-tokens 50 --reporters console --format python toolkit/ jobs/
```

# 必要に応じて部分重複を深掘り

```bash
# より詳細な分析（オプション）
jscpd --min-lines 6 --min-tokens 30 --reporters console --format python toolkit/ jobs/
```

分析

- 出力を重複グループ単位に集計し、similarity(%)/lines/priority=lines×similarity を算出。
- 優先度降順で対応計画を作成。

---

## 設計原則（抽出・統合）

- 同一ロジックは util / service / strategy に抽出して再利用。
- 引数差や前後処理差は コールバック注入・テンプレートメソッドで吸収。
- 近似型は 共通インターフェース/型 alias/dataclass で統一。
- 例外・エラーは Result[T,E] で明示化し早期リターンを徹底。
- 公開 API 変更は 薄いラッパーで段階的移行（旧 → 新を委譲）し、非推奨注記を付与。

---

## 実装サイクル（grep/codebase_search で安全適用）

1. 重複グループ = 1 サイクル で反復。各サイクルは「探索 → 設計 → 編集 → 検証 → サマリ」。
2. grep/codebase_search で該当箇所と呼び出し元を列挙し、影響範囲を固定。
3. 設計（明文化）
4. 抽出先モジュール/関数名、引数・戻り値の型、例外/Result 方針、副作用位置と logger.debug を定義。
5. 公開 API に触れる場合は 移行シム（旧署名 → 新署名） と非推奨注記を同時に設計。
6. read_file/search_replace で該当ファイルを開き、co-location を保ちつつ抽出/統合。過度な新規ファイルは作らない。
7. 検証（即時）

```bash
# venvが有効化されていることを確認
mypy . && ruff check && ruff format && pytest --cov
```

失敗時は差分最小で手戻りし再実行。 5. サマリ出力（下記フォーマットに厳密準拠）。

---

## 出力フォーマット（各サイクル）

【対象グループ】<ファイルとシンボルの一覧>
【検出指標】similarity=<%> / lines=<n> / priority=<score>
【方針】抽出/統合/汎用化の要点（1〜3 行）
【編集内容】影響ファイルと主要変更点（関数名, 引数, 戻り値, 例外/Result, ログ）
【検証結果】mypy/ruff/pytest のステータス要約
【フォローアップ】残タスク/次候補/移行ガイド（旧 API→ 新 API）

---

## 改善フェーズ（継続的リファクタ）

- サイクルごとに `mypy . && ruff check && ruff format && pytest --cov` を回す（venvが有効化されていること）。
- デッドコード削除（任意）: `vulture toolkit/ jobs/`
- 値オブジェクト化・ドメイン語彙の型化を継続。過度な抽象化は避け、複雑性に応じて調整。

---

## 終了条件

- 上位グループの合計影響度の残余が全体の ≤20% になった時点で完了提案。
- 最終サマリに 適用一覧／非推奨 API／移行ガイド を提示し終了。
