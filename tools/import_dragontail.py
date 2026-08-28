#!/usr/bin/env python3
"""Generate Godot Set 17 resources from a local Dragontail release."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


INTERNAL_UNIT_IDS = {
    "TFT17_DarkStar_FakeUnit",
    "TFT17_Enemy_Aatrox",
    "TFT17_IvernMinion",
    "TFT17_MissFortune_TraitClone",
}


def godot_string(value: str) -> str:
    """JSON and Godot use compatible quoting for ordinary strings."""
    return json.dumps(value, ensure_ascii=False)


def resource_filename(unit_id: str) -> str:
    return unit_id.removeprefix("TFT17_").lower() + ".tres"


def load_set_17_champions(champion_json: Path) -> list[dict]:
    document = json.loads(champion_json.read_text(encoding="utf-8"))
    champions = []

    for source_path, champion in document["data"].items():
        if "/TFTSet17/Shop/" not in source_path:
            continue
        if champion["id"] in INTERNAL_UNIT_IDS:
            continue
        if champion["tier"] not in range(1, 6):
            continue
        champions.append(champion)

    return sorted(champions, key=lambda unit: (unit["tier"], unit["name"]))


def write_unit_resource(project_root: Path, source_img_dir: Path, unit: dict) -> Path:
    filename = resource_filename(unit["id"])
    image_filename = unit["image"]["full"]
    source_image = source_img_dir / image_filename
    project_image = project_root / "assets" / "units" / "set17" / image_filename
    unit_resource = project_root / "units" / "set17" / filename

    if not source_image.is_file():
        raise FileNotFoundError(f"Missing champion image: {source_image}")

    project_image.parent.mkdir(parents=True, exist_ok=True)
    unit_resource.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_image, project_image)

    unit_resource.write_text(
        "\n".join(
            [
                '[gd_resource type="Resource" script_class="UnitData" load_steps=3 format=3]',
                "",
                '[ext_resource type="Script" path="res://unit_data.gd" id="1_script"]',
                f'[ext_resource type="Texture2D" path="res://assets/units/set17/{image_filename}" id="2_image"]',
                "",
                "[resource]",
                'script = ExtResource("1_script")',
                f'id = {godot_string(unit["id"])}',
                f'unit_name = {godot_string(unit["name"])}',
                f'rarity = {unit["tier"] - 1}',
                'unit_image = ExtResource("2_image")',
                'metadata/_custom_type_script = "res://unit_data.gd"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return unit_resource


def write_database(project_root: Path, unit_resources: list[Path]) -> None:
    ext_resources = [
        '[ext_resource type="Script" path="res://unit_data.gd" id="1_unit_script"]',
        '[ext_resource type="Script" path="res://unit_database.gd" id="2_database_script"]',
    ]
    references = []

    for index, resource in enumerate(unit_resources, start=3):
        resource_path = resource.relative_to(project_root).as_posix()
        resource_id = f"{index}_unit"
        ext_resources.append(
            f'[ext_resource type="Resource" path="res://{resource_path}" id="{resource_id}"]'
        )
        references.append(f'ExtResource("{resource_id}")')

    content = [
        f'[gd_resource type="Resource" script_class="UnitDatabase" load_steps={len(ext_resources) + 1} format=3]',
        "",
        *ext_resources,
        "",
        "[resource]",
        'script = ExtResource("2_database_script")',
        f'units = Array[ExtResource("1_unit_script")]([{", ".join(references)}])',
        'metadata/_custom_type_script = "res://unit_database.gd"',
        "",
    ]
    (project_root / "unit_database.tres").write_text("\n".join(content), encoding="utf-8")


def write_shop_odds(project_root: Path, odds_json: Path) -> None:
    document = json.loads(odds_json.read_text(encoding="utf-8"))
    levels = document["data"]["Shop"]
    max_level = max(level["level"] for level in levels)
    rates_by_level: list[list[int]] = [[] for _ in range(max_level + 1)]

    for level in levels:
        rates_by_level[level["level"]] = [
            tier["rate"] for tier in sorted(level["dropRatesByTier"], key=lambda tier: tier["cost"])
        ]

    packed_arrays = [
        "PackedInt32Array()"
        if not rates
        else f"PackedInt32Array({', '.join(str(rate) for rate in rates)})"
        for rates in rates_by_level
    ]
    content = [
        '[gd_resource type="Resource" script_class="ShopOddsData" load_steps=2 format=3]',
        "",
        '[ext_resource type="Script" path="res://shop_odds_data.gd" id="1_script"]',
        "",
        "[resource]",
        'script = ExtResource("1_script")',
        f'rates_by_level = Array[PackedInt32Array]([{", ".join(packed_arrays)}])',
        'metadata/_custom_type_script = "res://shop_odds_data.gd"',
        "",
    ]
    (project_root / "shop_odds.tres").write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dragontail_root", type=Path, help="Path to the versioned Dragontail folder")
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    data_dir = args.dragontail_root / "data" / "en_US"
    image_dir = args.dragontail_root / "img" / "tft-champion"
    champions = load_set_17_champions(data_dir / "tft-champion.json")
    resources = [write_unit_resource(args.project, image_dir, unit) for unit in champions]
    write_database(args.project, resources)
    write_shop_odds(args.project, data_dir / "tft-shop-drop-rates-data.json")

    print(f"Imported {len(resources)} Set 17 champions and shop odds.")


if __name__ == "__main__":
    main()
