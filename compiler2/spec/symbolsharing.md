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

entrypoint<minecraft:load> void main(){

    tellraw!(@a "${PI}"); // Output(chat): 3.14

    someModule.afunction(); // Output(chat): hi world

    bfunction(); // Output(chat): public static void main(String[] args)

}

```

# `extern`

# Namespaces

## `using`

## `namespace`
