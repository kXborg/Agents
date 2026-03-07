# Building Agent from Scratch
## Core Design Principles
 - Tools are self-contained
 - Registry collects tools
 - Agent orchestrates reasoning ( decides when to run them )
 - LLM client is independent
 - Tools return dictionaries ( Perform the work )
 - Tool schemas contain tool name
 - Registry uses dictionary lookup

Flow: `1` >> `2` >> `3` >> `4` below

## 1. Tool Module
The tool module design now follows the pattern.

 - schema >> description for LLM
 - function >> executable logic
 - TOOL object >> bundle for registry

`The Registry must collect tools and build two structures: tool_schemas and tool_functions`

Note: `Tool name` != `function name`

## 2. Tool Registry
The registry collects tools, exposes schemas, and exposes function map. In short, registry must:
 - Import all tools
 - Collect schemas
 - Build execution map `[name <<-->> functions]`

 Conceptually, 
 - `tool_schemas` = [ ]
 - `tool_functions` = { }

## 3. Agent Script
 - Calls tools
 - Manages States ( conversation history etc.)

## 4. LLM client
Calls the model