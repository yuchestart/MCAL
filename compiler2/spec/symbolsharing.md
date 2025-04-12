Symbol Sharing
====
[Go Back](./spec.md)

# Overview

MCAL Projects can be composed of multiple source files, in which case symbols might be needed to be shared across source files.

MCAL provides a system to do just that.

# Basic symbol sharing

## `export`

The `export` keyword is used to export a symbol to be used in other files.

Usage:
 * `export [symbolnames,...]`
 Exports `[symbolnames,...]`
 * `export *`
 Exports all the symbols in this file.
 * `export [symboldef]`
 Exports the defined symbol.

Examples:
```
const string secret = "we collect data";

void afunction(){
    tellraw!(@a "I will remove all the zombies.");
    kill!(@e[type=minecraft:zombie]);
}

export void anotherfunction(){
    msg!(@p "Psst. The secret is ${secret}.");
    kill
}

```

## `import`

The `import` keyword is used to import a symbol from another file.

Usage:
 * `import "[path-to-file]"`
 This imports all the symbols from `[path-to-file]` to the global namespace.
 * `import "[path-to-file]" as [name]`
 This imports all the symbols from `[path-to-file]` under namespace `[name]`
 * `import {[symbols]} from "[path-to-file]"`
 This imports `[symbols]` from `[path-to-file]`

Examples:
```
// ==== some_module.mcal ====
export void afunction(){
    tellraw!(@a "hi world");
}

export void bfunction(){
    tellraw!(@a "public static void main(String[] args)");
}

// some_other_module.mcal
export const double PI = 3.14;

// ==== main.mcal ====

import "some_other_module.mcal"; // Import all the symbols from some_other_module.mcal
import "some_module.mcal" as someModule; // Import all the symbols from some_module.mcal under namespace someModule
import { bfunction } from "some_module.mcal"; // Import "bfunction" from some_module.mcal

extern<minecraft:load> void main(){

    tellraw!(@a "${PI}"); // Output(chat): 3.14

    someModule.afunction(); // Output(chat): hi world

    bfunction(); // Output(chat): public static void main(String[] args)

}

```

## External symbols

### `extern`
> [!IMPORTANT]
> The `extern` keyword only applies to defined functions and class methods.
>
> Class methods marked `extern` are required to be `public` and `static`[^1].

> [!CAUTION]
> Be careful when using MCAL methods outside of MCAL programs, as they aren't your usual datapack functions.

The `extern` keyword is used to make a symbol available outside of the MCAL program. There are several reasons to do this, e.g.
 * You're writing a library for use by other MCAL programs or datapacks, and need to share symbols
 * You're exposing a command to the user to be invoked by `function`.

Symbols marked `extern` do not necessarily have to be exported.

Usage:
```
extern<namespace:name> [symboldefinition]
extern<namespace:name> [identifier]
```

Example:
```mcal
extern<minecraft:load> void main(){
    tellraw!(@a "hello world!")
}

void somethingelse(){
    execute<as @p at @s>{
        summon!(minecraft:sheep ~ ~ ~);
    };
}

class MyClass{
    extern<mynamespace:add> public static int add(int a, int b){
        return a + b;
    }

    public static int subtract(int a, int b){
        return a - b;
    }
}

extern<mynamespace:somethingelse> somethingelse;
extern<mynamespace:subtract> MyClass::subtract;
```

### Using external symbols

The calling convention for MCAL functions is similar to a regular function.
```mcfunction
function namespace:name { "name":<value>,... }
```
Return values from MCAL functions are stored in a storage called `namespace:mcal_runtime`, with the path `func_return_value`.

Example:
```mcfunction
# This could also be done with a function macro, however I'm gonna use scoreboard
scoreboard objectives add calculation;

# Add two numbers
function mynamespace:add {"a":5,"b":6}

# Move the result to the scoreboard objective
execute store result score @p calculation run data get storage mynamespace:mcal_runtime func_return_value 1

# Say the result
tellraw @a '{"type":"score","score":{"name":"@p","objective":"calculation"}}'
# Output(chat): 11
```

# Namespaces

## `namespace`
If you want to group symbols under a namespace, use the `namespace` keyword. When declaring things under a namespace, the namespace is used by default.

Usage:
```
namespace [name] { [symbols] }
namespace [name]
```

Example:
```mcal
namespace math {
    compound 
}


```

## `using`





[^1]: This may change in the future, depending on how class instances work.