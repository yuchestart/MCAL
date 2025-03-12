# MCAL (Minecraft Command Abstraction Language) Specification

**Version 0.2.1**  
_Author: Che Yu_

---

## Basic Syntax

All statements must be seperated by a semicolon.
```mcal
dec int health = 20i; //Semicolon here,
for(dec int i=0i; i<15; set i = i+1){
    tellraw!(@a "$(i)"); //here,
}; //here,
tellraw!(@a "I'm done!"); //and here.
```



## Modules

### Overview

Modules are kind of like reusable building blocks of code.

All code is organized into modules:

```mcal
module Example {
    // Classes, variables, and functions go here
};
```

Modules can also be defined across files:
```mcal
//someimportantfunction.mcal
module Example{
    function void someImportantFunction(){
        //...
    };
};
```

```mcal
//example.mcal
module Example{
    entrypoint<load> function void main(){
        someImportantFunction();
    };
};
```

### Symbol sharing

Modules can be imported and have exported symbols.

```
//math.mcal
module Math{
    function int add(int a, int b){
        return a + b;
    };
    
    function int subtract(int a, int b){
        return a - b;
    };
    export add,subtract;
};
```

```
//main.mcal
import Math;

module main{
    entrypoint<main> function void main(){
        dec int result = Math::add(1,2);
        tellraw!(@a "$(result)");
    };
};
```

In the case where you want code outside of your MCAL program(e.g. libraries, commands) to access MCAL functions, you can add the `extern` keyword to modules.

Any exported symbols within that module can be accessed outside of your MCAL program.

```
//api.mcal

extern module api{
    function void someImportantSymbol(int aparam){
        tellraw!(@a "yowsg");
        tellraw!(@a "The Param is $(aparam)");
    };
    export someImportantSymbol;
};
```

```
//someotherprogram.mcal

import MyLibrary::api;

module main{
    entrypoint<load> function void main(){
        MyLibrary::api::someImportantSymbol(5i);
    };
};
```

### The `using` keyword

The `using` keyword is used to reference namespaces without explicitly defining them. The intent of this is to make code more readable.

Usage:
```mcal
using [symbolname];
```

Example:
```mcal
import SomeRandomModule::SomeOtherRandomModule;

using SomeRandomModule::SomeOtherRandomModule;

module main{
    entrypoint<load> function void onLoad(){
        //Previously, I would've had to type SomeRandomModule::SomeOtherRandomModule::someFunction
        //With the 'using' keyword, I can just do:
        someFunction();
    };
};

```

## Variables

### Declaration

Variables are an essential part of programming. There are many ways to declar variables.

```mcal
dec int myvar;              // Declare a variable
dec int health = 20i;       // Declare a variable with a starting value
dec_scoreboard dummy kills; // Declare a variable that uses the scoreboard
```

`dec` declares variables in the NBT storage

`dec_scoreboard` creates a scoreboard objective. `dec_scoreboard` initializes variables to ints only.

Usage:

`dec [datatype] [name]`

`dec [datatype] [name] = [value]`

`dec_scoreboard [criteria] [name]`

### Data Types

Here are the primitive data types:
| Type Name    | Example                    |
| ------------ | -------------------------- |
| `int`        | `5i`                       |
| `float`      | `3.14f`                    |
| `double`     | `3.141592d`                |
| `long`       | `1000l`                    |
| `byte`       | `3b`                       |
| `bool`       | `true `                    |
| `seconds`    | `12s`                      |
| `ticks`      | `3t`                       |
| `coord`      | `~100 ~64 ~`               |
| `string`     | `"text"`                   |
| `nbt_object` | `{"a":"b","c":[1i,2i,3i]}` |
| `uuid`       | `[555l,555l,555l,555l]`    |

There are also pointers, represented as follows:
`[datatype or class name]&`

Pointers can point to primitives, classes, and even other pointers.

## Classes

### Overview

Classes are kind of like an nbt_object that has set properties.

Classes can also have instance methods, which allow them to be manipulated.

Classes can only be passed around as pointers, however they can be converted back into NBT objects as needed.

### Definition

To define a class, you use the following syntax:
```mcal
class [classname]{
    [classmembers]
};
```
Example:
```mcal
class Player {
    int health;
    ct position;
    static int count;

    static function Player& create(int health, ct pos) {
        dec Player& p = @Player;
        set p->health = health;
        return p;
    }

    function void takeDamage(Player& self,int amount){
        set self->health = self->health - amount;
    }
}
```

