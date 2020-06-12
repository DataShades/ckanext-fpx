ckan.module("fpx-position-tracker-toast", function ($) {
  "use strict";

  return {
    options: {},
    initialize: function () {
      this._hideToast = this._hideToast.bind(this);
      this._positionUpdated = this._positionUpdated.bind(this);

      this.sandbox.subscribe(ckan.TOPICS.FPX_TICKET_AVAILABLE, this._hideToast);
      this.sandbox.subscribe(ckan.TOPICS.FPX_CANCEL_DOWNLOAD, this._hideToast);
      this.sandbox.subscribe(
        ckan.TOPICS.FPX_POSITION_UPDATED,
        this._positionUpdated
      );
    },
    teardown: function () {
      this.sandbox.unsubscribe(
        ckan.TOPICS.FPX_TICKET_AVAILABLE,
        this._hideToast
      );
      this.sandbox.unsubscribe(
        ckan.TOPICS.FPX_CANCEL_DOWNLOAD,
        this._hideToast
      );
      this.sandbox.unsubscribe(
        ckan.TOPICS.FPX_POSITION_UPDATED,
        this._positionUpdated
      );
    },
    _hideToast: function () {
      this.el.removeClass("visible");
    },
    _positionUpdated: function (position) {
      this.el.addClass("visible");
      // position passed as zero-based value
      this.$(".position").text(+position + 1);
    },
  };
});
