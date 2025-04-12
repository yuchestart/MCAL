MCAL Specification
==================

**Version:** 0.4

**Targets:** JE 1.21.5+

# Overview

MCAL stands for **M**inecraft **C**ommand **A**bstraction **L**anguage. It is a DSL designed specifically to abstract Minecraft commands. The reason this exists is because I don't like JVM languages and want to write datapacks for Minecraft without breaking my brain.

## Why this isn't in Bedrock
1. MCAL internally relies on the `/data` command, and other features like `storage` are tailored heavily towards JE.
2. Bedrock behavior packs are easy enough to create, with JavaScript being a viable programming language.

# Architecture

At it's core, MCAL compiles to `.mcfunction` files. This is why keywords like `extern` and `entrypoint` exist. MCAL is also designed to allow for interface with mods, such as syntax for defining custom commands, entities, blocks, etc.. MCAL supports direct command execution as well, with the `!{}` syntax.

The file extension for an MCAL source file is `.mcal`.

For asthetics, an MCAL source file which is supposed to contain only definitions has the file extension `.d.mcal`. But these files are functionally similar to regular `.mcal` files.

# Syntax

## Language Features

 * [Functions and Variables](./funcandvar.md)
 * [Literals and Operations](./computations.md)
 * [Object-Oriented Programming](./oop.md)
 * [Symbol Sharing](./symbolsharing.md)
 * [Minecraft Interop](./minecraft.md)

## Comments

Comments in MCAL are used to annotate code and prevent code from executing.

Single line comments are prefixed with `//`. Multiline comments start with `/*` and end with `*/`.

Any code after a `//` or in between a `/*` and `*/` will not be executed. However, if said symbols are contained within a string or command execution block, they will not behave as comments.

Example:
```
// This is a single line comment
/*
This is a multiline comment
*/
```

## Statements

Statements, like command calls and variable declarations, are seperated by semicolons (`;`).

Example:
```
tellraw!(@a "Hi world"); // Valid: A semicolon terminates the statement.
int score = 0 // Invalid: there is no semicolon terminating the statement.
```