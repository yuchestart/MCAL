MCAL Symbol Declaration
====

**Version 0.3.0**
Author: Che Yu
Date: 2025-03-11

# Overview

MCAL Symbol Declarations are a subset of MCAL specifically for connecting external code for MCAL.

MCAL Symbol Declaration files end with `.msd`.

This following code snippet covers most of the specification:
```msd
namespace awesomelibrary;

extern module api{
    import someDependency::submodule;
    export import math::*;
    export import entity::Entity;

    export void apifunction(int a, int b);
}

module math{
    export int add(int a, int b);
    export int subtract(int a, int b);
}

module entity{
    export class Entity{
        public int a;
        public int b;
        static protected void c();
    }
}
```

# Basic Syntax

