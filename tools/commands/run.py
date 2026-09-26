# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import sys
import os
import time

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from compiler.errors import CompilerError
from runtime.vm.vm import VirtualMachine
from runtime.vm.config import VMConfig

from runtime.events.queue import EventQueue
from runtime.events.scheduler import FrameScheduler
from runtime.layout.engine import LayoutEngine
from runtime.ui.style_resolver import StyleResolver
from runtime.ui.painter import Painter
from runtime.diff.engine import DiffEngine
from runtime.renderers.console import ConsoleRenderer

def handle(args):
    renderer_type = "desktop"
    backend = "tkinter"
    target = "main.aayu"
    debug = False
    port = 3000
    
    for arg in args:
        if arg == "--console":
            renderer_type = "console"
        elif arg == "--web":
            renderer_type = "web"
        elif arg.startswith("--renderer="):
            renderer_type = arg.split("=")[1]
        elif arg.startswith("--backend="):
            backend = arg.split("=")[1]
        elif arg.startswith("--port="):
            port = int(arg.split("=")[1])
        elif arg == "--debug":
            debug = True
        elif not arg.startswith("-"):
            target = arg

    import urllib.request
    import hashlib
    
    if target.startswith("http://") or target.startswith("https://"):
        url = target
        print(f"[AAYU] Downloading remote source from {url} ...")
        
        # Isolated cache
        cache_dir = os.path.expanduser("~/.aayu/cache/urls")
        os.makedirs(cache_dir, exist_ok=True)
        
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:12]
        filename = url.split("/")[-1]
        if not filename.endswith(".aayu"):
            filename = "main.aayu"
            
        cached_file = os.path.join(cache_dir, f"{url_hash}_{filename}")
        
        try:
            urllib.request.urlretrieve(url, cached_file)
            target = cached_file
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            sys.exit(1)
            
    if not os.path.exists(target):
        print(f"Error: Target file {target} not found.")
        sys.exit(1)
        
    if debug:
        print(f"[AAYU] Running {target} with renderer={renderer_type} backend={backend}...")
    try:
        with open(target, 'r', encoding='utf-8') as f:
            source = f.read()
            
        # Process Assets
        from compiler.assets.manager import AssetManager
        project_dir = os.path.dirname(os.path.abspath(target))
        if not project_dir: project_dir = "."
        asset_manager = AssetManager(project_dir)
        asset_registry = asset_manager.build()
        
        # Compile
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        analyzer = SemanticAnalyzer(asset_registry=asset_registry)
        ir_pipeline = IRPipeline()
        encoder = BytecodeEncoder()
        ir_pipeline.debug = debug
        encoder.debug = debug
        
        
        ast = parser.parse()
        
        # --- MODULE LOADER PASS ---
        from compiler.ast.nodes import ImportNode, ProgramNode
        from compiler.lexer.lexer import Lexer as ModLexer
        from compiler.parser.parser import Parser as ModParser
        
        def load_imports(program_node, base_dir, visited):
            new_statements = []
            for stmt in program_node.statements:
                if isinstance(stmt, ImportNode):
                    if stmt.module.split(".", 1)[0] in {"math", "json", "http", "file", "crypto", "string", "time"}:
                        continue
                    mod_path = stmt.module.replace(".", "/") + ".aayu"
                    full_path = os.path.join(base_dir, mod_path)
                    
                    if full_path not in visited:
                        visited.add(full_path)
                        if os.path.exists(full_path):
                            with open(full_path, "r", encoding="utf-8") as mf:
                                mod_source = mf.read()
                            mod_ast = ModParser(ModLexer(mod_source).tokenize()).parse()
                            mod_ast = load_imports(mod_ast, base_dir, visited)
                            new_statements.extend(mod_ast.statements)
                        else:
                            print(f"Error: Module {stmt.module} not found at {full_path}")
                            sys.exit(1)
                else:
                    new_statements.append(stmt)
            return ProgramNode(line=program_node.line, column=program_node.column, statements=new_statements)
            
        base_directory = os.path.dirname(os.path.abspath(target))
        if not base_directory:
            base_directory = "."
            
        ast = load_imports(ast, base_directory, set([os.path.abspath(target)]))
        # --- END MODULE LOADER ---

        semantic_ast = analyzer.analyze(ast)
        
        # 1. Infer types
        from compiler.semantic.type_inference import TypeInference
        semantic_ast = TypeInference().infer(semantic_ast)
        
        # 2. Check types
        from compiler.semantic.type_checker import TypeChecker
        TypeChecker().check(semantic_ast)
        
        lir = ir_pipeline.to_lir(ir_pipeline.to_mir(ir_pipeline.to_hir(semantic_ast)))
        program = encoder.encode(lir)
        
        # Init VM
        vm = VirtualMachine(VMConfig.development() if debug else VMConfig.production())
        vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)
        vm.execute()
        
        event_queue = EventQueue()
        
        if renderer_type == "console":
            renderer = ConsoleRenderer(event_queue)
        elif renderer_type == "web":
            from runtime.renderers.web_renderer import WebRenderer
            from runtime.session.manager import SessionManager
            session_manager = SessionManager(program)
            renderer = WebRenderer(session_manager, project_dir=project_dir, port=port)
        elif renderer_type == "desktop":
            if backend == "tkinter":
                if "--ui" in args:
                    from runtime.renderers.tkinter_renderer import TkinterRenderer
                    renderer = TkinterRenderer(event_queue)
                else:
                    renderer = None
            else:
                raise ValueError(f"Unknown backend: {backend}")
        else:
            raise ValueError(f"Unknown renderer: {renderer_type}")
            
        if renderer:
            renderer.initialize()
            if hasattr(renderer, 'start'):
                print(f"\n>> Starting AAYU Web Server at http://localhost:{port} ...", flush=True)
                renderer.start()
        
        # Render Pipeline Components
        layout_engine = LayoutEngine(800, 600)
        painter = Painter()
        style_resolver = StyleResolver()
        diff_engine = DiffEngine()
        scheduler = FrameScheduler(fps=60)
        
        import tracemalloc
        tracemalloc.start()
        
        # Performance Tracking
        perf_metrics = {
            "initial_render_time": 0.0,
            "re_render_times": [],
            "frame_count": 0
        }
        
        current_render_tree = None
        
        def render_pass():
            nonlocal current_render_tree
            t_start = time.perf_counter()
            
            # 1. Ask VM to build New RenderTree
            if vm.router.current_route:
                # Push a new isolated scope for the page and pass the route parameters
                instance_id = f"page_{vm.router.current_route.name}"
                if instance_id not in vm.state_scopes_map:
                    vm.state_scopes_map[instance_id] = {"__instance_id__": instance_id}
                
                # Merge route parameters as props
                for k, v in vm.router.current_route.params.items():
                    vm.state_scopes_map[instance_id][k] = v
                    
                vm.state_scopes.append(vm.state_scopes_map[instance_id])
                
                action_name = f"__PAGE_START_{vm.router.current_route.name}"
                if action_name in vm.action_addresses:
                    vm.call_action_by_name(action_name)
                    vm.execute()
                
                vm.state_scopes.pop()
            else:
                if "__PAGE_START__" in vm.action_addresses:
                    vm.call_action_by_name("__PAGE_START__")
                    vm.execute()
                
            new_tree = vm.interpreter.render_tree
            
            # Check for navigation intent generated during rendering
            nav_action = vm.state.get("__nav_action__")
            nav_target = vm.state.get("__nav_target__")
            if nav_action:
                vm.state["__nav_action__"] = None
                vm.state["__nav_target__"] = None
                
                # Convert action params which might be on stack if any? No, they were set into UIRouter.
                # Actually, NAVIGATE already called vm.router.navigate() from interpreter!
                # We don't need to do it here. The router already updated its state and called the new action.
                pass

            # 2. Diff Phase
            changed = diff_engine.diff(current_render_tree, new_tree)
            if not changed:
                return # Skip render if tree is identical
                
            current_render_tree = new_tree
            
            if new_tree.root:
                if renderer_type == "web":
                    # Web Renderer handles its own DOM-based layout and CSS
                    renderer.render(new_tree)
                else:
                    # 3. Style Resolve Phase
                    style_resolver.resolve(new_tree.root)
                    
                    # 4. Layout Phase
                    render_object_tree = layout_engine.calculate_layout(new_tree.root)
                    
                    # 5. Paint Phase
                    display_list = painter.paint(render_object_tree)
                    
                    # 6. Render
                    renderer.render(display_list)
                    renderer.present()
            else:
                if renderer_type == "web":
                    renderer.render(new_tree)
                else:
                    from runtime.ui.display_list import DisplayList
                    renderer.render(DisplayList())
                    renderer.present()
            
            t_end = time.perf_counter()
            perf_metrics["frame_count"] += 1
            render_duration = (t_end - t_start) * 1000 # ms
            
            if perf_metrics["frame_count"] == 1:
                perf_metrics["initial_render_time"] = render_duration
            else:
                perf_metrics["re_render_times"].append(render_duration)

        if not renderer:
            # Headless mode, no UI to render, skip frame loop
            pass
        else:
            # --- First Render Pass ---
            render_pass()

        if renderer_type == "console":
            renderer.shutdown()
            return
        
        # Main Event Loop
        if renderer:
            running = True
            while running:
                try:
                    renderer.process_events()
                except Exception:
                    break
                    
                # Process AAYU events
                while event_queue.has_events():
                    event = event_queue.pop()
                    if hasattr(event, "action_name"):
                        action_name = event.action_name
                        if action_name == "sys_nav_back":
                            vm.router.back()
                        elif "::" in action_name:
                            instance_id, action_name = action_name.split("::")
                            if instance_id in vm.state_scopes_map:
                                vm.state_scopes.append(vm.state_scopes_map[instance_id])
                                vm.call_action_by_name(action_name)
                                vm.execute()
                                vm.state_scopes.pop()
                        else:
                            vm.call_action_by_name(action_name)
                            vm.execute()
                        # Instead of immediate render, request a frame!
                        scheduler.schedule_render()
                    elif hasattr(event, "target_state"):
                        vm.state[event.target_state] = event.value
                        scheduler.schedule_render()
                        
                scheduler.tick(render_pass)
                
            renderer.shutdown()
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        avg_re_render = 0
        if perf_metrics["re_render_times"]:
            avg_re_render = sum(perf_metrics["re_render_times"]) / len(perf_metrics["re_render_times"])
            
        print("\n--- AAYU Performance Metrics ---")
        print(f"Initial Render Time: {perf_metrics['initial_render_time']:.2f} ms")
        print(f"Avg Re-Render Time:  {avg_re_render:.2f} ms")
        print(f"Total Frames Painted: {perf_metrics['frame_count']}")
        print(f"Peak Memory Usage:   {peak / 10**6:.2f} MB")
        print("--------------------------------\n")
        
        print("[AAYU] Execution completed successfully.")
        
    except CompilerError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nRuntime Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
