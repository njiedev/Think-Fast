
class_name UnitDatabase
extends Resource

@export var units: Array[UnitData] = []

func get_by_id(unit_id: String) -> UnitData:
	for unit in units:
		if unit.id == unit_id:
			return unit

	return null
func remove_unit(unit_id: String) -> void:
	units.erase(get_by_id(unit_id))
	
	
