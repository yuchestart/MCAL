function mcal_core:internals/destroystack with storage mcal_core:stack

scoreboard players remove @e[tag=MCAL_RUNTIME_VARMANAGER] MCAL_RUNTIME_STACKPTR 1
execute store result storage mcal_core:stack stack_ptr int 1 run scoreboard players get @e[tag=MCAL_RUNTIME_VARMANAGER,limit=1] MCAL_RUNTIME_STACKPTR