### Instantiation
To instantiate a class, you use the following: `@[classname]`. This returns a pointer to the class that you have just instantiated.

> _**NOTE**_<br>
> The `@` operator will NOT call a factory function you have created (in this case `Player::create`). It will instead create a new class and initialize it each variable to `0` or something similar. If you want to use the factory function, call it directly.

To create a deep copy of the class, you use the following: `#[class identifier]`. The class identifier is basically the variable name of the class. When using this, it will return a pointer to the new class, different from the original.

```mcal
dec Player& player = @Player;
set player->health = 20i;
dec Player& copy = #player; // Deep copy
```

### NBT Object Conversion

To convert a class back into an NBT object, you use the following:
`#[class identifier]`. This will return a new NBT object based on the class's properties.

> _**NOTE**_<br>
> In order to convert an NBT Object back into a class, you will have to do it manually. There is no automatic way in the MCAL specification to do it.

```
dec Player& player = @Player;

dec nbt_object mynbt = #player; //Convert player to an nbt object
```

## Functions

### Basic
Usage:
```mcal
function [return type] [function name] ( [parameters] ){
    [code];  
};
```
Example:
```mcal
function int add(int a, int b) {
    return a + b;
}
```

### Entrypoints
Entrypoints define special functions that are used by minecraft, like tick and load

Usage:
```mcal
entrypoint<[entrypoint type]>
```
Example:
```mcal
entrypoint<tick> void onTick() {
    // Runs every tick
}

entrypoint<load> void onLoad() {
    // Runs on datapack load
}
```

---

## Control Flow

### Conditionals

```mcal
if (player->health < 10i) {
    heal(player);
} elif (player->health == 0i) {
    respawn!(@s);
} else {
    tellraw!(@a "You're perfectly fine bruh");
}
```

### Loops

```mcal
for (dec int i = 0i; i < 10i; i++) {
    tellraw!(@a "Count: $(i)");
}

while (someCondition()){
    tellraw!(@a "Still going...");
}

```

---

## Commands

### Overview

Sometimes you may need to execute normal minecraft commands. MCAL has several features for this purpose.

### Invocation

To invoke a command, use the following:

```mcal
[command name]!( [command arguments] )
```
Example:
```mcal
tp!(@e[type=minecraft:pig] #0 #1 #0);
```

### Substitution

When running a command, you may need to use variables within MCAL.

### Execute
Sometimes you may need to use the `execute` command. MCAL allows you to use `execute` as a block. However, traditional execute will still work.
```mcal
//Chaining multiple commands
execute<as @e[type=pig]> {
    particle!(minecraft:flame ~ ~ ~);
    particle!(minecraft:flame ~ ~1 ~);
}

//Still works!
execute!(as @e[type=sheep] run kill @s);
```

### Raw Commands

If you ever need to run a bunch of raw commands at once, you can use the raw command execution block to do just that. Here's what it looks like:
```
![ [your commands here] ]!
```
And here it is in action:
```mcal
dec int myvar = 5;
//Use a raw execution block to execute commands
![
    // Comments look like this in a raw execution block.
    say "This is pure Minecraft syntax. Now I'm gonna kill all the zombies."
    kill @e[type=zombie]
    say "Value of myvar: $(myvar)"
]!
```
> _**NOTE**_
> If you need to use `]!` in your commands, escape them as follows: `\]\!s`
## Pointers

## Operators

| Operator | Purpose              |
| -------- | -------------------- |
| `->`     | Class member access |
| `@`      | Class instantiation |
| `#`      | Deep copy            |
| `::`     | Static method access |
| `$()`    | Inline substitution  |
| `+` | Add | Binary |
| `-` | Subtract | Binary |
| `*` | Multiply | Binary |
| `/` | Divide | Binary |
| `%` | Modulo | Binary |
| `==` | Equal to | Binary |
| `!=` | Not equal to | Binary |
| `&&` | Logical and | Binary |
| <code>\|\|</code> | Logical or | Binary |
| `!` | Logical not | Unary |


---

## Examples

### Simple programs

```mcal
module Game {
    class Player {
        int health;
    }

    dec Player& player = @Player;

    entrypoint<load> void init() {
        set player->health = 20i;
    }

    entrypoint<tick> void onTick() {
        if (player->health < 10i) {
            heal(player);
        }
    }

    function void heal(Player& p) {
        set p->health = 20i;
    }
}
```
