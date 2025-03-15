MCAL (Minecraft Command Abstraction Language)
=====

**Version 0.3.1**
Author: Che Yu
Date: 2025-03-10
Minecraft Version(s): 1.21.4 - 1.21.5

**Overview**

MCAL is designed to hopefully make writing complicated command-heavy datapacks easier. MCAL abstracts away a lot of the internal logic for handling things like variables into a more readable and concise format.

You write your program in MCAL, chuck it into the compiler, and it spits out a shiny `data` folder for you. You can also download compiled datapacks and still use them with [MCAL Symbol Definitions](declaration.md) MCAL.

The file extension for MCAL files is `.mcal`

# Basic Syntax

## Operators
| Operator | Description | Usage |
|-|-|-|
| `=` | Assignment | `[symbol] = [value]` |
| `+=` | Addition Assignment | `[symbol] += [value]` |
| `-=` | Subtraction Assignment | `[symbol] -= [value]`|
| `*=` | Multiplication Assignment | `` |
| `/=` | Division Assignment | `` |
| `%=` | Modulo Assignment | `` |
| `+` | Addition | `` |
| `-` | Subtraction | `` |
| `*` | Multiplication | `` |
| `/` | Division | `` |
| `%` | Modulo | `` |
| `==` | Logical Equality | `` |
| `!=` | Logical  | `` |
| `&&` | | `` |
| `\|\|` | | `` |
| `!` | | `` |
| `&` | | `` |
| `<` | | `` |
| `>` | | `` |
| `<=` | | `` |
| `>=` | | `` |
| `++` | | `` |
| `--` | | `` |

## Toplevel statements

Toplevel statements are statements that are not contained within a function, class or similar but instead contained within the file itself.

Example:
```mcal
module main; //This is a toplevel statement

dec_scoreboard minecraft:carrot_on_a_stick.use carrots; // This is also a toplevel statement

tellraw!(@a "I'm toplevel too!");

//The function definition is a toplevel statement
entrypoint<load> void main(){
    execute!(at @p run summon sheep ~ ~ ~); //This isn't one, however.
}
```

All toplevel statements across all included files are executed before any entrypoint functions are run.
Toplevel statements are executed top to bottom, and in the dependency tree back to front.

# Control Flow

Control flow is essential for many complicated tasks. However, it does happen to be kind of horrible to implement with Minecraft commands, so MCAL takes care of that for you.


## Branching

Sometimes you need to run a portion of code if a condition is satisfied. To do so, use `if`, `elif`, and `else`.

Usage:
```mcal
if([condition]) [code]
elif([condition]) [code]
else [code]
```

Example:
```mcal
int a = random!(value 1..10);
if(a<6){
    tellraw!(@a "a less than 6");
} elif (a > 3){
    tellraw!(@a "a > 3");
} elif (a <= 3){
    tellraw!(@a "a <= 3");
} else {
    tellraw!(@a "a >= 6");
}

if(a % 2 == 0){
    tellraw!(@a "a is even");
} else {
    tellraw!(@a "a is odd");
}
```

## Loops

Loops are used to repeat actions.

### `for`

The first type of loop in MCAL is the for-loop. For loops have iterators which are updated each loop, and a condition for stopping.

Usage:
```mcal
for([declare iterators];[stop condition];[update iterators]) [code]
```

Example:
```mcal

for(int i=0; i<10; i++){
    tellraw!(@a "${i}");
}

```

### `while`

The second type of loop in MCAL is the while-loop. While loops loop until a certain condition is met.

While loops first check the condition, if it's satisfied, run the loop code, and repeat.

Usage:
```mcal
while(condition) [code]
```

Example:
```mcal
tellraw!(@a "Let's go gambling!");
while(random!(value 1..10) != 10){
    tellraw!(@a "Aw dangit.");
}
tellraw!(@a "My bank account is sad now");
```

### `do`

The third type is the do-while loop. Do while loops function similarly to while loops except that the loop code is run before checking the condition.

Usage:
```mcal
do [code] while([condition]);
```

