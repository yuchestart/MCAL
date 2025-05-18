Object-Oriented Programming
====
[Go Back](./spec.md)

# Overview

MCAL supports Object-Oriented Programming (OOP) concepts such as classes, structs, inheritance, and polymorphism. These features allow developers to organize code into reusable and modular components.

# Classes

## Definition

Classes are defined using the `class` keyword. They can include fields, methods, and constructors. Access modifiers (`public`, `private`, `protected`) and the `static` keyword are supported.

Example:
```mcal
class MyClass {
    public int field;
    private static string message = "Hello";

    public static void main(string[] args) {
        tellraw!(@a "${message}");
    }

    private int add(int a, int b) {
        return a + b;
    }
}
```

## Polymorphism

Classes can extend other classes or implement multiple interfaces using the `:` syntax. The `using` keyword allows selective inheritance of members from parent classes or interfaces.

Example:
```mcal
class ChildClass : ParentClass, Interface {
    using ParentClass::someMethod;

    public static ChildClass create() {
        return new ChildClass;
    }

    void doSomething() {
        super.ParentClass::someMethod();
    }
}
```

# Structs

Structs are lightweight data containers defined using the `struct` keyword. They can optionally be specialized for Minecraft entities or blocks using `<minecraft:entity>` or `<minecraft:block>`.

Example:
```mcal
struct entity<minecraft:pig> Technoblade {
    bool nerd = false;
    long soulmagic;
}
```

# Instances

Instances of classes and structs can be created using the `new` keyword. By default, these classes are passed by value. References to classes can be created as well. Class instances are destroyed with `delete`. To copy a class instance, use `copy`.

Example:
```mcal
MyClass instance = new MyClass;
MyClass& reference = instance;
MyClass& starter_reference = new MyClass;
Technoblade pig = new Technoblade;

delete instance; //now reference is invalid

Technoblade neverdies = copy pig;

```