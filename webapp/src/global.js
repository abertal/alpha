import BootstrapAlpha from './bootstrapAlpha.js'

$(document).ready(() => {
  BootstrapAlpha.langToogle($)
  BootstrapAlpha.logoSize($)

  $(window).resize(function () {
    BootstrapAlpha.logoSize()
  })
})
