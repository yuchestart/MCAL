scoreboard players add @e[tag=MCAL_RUNTIME_VARMANAGER,limit=1] MCAL_RUNTIME_STACKPTR 1
execute store result storage mcal_core:stack stack_ptr int 1 run scoreboard players get @e[tag=MCAL_RUNTIME_VARMANAGER,limit=1] MCAL_RUNTIME_STACKPTR

$data modify storage mcal_core:stack stack_registry append value $(data)