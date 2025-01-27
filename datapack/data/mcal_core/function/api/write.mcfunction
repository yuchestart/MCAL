data modify storage mcal_core:internal_functionargs args.stackptr set from storage mcal_core:stack stack_ptr
$data modify storage mcal_core:internal_functionargs args.path set value $(path)
$data modify storage mcal_core:internal_functionargs args.value set value $(value)

return run function mcal_core:internals/write with storage mcal_core:internal_functionargs args