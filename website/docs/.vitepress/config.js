import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/INTENT-TO-SILICON/',
  title: "AAYU",
  description: "Architecture-First Software Factory",
  head: [
    ['link', { rel: 'icon', type: 'image/png', href: '/INTENT-TO-SILICON/aayu-icon.png' }],
    ['link', { rel: 'apple-touch-icon', href: '/INTENT-TO-SILICON/aayu-icon.png' }]
  ],
  themeConfig: {
    logo: '/aayu-logo.png',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Get Started', link: '/guide/installation' },
      {
        text: 'Products',
        items: [
          { text: 'AAYU Language', link: '/platform/language' },
          { text: 'AAYU Engine', link: '/platform/engine' },
          { text: 'AAYU Studio', link: '/platform/studio' },
          { text: 'AAYU Chat', link: '/platform/chat' },
          { text: 'BrainOS', link: '/platform/brainos' }
        ]
      },
      { text: 'Documentation', link: '/guide/what-is-aayu' },
      { text: 'Roadmap', link: '/platform/roadmap' }
    ],
    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'What is AAYU?', link: '/guide/what-is-aayu' },
          { text: 'Installation', link: '/guide/installation' },
          { text: 'CLI Commands', link: '/guide/cli-commands' }
        ]
      },
      {
        text: 'Products',
        items: [
          { text: 'AAYU Language', link: '/platform/language' },
          { text: 'AAYU Engine', link: '/platform/engine' },
          { text: 'AAYU Studio', link: '/platform/studio' },
          { text: 'AAYU Chat', link: '/platform/chat' },
          { text: 'BrainOS', link: '/platform/brainos' }
        ]
      },
      {
        text: 'Reference',
        items: [
          { text: 'Syntax', link: '/specification/syntax' },
          { text: 'Compiler & Targets', link: '/specification/compiler' },
          { text: 'AAYU IR', link: '/specification/ir' },
          { text: 'Target Engine', link: '/specification/target_engine' }
        ]
      },
      {
        text: 'Roadmap',
        items: [
          { text: 'Development Roadmap', link: '/platform/roadmap' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Minato95-ayu/INTENT-TO-SILICON' }
    ]
  }
})
