# Why AAYU?

Programming languages shouldn't feel like speaking to a machine. They should feel like giving instructions to an assistant. 

AAYU was built with one simple philosophy: **Code should be read like a story.**

## The Problem

Most modern web frameworks require you to understand:
1. Complex syntax and boilerplate (e.g., `async/await`, `Promises`, `Interfaces`)
2. Context switching between backend languages (Python/Node) and frontend logic.
3. Obscure routing mechanisms and hidden state.

## The AAYU Solution

AAYU completely removes these barriers:

### 1. Human Readable Syntax
Instead of writing `function calculateTax(amount) { return amount * 0.2; }`, you write:
```aayu
task calculate_tax with amount.
    return amount * 0.2.
end.
```
It feels natural. It reads top-to-bottom.

### 2. Built-in Web Runtime
AAYU is not just a language; it is an **Application Platform**.
You don't need to install Express, Flask, or Django.
```aayu
serve on 8080.

get "/hello" to handler.
    render text "Hello World!".
end.
```

### 3. AI Agent Friendly
Because AAYU's syntax maps so closely to natural English intent, **AI Agents (like Claude, GPT, and Gemini) are exceptionally good at writing AAYU code.** 

When you prompt an AI to "write a loop that adds numbers", AAYU's syntax is often closer to the prompt itself than Python or JavaScript. 

[Learn how to build AAYU apps with AI Agents &rarr;](/guide/ai-agents)
