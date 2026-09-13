<div align="center">
  <h1>AAYU Programming Language</h1>
  <p><b>Intent To Silicon: One Language to Rule the Full-Stack.</b></p>
  <p>
    <a href="https://intent-to-silicon.vercel.app/">Official Website</a> &bull;
    <a href="https://intent-to-silicon.vercel.app/docs">Documentation</a> &bull;
    <a href="https://intent-to-silicon.vercel.app/learn">Learn in 15 Min</a> &bull;
    <a href="https://intent-to-silicon.vercel.app/examples">Examples</a>
  </p>
</div>

---

AAYU is a revolutionary, AI-native software engineering platform and programming language. It is designed to let **Students, Developers, Engineers, and Tech Companies** focus entirely on building projects without the friction of learning multiple languages.

With AAYU, you can build **everything** in one file, using **100% pure AAYU code**.
- **No HTML**
- **No CSS**
- **No JavaScript**
- **No Python/C++ boilerplate**

The AAYU compiler automatically handles your Backend Server, Database Models, Frontend UI/UX, and Styling.

## Why AAYU is Perfect for Companies and Students

- **All-In-One Full-Stack**: Define your database schema (`model`), backend endpoints (`route`), and frontend UI (`Page`) in the same file seamlessly.
- **Zero Boilerplate: AAYU applications minimize framework boilerplate. The compiler/runtime manages its own state and dependencies.
- **Colorful Native UI/UX**: Style your UI directly via widget properties (`backgroundColor`, `shadow`, `borderRadius`) without writing a single line of CSS.
- **Built-in State**: State management is a first-class citizen. No hooks, stores, or providers needed.

---

## The Power of AAYU (AAYUGram Example)

Want to see what AAYU can do? Here is a mini Instagram clone built entirely in AAYU. It features a Database Model, Backend Route, Actions, and a beautifully styled UI—all in under 50 lines of code!

```aayu
app AAYUGram

# 1. Database Model
model Post {
    username: String
    content: String
    likes: Int
}

# 2. State variables
state appName = "AAYUGram"

# 3. Backend API Route
route "/api/feed"
    get
        return "{'status': 'success', 'posts': []}"
    end
end

# 4. Logic / Actions
action createPost
    print("New Post Created!")
end

# 5. Colorful UI / UX (100% Pure AAYU, NO CSS/HTML)
Page Home
    # Navbar
    Row backgroundColor="#FFFFFF" padding="15px" shadow="true"
        Heading appName color="#E1306C"
    end
    
    # Main Feed Container
    Column padding="20px"
        Form id="newPost" backgroundColor="#FFFFFF" padding="20px" borderRadius="10px" shadow="true" margin="10px"
            Heading "Create Post" color="#262626"
            Input placeholder="What's on your mind?" name="content"
            Button "Share to AAYUGram" onClick="createPost" backgroundColor="#0095F6" color="#FFFFFF" borderRadius="5px"
        end
    end
end
```

To run this:
```bash
python -m tools.cli run aayugram.aayu --web
```
Then visit `http://localhost:3000` to see your fully colorful, full-stack app in action!

---

## Quick Start

### 1. Installation

Install AAYU globally:

```bash
Download AayuInstaller.exe from the official website (or build from source with `pip install -e .`)
```

Verify the installation:

```bash
aayu --version
aayu doctor
```

### 2. Create Your First Project

```bash
aayu new my_project
cd my_project
aayu run
```

---

## For Developers & Companies

AAYU enables companies to prototype rapidly and scale easily. It gives students an intuitive way to understand the full lifecycle of software development—from database to DOM—without getting bogged down by 10 different frameworks. 

Visit [**Intent To Silicon**](https://intent-to-silicon.vercel.app/) to join the movement, download the compiler, and start building the future of software today!

## License

AAYU is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

