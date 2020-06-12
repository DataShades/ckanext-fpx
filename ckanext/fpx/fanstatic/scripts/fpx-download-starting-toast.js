ckan.module("fpx-download-starting-toast", function ($) {
  "use strict";
  return {
    options: {
      toastLifetime: 3000,
    },
    initialize: function () {
      this._showToast = this._showToast.bind(this);

      this.sandbox.subscribe(ckan.TOPICS.FPX_TICKET_AVAILABLE, this._showToast);
    },
    teardown: function () {
      this.sandbox.unsubscribe(
        ckan.TOPICS.FPX_TICKET_AVAILABLE,
        this._showToast
      );
    },
    _showToast: function () {
      var el = this.el;
      el.addClass("visible");
      setTimeout(function () {
        el.removeClass("visible");
      }, this.options.toastLifetime);
    },
  };
});
