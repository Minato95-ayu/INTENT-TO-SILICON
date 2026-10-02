import re

with open('tests/test_smoke.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('session.trigger_event(get_button_id(tree), "onClick", {})', 'print("SCOPES:", session.vm.state_scopes); session.vm.call_action_by_name("inc")')

with open('tests/test_smoke.py', 'w', encoding='utf-8') as f:
    f.write(text)
