from .session import ChatSession
from .router import IntentRouter
from .graph import QuestionGraph
from .intent import IntentEngine
import os
import sys

# To call real generator, we'll need to import from existing AAYU project generator.
# We'll see how to integrate that based on user's instruction. For now, we mock the real call
# or invoke `generate_project` if available.

def run_chat():
    print("Welcome to AAYU Chat Engine")
    print("----------------------------")
    target = input("What do you want to build?\n> ")
    
    domain = IntentRouter.resolve_domain(target)
    if domain == "unknown":
        print(f"Sorry, I don't know how to build a '{target}' yet. I only know 'hospital' for now.")
        return

    print(f"\nAwesome! Let's build a {domain.capitalize()}.\n")
    
    session = ChatSession("sess_123")
    session.set_domain(domain)
    
    try:
        graph = QuestionGraph(domain)
    except FileNotFoundError:
        print("Domain JSON not found.")
        return
        
    for q in graph.get_questions():
        while True:
            ans = input(q.format_prompt())
            if q.validate_answer(ans):
                parsed = q.parse_answer(ans)
                session.add_answer(q.id, parsed)
                break
            else:
                print("Invalid answer, please try again.")
                
    # Build Intent
    intent = IntentEngine.build_from_answers(domain, session.answers)
    intent.print_preview()
    
    confirm = input("Generate? (Y/N)\n> ")
    if confirm.upper() in ["Y", "YES"]:
        print("\nIntent Locked")
        aayu_code = intent.to_aayu()
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out_dir = os.path.join(base_dir, "generated_project")
        os.makedirs(out_dir, exist_ok=True)
        
        filepath = os.path.join(out_dir, "main.aayu")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(aayu_code)
            
        print(f"Generated: {filepath}")
        
        # Call Builder API
        from builder.pipeline import build
        build(filepath, out_dir)
        
        print("Project Ready")
    else:
        print("Aborted.")
