scoreboard objectives add MCAL_RUNTIME_STACKPTR dummy
scoreboard players set @e[tag=MCAL_RUNTIME_VARMANAGER] MCAL_RUNTIME_STACKPTR -1
data merge storage mcal_core:stack {stack_registry:[],stack_ptr:0}
data merge storage mcal_core:functionargs {args:{},name:""}
data merge storage mcal_core:internal_functionargs {args:{}}