# python-documenter: documentation made simple
"*Everyone wants to be data a scientist, but nobody wants to write no documentation*"  
— Ronnie Coleman, probably  

## What is the purpose?
This package is not meant to replace docstrings and code comments, or even to generate those.  
In the author's opinion, those are usually best written by humans, and as little as possible.  
Its easy to hand that off to an LLM, and get a large pile of what the code does—but explaining *why* is far more important than *what*.
The programmer is usually the only agent with the context to explain why some code exists.

Instead, this is to be used to view code at a higher level.  
English summaries of code groups (functions, for now); trace program execution to create a control flow graph,
and more to come.
These are generally useful artifacts, and are also very hard to manually keep updated.  
Running this package in a pipeline solve that.


## Features
- Trace the execution of a program, and record the function calls
- LLM-driven explanation of functions (bring your own LLM)
