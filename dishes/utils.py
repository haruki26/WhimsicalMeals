"""料理名生成のためのユーティリティ関数."""

from __future__ import annotations

import random  # 暗号学的用途ではないため問題なし

# 定数定義
MIN_INGREDIENTS = 2
MAX_INGREDIENTS = 4
MIN_INGREDIENTS_FOR_PAIR = 2
DISH_TYPE_PROBABILITY = 0.3  # 料理タイプを使用する確率 (30%)
MAX_ATTEMPTS_MULTIPLIER = 10  # 無限ループを防ぐ試行回数の倍率

# 料理名生成テンプレート
DISH_NAME_TEMPLATES = [
    "{0}と{1}の{2}",
    "{0}{1}{2}",
    "{0}入り{1}{2}",
    "{0}まみれの{1}",
    "特製{0}{1}",
    "{0}と{1}の奇跡",
    "禁断の{0}{1}",
    "{0}{1}爆弾",
    "{0}風{1}",
    "秘密の{0}{1}",
    "{0}と{1}の冒険",
    "謎の{0}{1}",
    "{0}{1}の饗宴",
    "幻の{0}{1}",
    "{0}まみれ{1}スペシャル",
]

# 料理名に使用する料理のタイプと接尾語
DISH_TYPES = [
    "丼",
    "炒め",
    "煮込み",
    "焼き",
    "蒸し",
    "揚げ",
    "和え",
    "サラダ",
    "スープ",
    "カレー",
    "パスタ",
    "リゾット",
    "グラタン",
    "フリッター",
    "テリーヌ",
    "ムース",
    "コンポート",
    "マリネ",
    "カルパッチョ",
    "タルタル",
    "料理",
    "アラモード",
    "フィナンシェ",
    "キッシュ",
    "ポタージュ",
    "ビスク",
    "チャウダー",
    "ガスパチョ",
    "タプナード",
    "ペースト",
    "ジュレ",
    "エスプーマ",
    "コンフィ",
    "ロースト",
    "ブレゼ",
    "ポシェ",
]


def generate_dish_name(ingredient_names: list[str]) -> str:
    """材料名から架空の料理名を生成する.

    Args:
        ingredient_names: 使用する材料名のリスト

    Returns:
        生成された料理名

    Raises:
        ValueError: 材料が不足している場合
    """
    if len(ingredient_names) < MIN_INGREDIENTS_FOR_PAIR:
        msg = "料理を生成するには少なくとも2つの材料が必要です。"
        raise ValueError(msg)

    # 材料を2-4個ランダムに選択(最大で利用可能な材料数まで)
    num_ingredients = min(random.randint(MIN_INGREDIENTS, MAX_INGREDIENTS), len(ingredient_names))  # noqa: S311
    selected_ingredient_names = random.sample(ingredient_names, num_ingredients)

    # テンプレートをランダム選択
    template = random.choice(DISH_NAME_TEMPLATES)  # noqa: S311

    # テンプレートに応じて料理名を生成
    if "{2}" in template:
        # 3つのプレースホルダーがある場合
        if len(selected_ingredient_names) >= MIN_INGREDIENTS_FOR_PAIR:
            dish_type = random.choice(DISH_TYPES)  # noqa: S311
            return template.format(selected_ingredient_names[0], selected_ingredient_names[1], dish_type)
        return template.format(selected_ingredient_names[0], selected_ingredient_names[0], random.choice(DISH_TYPES))  # noqa: S311

    if "{1}" in template:
        # 2つのプレースホルダーがある場合
        if len(selected_ingredient_names) >= MIN_INGREDIENTS_FOR_PAIR:
            # 時々料理タイプを2番目の材料の代わりに使用
            if random.random() < DISH_TYPE_PROBABILITY:  # noqa: S311
                return template.format(selected_ingredient_names[0], random.choice(DISH_TYPES))  # noqa: S311
            return template.format(selected_ingredient_names[0], selected_ingredient_names[1])
        return template.format(selected_ingredient_names[0], random.choice(DISH_TYPES))  # noqa: S311

    # 1つのプレースホルダーまたはプレースホルダーなし
    return template.format(selected_ingredient_names[0])


def generate_multiple_dish_names(
    ingredient_names: list[str],
    count: int = 3,
) -> list[str]:
    """複数の料理名を生成する.

    Args:
        ingredient_names: 使用する材料名のリスト
        count: 生成する料理名の数

    Returns:
        生成された料理名のリスト
    """
    if len(ingredient_names) < MIN_INGREDIENTS_FOR_PAIR:
        msg = "料理を生成するには少なくとも2つの材料が必要です。"
        raise ValueError(msg)

    generated_names = set()
    max_attempts = count * MAX_ATTEMPTS_MULTIPLIER  # 無限ループを防ぐ
    attempts = 0

    while len(generated_names) < count and attempts < max_attempts:
        try:
            name = generate_dish_name(ingredient_names)
            generated_names.add(name)
        except ValueError:
            break
        attempts += 1

    return list(generated_names)