Example:
```mcal
do {
    tellraw!(@a "I will now roll the dice");
} while(random!(value 1..10) != 10)

tellraw!(@a "Finally! I can stop rolling the dice!");
```


### `break` and `continue`

In the case where you need to end a loop prematurely, use the `break` keyword.

Example:

```mcal
for(int i=0; i<10; i++){
    if(random!(value 1..10) == 5)
        break; //Break out of the loop if you roll a 5
    tellraw!(@a "${i}");
}
```

In the case where you need to skip the rest of the loop's code but continue looping, use the `continue` keyword.

Example:

```mcal
for(int i=0; i<10; i++){
    if(i%2 == 0)
        continue; //If the number is even, skip the rest of the code and continue
    tellraw!(@a "${i}");
}
```


## Functions

### Declaration

Functions are declared as follows:
```mcal
[datatype] [name] ([parameters]) { [code] }
entrypoint<[entrypoint]> [datatype] [name] ([parameters]) { [code] }
```

### `return`

To return a value from a function, use the following:

```mcal
return [expression];
```

## Error handling

TODO: write this

### `throw`

### `try`, `catch`, and `finally`

### `assert`
Assertions are a quick way to throw an error. Assertions will pass if the condition defined inside is true, otherwise it will throw an error.

Usage:
```mcal
assert([conditon])
```

Example:
```mcal
//Check if the block at 0 0 0 is a chest
block<minecraft:chest>? chest = new block<minecraft:chest>(0 0 0);

//If it's not a chest, then this will throw an error.
assert(chest != null);
```

# Modules

All code is organized into modules.
A module line is to be included at the beginning of each file.

```mcal
module Example;

//... code goes here
```

## Symbol Sharing
Symbols can be exported and imported between modules.

To export a symbol, place the `export` keyword in front of a symbol definition or name.

```mcal
//This works
export function int add(int a, int b){
    return a + b;
}

function int subtract(int a, int b){
    return a - b;
}

export subtract; //This also works

```

To import a symbol, use the `import` keyword followed by a module or the symbol name

```mcal
import Example; //Imports the whole module
import Example::someSymbol; //Imports a symbol from the module
import Example::*; //Imports all the symbols top-level
```

## The `using` keyword
The `using` keyword is used to reference namespaces without explicitly defining them. The intent of this is to make code more readable.

Usage:
```mcal
using [symbolname];
```

Example:
```mcal
module main;

import SomeRandomModule::SomeOtherRandomModule;

using SomeRandomModule::SomeOtherRandomModule;

entrypoint<load> function void onLoad(){
    //Previously, I would've had to type SomeRandomModule::SomeOtherRandomModule::someFunction
    //With the 'using' keyword, I can just do:
    someFunction();
}


```

## External symbol sharing
If you're developing something like a library, you need to be able to share symbols outside of the current program. To do that, you can mark a symbol or the whole module as `extern`.

```mcal
extern module api; //Mark the whole module as external

//...
```

```mcal
module something;

extern function void importantFunction(){
    //This function is now extern
    //...
}
```

These extern modules can then be used to generate MCAL Symbol Definitions for external re-use(see [MCAL Symbol Definitions](declaration.md) for more info)

To import that module back, simply include the MCAL Symbol Definition file as a regular module and then carry on.

```
import msdnamespace::somesymbol;
```

## Namespaces

TODO: Write this

Namespaces are used for multiple submodules.

Usage:
```
namespace [namespace];
```


# Data and Variables

## Variable Declaration

Variables are declared by placing the data type in front of the name.

```mcal
int myvar; // Declare a variable
int health = 20i; // Variables can be declared with starting values
int inta, intb=30, intc; // Variables can also be declared in chains.
```

## Datatypes

### Primitives

Here are the primitive data types:
| Type Name | Example |
| --------- | ------- |
| `int` | `5i` |
| `float` | `3.14f` |
| `double` | `3.141592d` |
| `long` | `1000l` |
| `byte` | `3b` | 
| `bool` | `true` |
| `short` | `3s` |
| `string` | `"text"` |
| `uuid` | `2f2a1f62-625f-4b7a-9592-e3166e118cc4` or `[L;555l,555l,555l,555l]` |

