MCAL Symbol Declaration
====

**Version 0.3.1**
Author: Che Yu
Date: 2025-03-11
Minecraft Version(s): 1.21.4 - 1.21.5

# Overview
MCAL Symbol Declaration (MSD for short) is used to declare external symbols for use by MCAL Programs.

They provide definitions for commands, entities, items, methods, and other things you may want to know.



# MCAL Declarations




# Minecraft Declarations

## Entities

Entities can be declared similarly to structs
```msd
struct entity<[namespace:name]>{
    [similar to structs]
}

```

## Items
Items are declared like structs
```msd
struct item<[namespace:name]>{
    ...
}
```
## Commands
Commands are declared as follows
```msd
command [namespace:name]{
    [returntype]|[format]
    [returntype]|[format]
    ...
}
```
### Command Format
The command format is a PCRE2 regular expression, however there are a few magic tags:
```
<dtype> - This is a value of datatype dtype in the command. All primitives are allowed, and some others are listed below.
<command> - As written, this command takes another command. Only one is allowed.
```

Aside from MCAL primitives, other datatypes are allowed in commands. Example:
* `selector` - An entity selector
* `selector_single` - An entity selector that only allows one entity
* `name` - A resource name, like `minecraft:stone`
* `path` - An nbt path
* `item` - An item definition

If you need to use the actual symbol `<` or `>` in the regular expression, then escape it with a backslash.

Datatype can be of any datatype, or of `command_ret`, which means it returns whatever the command was written in.
If data type is unknown, use `unknown`.
Use the `void` return type to denote no return type.

Example:
```msd
command minecraft:item{
    void|modify (?:block <coordinate>|entity <selector>) <path> <name>?
    void|replace (?:block <coordinate>|entity <selector>) <path> with <item> <int>
    void|replace (?:block <coordinate>|entity <selector>) <path> from (?:block <coordinate>|entity <selector>) <path> <name>?
}

command minecraft:data{
    unknown|get (?:block <coordinate>|entity <selector_single>|storage <name>) <path> <double>
    unknown|merge (?:block <coordinate>|entity <selector_single>|storage <name>) <compound>
    void|modify (?:block <coordinate>|entity <selector_single>|storage <name>) <path> append from (?:block <coordinate>|entity <selector_single>|storage <name>) <path>
    //... more stuff
}
```
### Command Aliases
To create an alias to another command, use the `alias_of` keyword.
Usage:
```msd
command [namespace:name] alias_of [namespace:name]
```
Example:
```
command minecraft:teleport alias_of minecraft:tp;
```

# Interop

If you want to expose a traditional command datapack to MCAL, note the following:
 * MCAL will use function macros to pass parameters. This goes for both exposing and calling functions to/from MCAL.
 * MCAL will use certain reserved variables for variable managment. Usually there are no collisions but don't use any reserved names.