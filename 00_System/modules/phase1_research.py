#!/usr/bin/env python3
"""
Phase 1: リサーチ & コンセプト定義
テーマとターゲットから記事コンセプトを自動生成
"""

from pathlib import Path
import anthropic
import os


def load_claude_api_key():
    """Claude APIキーを読み込む"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        return api_key.strip()
    
    env_paths = [
        Path("/Users/keigo/001_cursor/.env"),
        Path("/Users/keigo/001_cursor/文字起こしブースター/mioji_share_v2/.env"),
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key == "ANTHROPIC_API_KEY":
                                return value.strip()
            except Exception:
                continue
    
    return None


def generate_concept_with_claude(theme, target, claude_client):
    """Claude APIでコンセプトを生成"""
    prompt = f"""あなたはプロのマーケティングリサーチャーです。Brain/Tips向けの情報商材のコンセプトを設計してください。

【テーマ】
{theme}

【ターゲット】
{target}

【タスク】
以下のフォーマットでコンセプトを設計してください：

# コンセプト定義

## テーマ
{theme}

## ターゲットペルソナ

### 基本属性
- 年齢: 
- 性別: 
- 職業: 
- 年収: 

### 抱えている悩み・課題
1. 
2. 
3. 

### 目指している理想の未来
- 

## 提供価値

### 核となる価値
- 

### 具体的なメリット
1. 
2. 
3. 

### このnoteを読むことで得られる成果
- 

## 差別化ポイント

### 競合との違い
1. 
2. 
3. 

### 独自の強み
- 

## 価格戦略

### 定価設定
- 定価: 4,980円

**理由**:
- 情報商材の相場（5,000円前後）
- 実践的ノウハウの価値
- 競合価格との比較

### 初回限定価格
- 初回限定: 100円（24時間限定）

**理由**:
- 心理的ハードルを極限まで下げる
- 缶コーヒー1本分の価格で「試しやすさ」を訴求
- 緊急性（24時間限定）で即決を促す
- 100円購入者をLINE登録に誘導し、リスト化

### マネタイズ導線
1. Brain/Tipsで100円note販売
2. 購入者に特典でLINE登録を促す
3. LINE登録者に継続的な価値提供
4. バックエンド商品（高額商品・コンサル）へ誘導

## デザインコンセプト（NanoBanana用）

### カラーパレット
- メインカラー: ゴールド（#FFD700）- 成功、富、権威を象徴
- アクセントカラー: ブラック（#000000）- 高級感、信頼性
- サブカラー: ホワイト（#FFFFFF）- 清潔感、可読性

### デザインスタイル
- 3Dメタリック質感
- 太字ゴシック体（ExtraBold/Black）
- 光沢エフェクト（グロウ、陰影）
- 動的な抽象背景（光線、粒子、エネルギー波）

### 訴求方向性
- 成功イメージ（上昇、成長、達成）
- 緊急性（限定、ラストチャンス）
- 信頼性（実績、データ、権威）

---

上記のフォーマットに従って、具体的な内容を記載してください。
"""
    
    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        text = response.content[0].text
        return text, response.usage.input_tokens, response.usage.output_tokens
    
    except Exception as e:
        print(f"    ❌ エラー: {str(e)}")
        return None, 0, 0


def run(project_dir, theme, target):
    """Phase 1実行"""
    print("  ├─ Claude APIキー読み込み中...")
    claude_key = load_claude_api_key()
    
    if not claude_key:
        print("  ⚠️  Claude APIキーが見つかりません")
        return None
    
    print("  │  └─ Claude APIキー: OK")
    
    # Claude クライアント初期化
    claude_client = anthropic.Anthropic(api_key=claude_key)
    
    # コンセプト生成
    print("  ├─ コンセプト生成中（Claude API）...")
    print(f"  │  ├─ テーマ: {theme}")
    print(f"  │  └─ ターゲット: {target}")
    
    concept_text, input_tokens, output_tokens = generate_concept_with_claude(
        theme, target, claude_client
    )
    
    if not concept_text:
        print("  ⚠️  コンセプト生成失敗")
        return None
    
    print(f"  │  └─ コンセプト生成完了 ({len(concept_text)}文字)")
    
    # concept_definition.md を生成
    print("  ├─ concept_definition.md 生成中...")
    research_dir = project_dir / "01_Research"
    research_dir.mkdir(parents=True, exist_ok=True)
    
    concept_file = research_dir / "concept_definition.md"
    concept_file.write_text(concept_text, encoding="utf-8")
    
    print(f"  │  └─ {concept_file.name} 保存完了")
    
    print("  └─ Phase 1完了")
    
    return {
        "concept_file": str(concept_file),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }

