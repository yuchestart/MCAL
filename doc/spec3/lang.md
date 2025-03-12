MCAL (Minecraft Command Abstraction Language)
=====

**Version 0.3.0**
Author: Che Yu
Date: 2025-03-10

**Overview**

MCAL is designed to hopefully make writing complicated command-heavy datapacks easier. MCAL abstracts away a lot of the internal logic for handling things like variables into a more readable and concise format.

You write your program in MCAL, chuck it into the compiler, and it spits out a shiny `data` folder for you. You can also download compiled datapacks and still use them with [MCAL Symbol Definitions](declaration.md) MCAL.

The file extension for MCAL files is `.mcal`

# 1.0 Basic Syntax

## 1.1 Operators
| Operator | Description | Usage |
|-|-|-|
| `=` | Assignment | `[symbol] = [value]` |
| `+=` | Addition Assignment | `[symbol] += [value]` |
| `-=` | Subtraction Assignment | `[symbol] -= [value]`|

# 2.0 Commands

Minecraft commands are essential to any datapack. Without them, it's like drinking dehydrated water.

MCAL must have a way to invoke minecraft commands, or it would be utterly useless.

## 2.1 Invocation

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

## 2.2 Interpolation and Substitution

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

## 2.3 `execute`
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

# 3.0 Control Flow

Control flow is essential for many complicated tasks. However, it does happen to be kind of horrible to implement with Minecraft commands, so MCAL takes care of that for you.


## 3.1 Branching

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

## 3.2 Loops

Loops are used to repeat actions.

### 3.2.1 `for`

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

### 3.2.2 `while`

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

### 3.2.3 `do`

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


### 3.2.4 `break` and `continue`

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


## 3.3 Functions

### 3.3.1 Declaration

Functions are declared as follows:
```mcal
[datatype] [name] ([parameters]) { [code] }
entrypoint<[entrypoint]> [datatype] [name] ([parameters]) { [code] }
```

### 3.3.2 `return`

To return a value from a function, use the following:

```mcal
return [expression];
```

### 3.3.3 Entrypoints

TODO: write this

```mcal
entrypoint<[type]> [...]
```

## 3.4 Error handling

TODO: write this

### 3.4.1 `throw`

### 3.4.2 `try`, `catch`, and `finally`

# 4.0 Modules

All code is organized into modules.
A module line is to be included at the beginning of each file.

```mcal
module Example;

//... code goes here
```

## 4.1 Symbol Sharing
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

## 4.2 The `using` keyword
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

## 4.3 External symbol sharing
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

# 5.0 Data and Variables

## 5.1 Variable Declaration

Variables are declared by placing the data type in front of the name.

```mcal
int myvar; // Declare a variable
int health = 20i; // Variables can be declared with starting values
int inta, intb=30, intc; // Variables can also be declared in chains.
```

## 5.2 Datatypes

### 5.2.1 Primitives

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


### 5.2.2 Strings
Strings are a sequence of characters, similar to an array. Strings are represented by the `string` keyword.
The difference between strings and arrays are that strings can only store characters and are immutable.

To declare a string as a value, use a pair of either `'` or `"` with the contents in between.

```mcal
string mystring = "cheese"; //Double quotes
string mystring2 = 'i hate string cheese'; //Single quotes

someMethod("I'm a string"); //As a value
```

Like arrays, strings have no callable methods.

### 5.2.3 Arrays

To represent an array, you use the `[]` suffix.

```mcal
int[] intarr; //Create an array of ints

long[] longarr = [1l,2l,3l]; //Initialize an array of longs
```
Arrays have no callable methods.

Arrays can be subscripted as follows:
```
int[] somearr = [1,2,3];

tellraw!(@a "${somearr[0]}"); //1

somearr[0] = 3;

tellraw!(@a "${somearr[0]}"); //3
```

### 5.2.4 Functions

Functions are also a datatype. To represent a function, use this syntax:

`function<[returntype]>([parameters])`

Here are a few examples:

```
function<void>(int,int) mycallback = someFunctionDefinedElsewhere;

mycallback(1i,2i);
```

This datatype is meant for callbacks and events.

This datatype can be called itself, but it doesn't have any callable methods of it's own.

### 5.2.5 Compounds
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

## 5.3 Data type behavior

### 5.3.1 References

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

### 5.3.2 Casting

Similar data types can be casted with `as`.

```mcal
[identifier] as [datatype]
```

Example:

```mcal
int myint = 5;
float myfloat = myint as float;
```


## 5.4 Scoreboard objectives

Scoreboard objectives can be declared and used similarly to variables.

They are declared with the `dec_scoreboard` keyword.

Usage:
```mcal
dec_scoreboard [criteria] [name];
```
Example:
```mcal
dec_scoreboard minecraft:carrot_on_a_stick.use clicks;
```
> _**NOTICE**_<br>
> Scoreboard objectives are deleted after the stack is exited.
> If you wish to avoid this, declare them top-level instead.


# 6.0 Object-Oriented Programming

## 6.1 Declaration

### 6.1.1 Overview

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


### 6.1.2 Visibility
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

### 6.1.3 The `partial` keyword

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


## 6.2 Instances

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



## 6.3 Inheritance and Polymorphism

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
