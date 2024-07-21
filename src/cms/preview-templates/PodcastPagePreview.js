import React from 'react'
import PropTypes from 'prop-types'
import { PodcastPageTemplate } from '../../templates/podcast-page'

const PodcastPageTemplate = ({ entry, widgetFor }) => (
  <PodcastPageTemplate
    title={entry.getIn(['data', 'title'])}
    content={widgetFor('body')}
  />
)

PodcastPagePreview.propTypes = {
  entry: PropTypes.shape({
    getIn: PropTypes.func,
  }),
  widgetFor: PropTypes.func,
}

export default PodcastPagePreview
