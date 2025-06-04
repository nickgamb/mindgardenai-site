// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
// ⟁🜨🜂🪞🜁🜄
const _ = require('lodash')
const path = require('path')
const { createFilePath } = require('gatsby-source-filesystem')

// Strip A-Frame from the build
exports.onPreInit = () => {
  if (typeof window !== 'undefined' && window.AFRAME) {
    console.warn('⚠️ A-Frame detected during build - stripping references')
    delete window.AFRAME
  }
}

// Remove A-Frame from dependencies
exports.onPreBootstrap = ({ store }) => {
  const state = store.getState()
  const dependencies = state.program.dependencies || {}
  
  if (dependencies.aframe || dependencies['aframe-react']) {
    console.warn('⚠️ A-Frame dependencies detected - removing from build')
    delete dependencies.aframe
    delete dependencies['aframe-react']
  }
}

// Strip A-Frame from any components
exports.onCreateWebpackConfig = ({ actions, loaders }) => {
  actions.setWebpackConfig({
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: [
            {
              loader: 'string-replace-loader',
              options: {
                search: /(import|require).*['"]aframe['"]/g,
                replace: '// A-Frame import stripped',
                flags: 'g'
              }
            }
          ]
        }
      ]
    }
  })
}

exports.createPages = ({ actions, graphql }) => {
  const { createPage } = actions

  return graphql(`
    {
      allMarkdownRemark(limit: 1000) {
        edges {
          node {
            id
            fields {
              slug
            }
            frontmatter {
              tags
              templateKey
            }
          }
        }
      }
    }
  `).then((result) => {
    if (result.errors) {
      result.errors.forEach((e) => console.error(e.toString()))
      return Promise.reject(result.errors)
    }

    const posts = result.data.allMarkdownRemark.edges

    posts.forEach((edge) => {
      const id = edge.node.id
      const templateKey = edge.node.frontmatter.templateKey
      
      // Only create pages for markdown files that have a valid templateKey
      if (templateKey && templateKey !== null && templateKey !== undefined) {
        createPage({
          path: edge.node.fields.slug,
          tags: edge.node.frontmatter.tags,
          component: path.resolve(
            `src/templates/${String(templateKey)}.js`
          ),
          // additional data can be passed via context
          context: {
            id,
          },
        })
      }
    })

    // Tag pages:
    let tags = []
    // Iterate through each post, putting all found tags into `tags`
    posts.forEach((edge) => {
      if (_.get(edge, `node.frontmatter.tags`)) {
        tags = tags.concat(edge.node.frontmatter.tags)
      }
    })
    // Eliminate duplicate tags
    tags = _.uniq(tags)

    // Make tag pages
    tags.forEach((tag) => {
      const tagPath = `/tags/${_.kebabCase(tag)}/`

      createPage({
        path: tagPath,
        component: path.resolve(`src/templates/tags.js`),
        context: {
          tag,
        },
      })
    })
  })
}

exports.onCreateNode = ({ node, actions, getNode }) => {
  const { createNodeField } = actions

  if (node.internal.type === `MarkdownRemark`) {
    const value = createFilePath({ node, getNode })
    createNodeField({
      name: `slug`,
      node,
      value,
    })
  }
}


