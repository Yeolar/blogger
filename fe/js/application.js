/* global */

+function ($) {
  'use strict';

  $(function () {

    // Scrollspy
    var $window = $(window)
    var $body   = $(document.body)

    $body.scrollspy({
      target: '.rdd-sidebar',
      offset: 66
    })
    $window.on('load', function () {
      $body.scrollspy('refresh')
    })

    // Kill links
    $('.rdd-doc-container [href=#]').click(function (e) {
      e.preventDefault()
    })

    // Modal relatedTarget demo
    $('#exampleModal').on('show.bs.modal', function (event) {
      var $button = $(event.relatedTarget)      // Button that triggered the modal
      var recipient = $button.data('whatever')  // Extract info from data-* attributes
      // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
      // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
      var $modal = $(this)
      $modal.find('.modal-title').text('New message to ' + recipient)
      $modal.find('.modal-body input').val(recipient)
    })

    // Config ZeroClipboard
    ZeroClipboard.config({
      moviePath: '/static/o/js/ZeroClipboard.swf',
      hoverClass: 'btn-clipboard-hover'
    })

    // Insert copy to clipboard button before .highlight
    $('.highlight').each(function () {
      var btnHtml = '<div class="zero-clipboard"><span class="btn-clipboard">复制</span></div>'
      $(this).before(btnHtml)
    })
    var zeroClipboard = new ZeroClipboard($('.btn-clipboard'))
    var $htmlBridge = $('#global-zeroclipboard-html-bridge')

    // Handlers for ZeroClipboard
    zeroClipboard.on('load', function () {
      $htmlBridge
        .data('placement', 'top')
        .attr('title', '复制到剪贴板')
        .tooltip()


      // Copy to clipboard
      zeroClipboard.on('dataRequested', function (client) {
        var highlight = $(this).parent().nextAll('.highlight').first()
        client.setText(highlight.text())
      })

      // Notify copy success and reset tooltip title
      zeroClipboard.on('complete', function () {
        $htmlBridge
          .attr('title', '已复制')
          .tooltip('fixTitle')
          .tooltip('show')
          .attr('title', '复制到剪贴板')
          .tooltip('fixTitle')
      })
    })

    // Hide copy button when no Flash is found
    // or wrong Flash version is present
    zeroClipboard.on('noflash wrongflash', function () {
      $('.zero-clipboard').remove()
      ZeroClipboard.destroy()
    })

    var scroll = function(hash) {
      var target = document.getElementById(hash.slice(1));
      if (!target) return;
      var targetOffset = $(target).offset().top - 60;
      $('html,body').animate({
        scrollTop: targetOffset
      }, 1)
    }
    $('.rdd-content a[href^=#][href!=#]').click(function(e) {
      scroll(this.hash)
    })
    $('.rdd-sidebar a[href^=#][href!=#]').click(function(e) {
      scroll(this.hash)
    })
    if (location.hash) scroll(location.hash);

    // Popup original text
    $('.rdd-content *[id^="msgkey-"]').each(function() {
      var ids = $(this).attr('id');
      var tip = $('<span></span>').attr('data-tipso', ids).html($(this).html());
      $(this).html(tip);
      $(this).removeAttr('id');
    });
    $('.rdd-content *[data-tipso]').each(function() {
      $(this).tipso({
        width: 0,
        maxWidth: 800,
        tooltipHover: true,
        titleBackground: '#55b555',
        titleContent: '<b>原文：</b>',//<a class="pull-right" href="">改进翻译</a>',
        ajaxContentUrl: '/po/api/id/' + $(this).attr('data-tipso').slice(7) + '/ctext/'
      });
    });
  })

}(jQuery);

