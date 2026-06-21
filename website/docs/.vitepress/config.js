import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "AAYU",
  description: "The Intent Operating System",
  themeConfig: {
    logo: '/logo.png',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Install', link: '/guide/installation' },
      { text: 'Documentation', link: '/guide/syntax' },
      { text: 'Intent Engine', link: '/platform/intent-engine' },
      { text: 'Examples', link: '/examples/' }
    ],
    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Installation', link: '/guide/installation' },
          { text: 'Downloads', link: '/guide/downloads' }
        ]
      },
      {
        text: 'Language Guide',
        items: [
          { text: 'Syntax Basics', link: '/guide/syntax' }
        ]
      },
      {
        text: 'Framework',
        items: [
          { text: 'Web Development', link: '/web/' },
          { text: 'Database', link: '/web/database' },
          { text: 'Relations', link: '/web/relations' },
          { text: 'RBAC', link: '/web/rbac' },
          { text: 'Workflow', link: '/web/workflow' },
          { text: 'UI DSL', link: '/web/ui-dsl' }
        ]
      },
      {
        text: 'Platform',
        items: [
          { text: 'Intent Engine', link: '/platform/intent-engine' }
        ]
      },
      {
        text: 'Examples',
        items: [
          { text: 'Showcase', link: '/examples/' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Minato95-ayu/INTENT-TO-SILICON' }
    ]
  }
})
