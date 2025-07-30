# 気まぐれレシピ研究所 (WhimsicalMeals)

**このREADMEはAIを使用し作成しています**

---

架空の料理名を生成して楽しむDjangoアプリケーションです。手持ちの材料から創造的な料理名を自動生成し、コミュニティで共有することができます。

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/haruki26/WhimsicalMeals.git
cd WhimsicalMeals
```

### 2. VS Code Dev Container で開く

#### 前提条件
- [Docker](https://www.docker.com/ja-jp/)または[Docker Desktop](https://www.docker.com/products/docker-desktop) がインストールされていること
- [Visual Studio Code](https://code.visualstudio.com/) がインストールされていること
- [Dev Containers拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) がインストールされていること

#### 起動手順

1. **VS Codeでプロジェクトを開く**
```bash
code .
```

2. **Dev Containerで開く**
- VS Codeが起動したら、画面右下に「Reopen in Container」の通知が表示されます
- 通知をクリックするか、コマンドパレット（`Ctrl+Shift+P` / `Cmd+Shift+P`）を開いて「Dev Containers: Reopen in Container」を実行

3. **初期化の完了を待つ**
- 初回起動時はDockerイメージのビルドと依存関係のインストールが実行されます
- ターミナルで以下のコマンドが自動実行されるのを確認してください

### 3. 開発サーバーの起動

Dev Containerが起動したら、以下のコマンドでサーバーを開始できます：

```bash
# データベースのマイグレーション
uv run python manage.py migrate

# 開発サーバーの起動
uv run python manage.py runserver
```

### 4. アプリケーションへのアクセス

ブラウザで [http://localhost:8000](http://localhost:8000) にアクセスしてアプリケーションを確認できます。

## uvを使用しない場合のセットアップ

uvが利用できない環境や、従来のPython環境を使用したい場合の手順です。

### 前提条件
- Python 3.12以上がインストールされていること
- pipが利用可能であること

### セットアップ手順

1. **リポジトリのクローン**
```bash
git clone https://github.com/haruki26/WhimsicalMeals.git
cd WhimsicalMeals
```

2. **仮想環境の作成と有効化**
```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate
```

3. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

4. **データベースのセットアップ**
```bash
# マイグレーションの実行
python manage.py migrate
```

5. **開発サーバーの起動**
```bash
# サーバーの起動
python manage.py runserver
```

6. **アプリケーションへのアクセス**

ブラウザで [http://localhost:8000](http://localhost:8000) にアクセスしてアプリケーションを確認できます。

### 利用可能なコマンド（uv非使用）

```bash
# サーバー起動
python manage.py runserver

# マイグレーション作成
python manage.py makemigrations

# マイグレーション実行
python manage.py migrate

# スーパーユーザー作成
python manage.py createsuperuser

# テスト実行
python manage.py test

# 静的ファイル収集
python manage.py collectstatic
```

### 注意事項
- 依存関係の管理はpipとrequirements.txtに依存します
- uvを使用した場合と比べて、パッケージ管理が複雑になる可能性があります
- 本プロジェクトではuvの使用を推奨しています

## �🛠️ 開発環境の詳細

### 技術スタック
- **Backend**: Django 5.x
- **Frontend**: SCSS, Vanilla JavaScript
- **Database**: SQLite (開発環境)
- **Build Tool**: uv
- **Container**: Docker + Dev Container

### プロジェクト構成
```
WhimsicalMeals/
├── .devcontainer/          # Dev Container設定
├── config/                 # Django設定
├── dishes/                 # 料理生成アプリ
├── ingredients/            # 材料管理アプリ
├── users/                  # ユーザー認証アプリ
├── core/                   # 共通機能
├── static/                 # 静的ファイル
├── templates/              # テンプレート
├── manage.py
├── pyproject.toml
└── README.md
```

### 利用可能なコマンド

```bash
# サーバー起動
uv run python manage.py runserver

# マイグレーション作成
uv run python manage.py makemigrations

# マイグレーション実行
uv run python manage.py migrate

# スーパーユーザー作成
uv run python manage.py createsuperuser

# テスト実行
uv run python manage.py test

# 静的ファイル収集
uv run python manage.py collectstatic
```

## 📝 主な機能

- 🎲 **料理名生成**: 手持ちの材料から創造的な料理名を自動生成
- 📋 **材料管理**: 個人の材料リストを管理
- ❤️ **いいね機能**: 気に入った料理にいいねを付与
- 🏆 **ランキング**: 人気の料理をランキング表示
- 🔐 **ユーザー認証**: アカウント作成・ログイン機能

## 🎯 使い方

1. **アカウント作成**: 新規登録でアカウントを作成
2. **材料登録**: 手持ちの材料を登録
3. **料理生成**: 材料を選んで架空の料理名を生成
4. **料理保存**: 気に入った料理名を保存
5. **コミュニティ**: 他のユーザーの料理を見ていいねを付与