Primitive data types have no callable methods.

### Numbers

> **COMPATIBILITY WARNING** <br>
> Signed and unsigned integers are only supported when targeting Java Edition 1.21.5<br>
> Reason:<br>
> Made possible by [25w09a](https://www.minecraft.net/en-us/article/minecraft-snapshot-25w09a)/SNBT Changes/Number Format -
> _Integer type suffixes (`b` or `B` - byte, `s` or `S` - short, `i` or `I` - integer, `l` or `L`) can now be prefixed with `s`(signed) or `u` unsigned_

Integers `int`, `byte`, `long` and `short` can have signed and unsigned variants.

When using a literal or declaring a variable, by default the signed variants are used. However, you can explicitly declare them with `signed` and `unsigned`.

For literals, to declare them signed or unsigned, place `u`(unsigned) or `s`(signed) before the type suffix.

Example:

```mcal
unsigned int myUint = 4294967295; // Unsigned ints can go up to here, but they can only be positive
signed int myInt = -2147483647; // Signed ints can go both ways, but for half the distance.
int x = 3; // If you omit, the marker, signed variants are used by default.

someFunction(8ub); // To pass specifically an unsigned byte, place the -ub suffix.
```

### Strings
Strings are a sequence of characters, similar to an array. Strings are represented by the `string` keyword.
The difference between strings and arrays are that strings can only store characters and are immutable.

To declare a string as a value, use a pair of either `'` or `"` with the contents in between.

```mcal
string mystring = "cheese"; //Double quotes
string mystring2 = 'i hate string cheese'; //Single quotes

someMethod("I'm a string"); //As a value
```

Like arrays, strings have no callable methods.

### Arrays

To represent an array, you use the `[]` suffix.

```mcal
int[] intarr; //Create an array of ints

long[] longarr = [1l,2l,3l]; //Initialize an array of longs
```

Arrays can be subscripted to access and write to elements.

```
int[] somearr = [1,2,3];

tellraw!(@a "${somearr[0]}"); //1

somearr[0] = 3; //Subscripting an array

tellraw!(@a "${somearr[0]}"); //3
```

To manipulate arrays, you can use the methods `push([value])`, `pop([index])`, `insert([value],[index])`, `slice([start],[end])`, and `splice([start],[end]])`.

Example:
```mcal
int[] arr = [1,2,3,4,5,6];

arr.push(7); //arr: [1,2,3,4,5,6,7]

arr.pop(0); //arr: [2,3,4,5,6,7]

arr.insert(8,0); //arr: [8,2,3,4,5,6,7]

int[] newarr = arr.slice(3,6);
//newarr: [4,5,6]
//arr: [8,2,3,4,5,6,7]

newarr = arr.splice(1,6);
//newarry: [8,2,3,4,5,6]
//arr: [7]
```

To delete elements, use the `delete` keyword.
```mcal
delete [array][ [index] ]
```

Example:
```mcal
int[] arr = [1,2,3,4,5];

delete arr[2]; //arr: [1,2,4,5]
```

### Functions

Functions are also a datatype. To represent a function, use this syntax:

`function<[returntype]>([parameters])`

Here are a few examples:

```
void someFunctionDefinedElsewhere(int a, int b){
    tellraw!(@a "${a + b}");
}

//...

function<void>(int,int) mycallback = someFunctionDefinedElsewhere;

mycallback(1i,2i); // 3
```

This datatype is meant for callbacks and events.

This datatype can be called itself, but it doesn't have any callable methods of it's own.

### Compounds
Compounds are essentially NBT Objects. They have no callable methods. They can be subscripted by `[]` or `.`.

Compounds can hold any data type, so long as it's encapsulated in an NBT object.

```
compound mycompound = {
    "key":"value",
    "array":[1,2,3,4],
    "nested"{
        "objects":["are","very","nice"]
    }
};
```

To delete a key from a compound, use the `delete` keyword.

Usage:
```mcal
delete [compoundkey]
```

Example:
```
compound mycompound = {
    "key":"value",
    "array":[1,2,3,4],
    "nested"{
        "objects":["are","very","nice"]
    }
};

delete mycompound.key;
delete mycompound.array[3];
delete mycompound["nested"].objects[1];
```

## Behavior

### References

Primitives and strings are always passed by value.

Arrays, compounds, and classes are always passed by reference.

To copy an array, compound, or class, prefix the identifier of such object with the `copy` keyword.

```mcal
int[] a = [1,2,3];
int[] b = a;

b[0] = 3; //a:[3,2,3] b:[3,2,3]

int[] c = copy a;

c[0] = 7; //a:[3,2,3] b:[3,2,3] c:[7,2,3]
```

In the case that you want to pass a primitive variable by reference, use the `&` suffix.

Example:
```mcal
void complexCalculation(int& var1, int& var2){
    var1 += 3;
    var2 += 4;
}

entrypoint<load> void main(){
    int a = 0;
    int b = 1;
    complexCalculation(a,b);
    tellraw!(@a "${a} ${b}"); //3 5
}
```

### Casting

Similar data types can be casted with `as`.

```mcal
[identifier] as [datatype]
```

Example:

```mcal
int myint = 5;
float myfloat = myint as float;
```

### Null values and safety
> **COMPATIBILITY WARNING**<br>
> These features are only supported when targeting Minecraft 1.21.5<br>
> Reason:<br>
> Made possible by 
> [25w09a](https://www.minecraft.net/en-us/article/minecraft-snapshot-25w09a)/NBT Changes - 
> _Any interface with NBT data within the game (SNBT representation, /data) now supports heterogeneous lists, i.e. ones where elements are not of the same type_

To denote a null value, use the `null` keyword.

By default, variables cannot be null. To mark a variable as nullable, use the `?` suffix in a datatype.

If you try to use a nullable value with a non-nullable datatype(e.g. calling a function), then the compiler will throw an error.
Nullable data types can be cast back into their non-nullable counterparts with `as`.

> **WARNING**<br>
> When casting nullable to non-nullable, it **does not throw errors if the value is null**.<br>
> You are to manage null safety in these situations, e.g. checking for null values.

Example:
```mcal
void someFunction(int a){
    tellraw!(@a "a is {a}.");
}

void someFriendlyFunction(int? a){
    if(a == null){
        tellraw!(@a "a is null, aborting...");
        return;
    }
    tellraw!(@a "a is {a}.");
}

int? nullable = 17; // This variable is nullable. It is initialized to `null` by default.

someFriendlyFunction(nullable); // Output: a is 17.
someFunction(nullable); // This would throw a compiler error.
// Do NOT cast to non-nullable types unless you have checked the value first.
someFunction(nullable as int); // Output: a is 17.

nullable = null;

someFriendlyFunction(nullable); // Output: a is null, aborting...
// Here's why you need to practice null safety.
someFunction(nullable as int); // Output: a is [a bunch of random gibberish]
```


## Scoreboard objectives

Scoreboard objectives can be declared and used similarly to variables.

They are declared with the `dec_scoreboard` keyword.

> **WARNING**<br>
> Scoreboard objectives are deleted after the stack is exited.
> If you wish to avoid this, declare them top-level instead.


Usage:
```mcal
dec_scoreboard [criteria] [name];
```
Example:
```mcal
dec_scoreboard minecraft:carrot_on_a_stick.use clicks;
```

# Object-Oriented Programming

## Declaration

### Overview

To create a class, use the following format:
```
class [name]{
    [members]
}
```

A property is declared like a variable, and a method is declared like a function.

Example:
```
class MyClass{
    int property; 
    int property2 = 5; //Default value for a property 
    void myMethod(){
        //...
    }
}
```


When a method is called from an instance, the first parameter will be the class instance it's being called from. However, when it's called from the class itself, there are no parameters provided by default.

Example:
```mcal
class MyClass{
    int awesomeprop=6;
    void myMethod(MyClass self){
        tellraw!(@a ${self.awesomeprop});
    }
}

MyClass myinstance = new MyClass;

myinstance.myMethod(); //Output: 5

MyClass::myMethod(myinstance); //Output: 5
```

To avoid confusion for methods meant to be called from the class directly, the `static` keyword may be used. `static` marks methods and properties to be accessed from the class directly. To access an identifier from a class, you use the `::` operator.

```mcal
class MyClass{
    static int prop;
    static void method(int e){
        //...
    }
}
//...

MyClass::method(MyClass::prop);

```


### Visibility
Sometimes you don't want members to be accessed outside a class. To achieve this, you can use visibility markers. The visibility markers include:
 * `public`: Accessible outside a class
 * `private`: Accessible inside a class
 * `protected`: Accessible inside a class and it's descendants

By default all members are `public`.

To mark a member's visibility, prefix the member's declaration with a visibility marker. If a member is static, the visibility marker comes before the `static` keyword.

Example:
```mcal
class MyClass{
    public void method(){
        //...
        //I can be called outside the MyClass
    }
    private void internalMethod(){
        //...
        //I can only be called within MyClass
    }
    protected void protectedMethod(){
        //...
        //I can be called within MyClass and it's descendants
    }
    //Notice that `static` comes after `public`
    public static void main(string[] args){
        //...
    }
}
```

### The `partial` keyword

If you need to split a class across files, you can use the `partial` keyword.

To make a partial class, just prefix the class definition with `partial` as follows:
```
partial class [name]{
    [members]
}
```

Example:
```
//myclass.mcal
partial class MyClass{
    //...
    public void doStuff(MyClass this){
        //...
        this.importantFeature();
        //...
    }
    //...
}
```

```
//importantfeature.mcal
partial class MyClass{
    private void importantFeature(){
        //...
    }
}
```


## Instances

Class instances behave similarly to `compound`s, except you can use the methods defined in the class.

To create a class instance, the `new` keyword is used.

> _**NOTICE**_<br>
> Any initialization code you may have for classes is not run when the `new` keyword is used.
> If you want to run your initialization code, create a factory function within that class.

```mcal
MyClass myinstance = new MyClass;

myinstance.property = 5; //This works similarly to compounds
myinstance.method(); //This also works

CustomInitClass myinstance2 = CustomInitClass::create(); //Calling a factory function defined on 
```

To deserialize a class to a `compound`, you can cast it to a type with `as`.

```mcal
MyClass instance = new MyClass;

compound deserialized = instance as compound; //Instance is now a compound

someFunction(instance as compound); //Explicit deserialization.

```



## Inheritance and Polymorphism

Classes can inherit eachother via the `extends` keyword. Classes can only extend from one class.

Example:

```mcal
class BaseClass{
    //...
}

class MyClass extends BaseClass{
    //...
}
```

Extending classes can override methods from the original class, but still access them with the `super` keyword.

Example:
```mcal
class BaseClass{
    int prop;
    void method(BaseClass this){
        tellraw!(@a "Base prop: ${this.prop}")
    }
}

class Extending extends BaseClass{
    int prop;
    void method(Extending this){
        super.method(this); //An implicit cast occurs here.
        tellraw!(@a "Extending prop: ${this.prop}");
    }
}

//...

Extending myinstance = new Extending;
myinstance.prop = 56;

/*
Output:
Base prop: 56
Extending prop: 56
*/
myinstance.method();

```

# Minecraft Interop

## Commands

Minecraft commands are essential to any datapack. Without them, it's like drinking dehydrated water.

MCAL must have a way to invoke minecraft commands, or it would be utterly useless.

### Invocation

There are two ways to invoke Minecraft commands.

The first method is single-command invocation, which is used to invoke a single command.

Usage:
```mcal
[command]!([parameters]);
```

Example:
```mcal
tellraw!(@a "Hello world!"); //Notice how the command parameters are space-seperated, unlike functions.
```

If you ever need to invoke a huge block of commands, the second method of command invocation is the command invocation block(not to be confused with command blocks in-game). These blocks can span multiple lines.

Usage:
```mcal
!{
[commands]
}
```

Example:
```mcal
!{

tellraw @a "Command syntax is preserved here"

# Comments look like this inside of command invocation blocks
# This block of code turns snowballs into arrows
# Which by extension turns snow golems into police officers

execute as @e[type=snowball] at @s run summon arrow ~ ~ ~ {Tags:["fired"]}
execute as @e[type=arrow,tag=fired] at @s run data modify entity @s Owner set from entity @e[type=snowball,sort=nearest,limit=1] Owner
execute as @e[type=arrow,tag=fired] at @s run data modify entity @s Motion set from entity @e[type=snowball,sort=nearest,limit=1] Motion
execute as @e[type=snowball] kill @s

}
```

### Interpolation and Substitution

MCAL variables and objects should also be able to interface with commands. That's where the `${}` operator comes in.

With this operator, you can run MCAL expressions within command invocations, and have their return value be inserted into the command.

Usage:
```
${[expression]}
```

Example:
```
tellraw!(@a "1+1 is ${1+1}");

string toeliminate = "zombie";

!{
tellraw @a "Now exterminating all ${toeliminate}. WAHAHAHAHAHA!"
execute as @e[type=${toeliminate}] run say "Please, spare me!"

kill @e[type=${toeliminate}]
}
```

### `execute`
Minecraft provides the versatile `execute` command. You can leverage it's power in MCAL with the `execute` blocks.

Usage:
```
execute<[statements]>{
    [code]
}
```

Example:
```
//Make all the eggs clone themselves 5 times

execute<as @e[type=item,nbt={Item:{id:"minecraft:egg"}}] at @s>{
    for(int i=0; i<5; i++){
        int randomx = random!(value 1..3) - 2;
        int randomz = random!(value 1..3) - 2;
        summon!(item ~${randomx} ~ ~${randomz} {Item:{id:"minecraft:egg"}})
    }
}

```

## Functions

If a function needs to be run from a tag, like `minecraft:load`, the `entrypoint` keyword can be used to specify that.

`entrypoint` can only be used on defined symbols, not anonymous functions.

```mcal
//This will run on minecraft:load
entrypoint<minecraft:load> void main(){
    tellraw!(@a "Hi world!");
}
```

## NBT

### Storage
> **COMPATIBILITY WARNING**<br>
> This feature is only supported when targeting Java Edition 1.21.5 <br>
> Reason:<br>
> This feature utilizes [nullable types](#null-values-and-safety), which are only supported when targeting Java Edition 1.21.5

To access and modify the NBT data of storages without extra overhead, use the `storage` datatype.

TODO: write this

### Entities
> **COMPATIBILITY WARNING**<br>
> This feature is only supported when targeting Java Edition 1.21.5 <br>
> Reason:<br>
> This feature utilizes [nullable types](#null-values-and-safety), which are only supported when targeting Java Edition 1.21.5

To access and modify the NBT data of entities without extra overhead, use the `entity` datatype.

Usage as datatype:
```mcal
entity<[entityid]>
```

When initializing an entity, if the entity behind the uuid does not exist, then it will return null.

Usage for initialization:
```mcal
new entity<[entityid]>([uuid])
```

Example:
```
//Get all the zombies
entity<minecraft:zombie>[] zombies = [];

execute<as @e[type=zombie]>{
    //Return nullable
    entity<minecraft:zombie>? zombie = new entity<minecraft:zombie>(data!(get entity @s UUID));
    zombies.push(
        //Cast to non-nullable for example's sake.
        zombie as entity<minecraft:zombie>
    );
};
```

### Blocks

> **COMPATIBILITY WARNING**<br>
> This feature is only supported when targeting Java Edition 1.21.5 <br>
> Reason:<br>
> This feature utilizes [nullable types](#null-values-and-safety), which are only supported when targeting Java Edition 1.21.5

To access and modify the NBT data of blocks without extra overhead, use the `block` datatype.

Usage as datatype:
```
block<[blockid]>
```

Usage for initialization:
```
new block<[blockid]>([coordinate])
```

If the block at said coordinate is not of the same type, this expression will return `null`.

Example:
```
//Mark it nullable 
block<minecraft:chest>? myChest = block(0 0 0);
```