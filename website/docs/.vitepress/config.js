import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "AAYU",
  description: "Human Readable Programming Language for Web Applications and AI Agents",
  themeConfig: {
    logo: '/logo.png', // Assuming we'll add a logo later
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/why-aayu' },
      { text: 'Examples', link: '/examples/adumate' },
      { text: 'GitHub', link: 'https://github.com/Minato95-ayu/INTENT-TO-SILICON' }
    ],
    sidebar: [
      {
        text: 'Introduction',
        items: [
          { text: 'Why AAYU?', link: '/guide/why-aayu' },
          { text: 'Installation', link: '/guide/installation' },
          { text: 'Getting Started', link: '/guide/hello-world' },
        ]
      },
      {
        text: 'Core Concepts',
        items: [
          { text: 'Variables & Types', link: '/guide/variables' },
          { text: 'Tasks (Functions)', link: '/guide/tasks' },
          { text: 'Control Flow', link: '/guide/control-flow' },
        ]
      },
      {
        text: 'Web & Database',
        items: [
          { text: 'Routing & Views', link: '/guide/routing' },
          { text: 'Database & Entities', link: '/guide/database' },
          { text: 'Authentication', link: '/guide/authentication' },
        ]
      },
      {
        text: 'AI Integration',
        items: [
          { text: 'Building with AI Agents', link: '/guide/ai-agents' },
        ]
      },
      {
        text: 'Examples',
        items: [
          { text: 'Adumate', link: '/examples/adumate' },
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Minato95-ayu/INTENT-TO-SILICON' }
    ],
    search: {
      provider: 'local'
    }
  }
})
