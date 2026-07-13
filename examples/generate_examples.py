import os
import subprocess
import shutil

examples_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\examples"
os.makedirs(examples_dir, exist_ok=True)

apps = {
    "01_hello_world": """app hello_world

page Home
    title "Hello World"
    text "Welcome to AAYU! Your first app is running successfully."
end

run
""",
    "02_counter": """app counter

state count = 0

action increment()
    count = count + 1
end

action decrement()
    count = count - 1
end

page Home
    title "Counter Demo"
    
    container
        text "Current Count:"
        text count
    end
    
    row
        button "Decrease" onClick="decrement"
        button "Increase" onClick="increment"
    end
end

run
""",
    "03_login": """app login

state username = ""
state password = ""
state message = ""

action handleLogin()
    message = "Logging in..."
end

page Login
    title "Login to AAYU"
    
    card
        text "Sign In"
        input "Username" bind="username"
        input "Password" bind="password"
        
        button "Login" onClick="handleLogin"
        
        text message
    end
end

run
""",
    "04_todo": """app todo

state new_task = ""
state task_count = 0

action addTask()
    task_count = task_count + 1
end

page Todo
    title "AAYU Todo List"
    
    row
        input "Enter a new task..." bind="new_task"
        button "Add" onClick="addTask"
    end
    
    container
        text "Tasks remaining:"
        text task_count
    end
end

run
""",
    "05_calculator": """app calculator

state display = "0"

action press_1()
    display = "1"
end

action press_clear()
    display = "0"
end

page Calculator
    title "Calculator"
    
    container
        text display
    end
    
    row
        button "1" onClick="press_1"
        button "C" onClick="press_clear"
    end
end

run
""",
    "06_dashboard": """app dashboard

state active_tab = "Overview"

page Dashboard
    title "Analytics Dashboard"
    
    row
        column
            button "Overview"
            button "Reports"
            button "Settings"
        end
        
        column
            text "Dashboard Content"
            card
                text "Total Users"
                text "1,024"
            end
        end
    end
end

run
""",
    "07_notes": """app notes

page Notes
    title "My Notes"
    
    row
        column
            text "Recent Notes"
            button "Meeting Notes"
            button "Ideas"
        end
        
        column
            text "Note Editor"
            input "Type your note here..."
            button "Save Note"
        end
    end
end

run
""",
    "08_chat_ui": """app chat_ui

state message = ""

action send()
    message = ""
end

page Chat
    title "Team Chat"
    
    container
        text "Alice: Hello everyone!"
        text "Bob: Hey Alice!"
    end
    
    row
        input "Type a message..." bind="message"
        button "Send" onClick="send"
    end
end

run
""",
    "09_weather_ui": """app weather_ui

page Weather
    title "Weather Forecast"
    
    card
        text "San Francisco"
        text "72°F"
        text "Sunny"
    end
    
    row
        card
            text "Mon"
            text "70°F"
        end
        card
            text "Tue"
            text "74°F"
        end
    end
end

run
""",
    "10_whatsapp_clone": """app whatsapp_clone

state current_chat = "Alice"
state draft = ""

page App
    row
        # Sidebar
        column
            title "Chats"
            button "Alice"
            button "Bob"
            button "Charlie"
        end
        
        # Chat View
        column
            title current_chat
            
            container
                text "No messages yet."
            end
            
            row
                input "Type a message" bind="draft"
                button "Send"
            end
        end
    end
end

run
"""
}

# Change to examples directory
os.chdir(examples_dir)

# Create each app
for name, code in apps.items():
    print(f"Generating {name}...")
    # Use aayu CLI to init project
    subprocess.run(["aayu", "new", name], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Overwrite main.aayu
    main_file = os.path.join(name, "main.aayu")
    with open(main_file, "w", encoding="utf-8") as f:
        f.write(code)

print("All 10 examples generated successfully!")
