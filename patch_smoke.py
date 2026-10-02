import re

with open('tests/test_smoke.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('session.vm.call_action_by_name("inc")', 'session.trigger_event(get_button_id(tree), "onClick", {})')

with open('tests/test_smoke.py', 'w', encoding='utf-8') as f:
    f.write(text)
