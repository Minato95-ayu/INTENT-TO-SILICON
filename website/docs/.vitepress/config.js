import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "AAYU",
  description: "Human Readable Programming Language",
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Get Started', link: '/guide/installation' }
    ],
    sidebar: [
      {
        text: 'Get Started',
        items: [
          { text: 'Installation', link: '/guide/installation' },
          { text: 'Language Basics', link: '/guide/basics' }
        ]
      },
      {
        text: 'Web Development',
        items: [
          { text: 'Routing & Views', link: '/web/routing' },
          { text: 'Database Models', link: '/web/database' }
        ]
      },
      {
        text: 'Packages',
        items: [
          { text: 'Overview', link: '/packages/index' },
          { text: 'Auth', link: '/packages/auth' },
          { text: 'HTTP', link: '/packages/http' }
        ]
      },
      {
        text: 'AI & ML',
        items: [
          { text: 'Gemini LLM', link: '/packages/gemini' },
          { text: 'Data Science (ML)', link: '/packages/ml' },
          { text: 'Vision processing', link: '/packages/vision' }
        ]
      },
      {
        text: 'Examples',
        items: [
          { text: 'Todo App', link: '/examples/todo-app' },
          { text: 'LMS System', link: '/examples/lms' }
        ]
      },
      {
        text: 'Showcase',
        items: [
          { text: 'Built with AAYU', link: '/showcase' }
        ]
      }
    ]
  }
})
