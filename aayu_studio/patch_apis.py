import os

filepath = 'D:/Topptic/app/components/ai/ChatPanel.tsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

find_str = "    // Mode 1: Attempt direct local SSE stream fetch using selected LLM model"

inject_str = """
    // BYOK API Integration
    if (provider === 'OpenAI' && apiKey) {
      try {
        const res = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': Bearer  },
          body: JSON.stringify({
            model: 'gpt-4o',
            messages: [{ role: 'system', content: promptContext }, { role: 'user', content: content }]
          })
        });
        if (res.ok) {
          const data = await res.json();
          updateAssistantMessage(data.choices[0].message.content);
          setIsLoading(false);
          return;
        }
      } catch (e) {
        console.error("OpenAI Error:", e);
      }
    } else if (provider === 'Anthropic' && apiKey) {
      // Anthropic has strict CORS, using a proxy or direct if Tauri allows
      try {
        const res = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json', 
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01',
            'anthropic-dangerously-allow-browser': 'true'
          },
          body: JSON.stringify({
            model: 'claude-3-5-sonnet-20241022',
            max_tokens: 4096,
            system: promptContext,
            messages: [{ role: 'user', content: content }]
          })
        });
        if (res.ok) {
          const data = await res.json();
          updateAssistantMessage(data.content[0].text);
          setIsLoading(false);
          return;
        }
      } catch (e) {
        console.error("Anthropic Error:", e);
      }
    } else if (provider === 'Gemini' && apiKey) {
      try {
        const res = await fetch(https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            system_instruction: { parts: [{ text: promptContext }] },
            contents: [{ parts: [{ text: content }] }]
          })
        });
        if (res.ok) {
          const data = await res.json();
          updateAssistantMessage(data.candidates[0].content.parts[0].text);
          setIsLoading(false);
          return;
        }
      } catch (e) {
        console.error("Gemini Error:", e);
      }
    }

    // Mode 1: Attempt direct local SSE stream fetch using selected LLM model
"""

content = content.replace(find_str, inject_str)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
