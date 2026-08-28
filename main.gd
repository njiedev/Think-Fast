extends Node


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	## Variable Definitions
	const POOL_TEMPLATE: UnitPool = preload("res://unit_pool.tres")
	var runtime_pool: UnitPool = POOL_TEMPLATE.duplicate(true)
	var shop := Shop.new()
	var shopOddData: ShopOddsData = preload("res://shop_odds.tres")
	var unitDB: UnitDatabase = load("res://unit_database.tres")
	
	print(shop.reroll(5,runtime_pool,shopOddData,unitDB))
	print(shop.reroll(7,runtime_pool,shopOddData,unitDB))
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
