data modify storage mcal_core:internal_functionargs args.stackptr set from storage mcal_core:stack stack_ptr
$data modify storage mcal_core:internal_functionargs args.path set value $(path)

return run function mcal_core:internals/read with storage mcal_core:internal_functionargs args