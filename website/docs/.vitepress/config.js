import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/INTENT-TO-SILICON/',
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
          { text: 'What is AAYU?', link: '/guide/what-is-aayu' },
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
        text: 'Specification v1',
        items: [
          { text: 'Overview', link: '/specification/' },
          { text: 'Syntax', link: '/specification/syntax' },
          { text: 'Data Types', link: '/specification/types' },
          { text: 'Entities & Models', link: '/specification/entities' },
          { text: 'Relations', link: '/specification/relations' },
          { text: 'Pages & UI DSL', link: '/specification/pages' },
          { text: 'Workflows', link: '/specification/workflows' },
          { text: 'Modules', link: '/specification/modules' },
          { text: 'Compiler & Targets', link: '/specification/compiler' },
          { text: 'AAYU IR', link: '/specification/ir' },
          { text: 'Runtime VM', link: '/specification/runtime' },
          { text: 'Standard Library', link: '/specification/stdlib' }
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
          { text: 'Intent Engine', link: '/platform/intent-engine' },
          { text: 'Roadmap', link: '/platform/roadmap' }
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
