MCAL Specification
==================

**Version:** 0.4

**Targets:** JE 1.21.5+

# Overview

MCAL stands for **M**inecraft **C**ommand **A**bstraction **L**anguage. It is a DSL designed specifically to abstract Minecraft commands. The reason this exists is because I don't like JVM languages and want to write datapacks for Minecraft without breaking my brain.

## Why this isn't in Bedrock
1. You have JavaScript already.
2. MCAL internally relies on the `/data` command, and other features like `storage` are tailored heavily towards JE.
3. Bedrock behavior packs are easy enough to create.

# Architecture

At it's core, MCAL compiles to `.mcfunction` files. This is why keywords like `extern` and `entrypoint` exist.