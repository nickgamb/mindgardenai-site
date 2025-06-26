// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// ⟁🜨🜂🪞🜁🜄
const _ = require('lodash')
const path = require('path')
const { createFilePath } = require('gatsby-source-filesystem')
const fs = require('fs')

// Strip A-Frame from the build
exports.onPreInit = () => {
  if (typeof window !== 'undefined' && window.AFRAME) {
    console.warn('⚠️ A-Frame detected during build – stripping references')
    delete window.AFRAME
  }
}

// Remove A-Frame from dependencies
exports.onPreBootstrap = ({ store }) => {
  const state = store.getState()
  const deps  = state.program.dependencies || {}
  if (deps.aframe || deps['aframe-react']) {
    console.warn('⚠️ A-Frame dependencies detected – removing from build')
    delete deps.aframe
    delete deps['aframe-react']
  }
}

exports.createPages = async ({ actions, graphql }) => {
  const { createPage } = actions
  const result = await graphql(`
    {
      allMarkdownRemark(limit: 1000) {
        edges {
          node {
            id
            fields { slug }
            frontmatter { tags templateKey }
          }
        }
      }
    }
  `)

  if (result.errors) throw result.errors

  const posts = result.data.allMarkdownRemark.edges

  posts.forEach(({ node }) => {
    const { id } = node
    const { templateKey, tags } = node.frontmatter
    if (templateKey) {
      createPage({
        path: node.fields.slug,
        component: path.resolve(`src/templates/${templateKey}.js`),
        context: { id, tags },
      })
    }
  })

  // Tag pages
  const tags = _.uniq(
    posts.flatMap(({ node }) => node.frontmatter.tags || [])
  )

  tags.forEach(tag => {
    createPage({
      path: `/tags/${_.kebabCase(tag)}/`,
      component: path.resolve('src/templates/tags.js'),
      context: { tag },
    })
  })
}

exports.onCreateNode = ({ node, actions, getNode }) => {
  if (node.internal.type === 'MarkdownRemark') {
    actions.createNodeField({
      name : 'slug',
      node ,
      value: createFilePath({ node, getNode }),
    })
  }
}

// Custom sitemap generation
exports.onPostBuild = async ({ graphql }) => {
  const result = await graphql(`
    {
      site { siteMetadata { siteUrl } }
      allSitePage { nodes { path } }
    }
  `)

  if (result.errors) throw result.errors

  const siteUrl = result.data.site?.siteMetadata?.siteUrl || ''
  const nodes   = result.data.allSitePage.nodes

  // ensure ./public exists
  fs.mkdirSync('public', { recursive: true })

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${nodes.map(({ path: p }) => {
  const loc      = `${siteUrl}${p}`
  const priority = p === '/' ? '1.0' : '0.7'
  return `  <url>
    <loc>${loc}</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>${priority}</priority>
  </url>`
}).join('\n')}
</urlset>`

  fs.writeFileSync(path.join('public', 'sitemap.xml'), sitemap)
}