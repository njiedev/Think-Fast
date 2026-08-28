# unit_data.gd
class_name UnitData
extends Resource

enum Rarity {
	ONECOST,
	TWOCOST,
	THREECOST,
	FOURCOST,
	FIVECOST
}

@export var id: String
@export var unit_name: String
@export var rarity: Rarity
@export var unit_image: Texture2D
