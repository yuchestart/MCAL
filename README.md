# MCAL : Minecraft Command Abstraction Layer

## Introduction
MCAL exists to make sure your brain doesn't break when you code complex behavior.

## Project Structure
MCAL requires a runtime, which the source code is found in the `datapack` folder.

MCAL's compiler's source code is located within the `compiler` folder. The CLI is not finished yet, however it will be run from the `mclc.py` script.

VSCode doesn't support MCAL natively, so an extension to provide syntax highlighting for VSCode is available under the folder `vscode_extension`

Test MCAL scripts are located under the `tests` folder.

Documentation such as the language specification are located under the `doc` folder.

## FAQ
Why use this? If you need to create complicated datapacks, e.g. for maps or servers, then you can use high-level abstractions to do so.

Is this available on Bedrock? No. MCAL relies too heavily on the `/data` command and JE function macros. If you want high-level abstractions on Bedrock, JS is available.

What versions does it target? JE 1.21.5 or later.

What do I need to run this? You need Python to compile your programs.

## Licensing
MCAL is licensed under MIT. Read more about it [here](LICENSE)
