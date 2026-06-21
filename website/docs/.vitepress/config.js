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
        text: 'Standard Library',
        items: [
          { text: 'Overview', link: '/packages/index' },
          { text: 'aayu-auth', link: '/packages/auth' },
          { text: 'aayu-http', link: '/packages/http' },
          { text: 'aayu-fs', link: '/packages/fs' },
          { text: 'aayu-json', link: '/packages/json' },
          { text: 'aayu-math', link: '/packages/math' },
          { text: 'aayu-datetime', link: '/packages/datetime' },
          { text: 'aayu-crypto', link: '/packages/crypto' }
        ]
      },
      {
        text: 'AI & Data Ecosystem',
        items: [
          { text: 'aayu-gemini', link: '/packages/gemini' },
          { text: 'aayu-ml', link: '/packages/ml' },
          { text: 'aayu-vision', link: '/packages/vision' }
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
