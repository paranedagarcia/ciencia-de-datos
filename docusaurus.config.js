// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';
// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Ciencia de Datos',
  tagline: 'Fundamentos de Ciencia de Datos, de análisis a producción',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://patricioaraneda.cl',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/ciencia-de-datos/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'patricioaraneda', // Usually your GitHub org/user name.
  projectName: 'ciencia-de-datos', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'es',
    locales: ['es'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          rehypePlugins: [rehypeKatex],
          remarkPlugins: [remarkMath],
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/ODC-isotipo.svg',
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Ciencia de Datos',
        logo: {
          alt: 'Ciencia de Datos Logo',
          src: 'img/ODC-isotipo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Al Curso',
          },
          
          {
            href: 'https://github.com/paranedagarcia/ciencia-de-datos',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Otros cursos de la serie',
            items: [
              {
                label: 'Programación en Python',
                href: 'https://patricioaraneda.cl/python/',
              },
              {
                label: 'Bioestadística',
                href: 'https://patricioaraneda.cl/bioestadistica/',
              },
              {
                label: 'Ciencia de Datos',
                href: 'https://patricioaraneda.cl/ciencia-de-datos/',
              },
              {
                label: 'Análisis con SQL',
                href: 'https://patricioaraneda.cl/sql/',
              },
              {
                label: 'Inteligencia Artificial',
                href: 'https://patricioaraneda.cl/inteligencia-artificial/',
              },
            ],
          },
          {
            title: 'Conecta',
             items: [
              {
                label: 'Website',
                href: 'https://patricioaraneda.cl',
              },
              {
                label: 'Linkedin',
                href: 'https://www.linkedin.com/in/patricioaraneda',
              },
              {
                label: 'Whatsapp',
                href: 'https://wa.me/56978872845',
              },
              
            ],
          },
          {
            title: 'Más',
            items: [
              
              {
                label: 'GitHub',
                href: 'https://github.com/paranedagarcia/ciencia-de-datos',
              },
              {
                label: 'ORCID',
                href: 'https://orcid.org/0000-0001-9677-5959',
              },
              {
                label: 'Correo',
                href: 'mailto:paraneda@ug.uchile.cl',
              }
            ],
          },

        ],
        copyright: `Copyright © ${new Date().getFullYear()} Ciencia de Datos, Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['r', 'python', 'javascript', 'bash', 'sql']
      },
    }),
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
      integrity:
        'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
      crossorigin: 'anonymous',
    },
  ],
};

export default config;
