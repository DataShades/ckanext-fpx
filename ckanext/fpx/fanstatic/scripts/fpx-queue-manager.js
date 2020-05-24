ckan.module("fpx-queue-manager", function($) {
  "use strict";
  ckan.TOPICS = ckan.TOPICS || {};
  ckan.TOPICS.FPX_ORDER_TICKET = "fpx:ticket:order";
  ckan.TOPICS.FPX_TICKET_CREATED = "fpx:ticket:created";
  ckan.TOPICS.FPX_TICKET_AVAILABLE = "fpx:ticket:available";
  ckan.TOPICS.FPX_POSITION_UPDATED = "fpx:ticket:position-updated";

  return {
    options: {
      serviceUrl: null
    },
    initialize: function() {
      this._onOrder = this._onOrder.bind(this);
      this._onTicket = this._onTicket.bind(this);
      this._onAvailable = this._onAvailable.bind(this);
      this._ticketOrdered = this._ticketOrdered.bind(this);

      this.sandbox.subscribe(ckan.TOPICS.FPX_ORDER_TICKET, this._onOrder);
      this.sandbox.subscribe(ckan.TOPICS.FPX_TICKET_CREATED, this._onTicket);
      this.sandbox.subscribe(
        ckan.TOPICS.FPX_TICKET_AVAILABLE,
        this._onAvailable
      );
    },
    teardown: function() {
      this.sandbox.unsubscribe(
        ckan.TOPICS.FPX_TICKET_AVAILABLE,
        this._onAvailable
      );
      this.sandbox.unsubscribe(ckan.TOPICS.FPX_TICKET_CREATED, this._onTicket);
      this.sandbox.unsubscribe(ckan.TOPICS.FPX_ORDER_TICKET, this._onOrder);
    },

    _onOrder: function(type, items) {
      this.sandbox.client.call(
        "POST",
        "fpx_order_ticket",
        { type: type, items: items },
        this._ticketOrdered,
        console.error
      );
    },
    _onTicket: function(data) {
      var ws = new WebSocket(
        this.options.serviceUrl.replace(/^http/, "ws") +
          "/ticket/" +
          data.id +
          "/wait"
      );
      function onMessage(e) {
        var msg = JSON.parse(e.data);
        if (msg.available) {
          this.sandbox.publish(
            ckan.TOPICS.FPX_TICKET_AVAILABLE,
            data.download_url
          );
        } else {
          this.sandbox.publish(ckan.TOPICS.FPX_POSITION_UPDATED, msg.position);
        }
      }
      ws.addEventListener("message", onMessage.bind(this));
    },
    _onAvailable: function(url) {
      window.location.href = url;
    },

    _ticketOrdered: function(data) {
      this.sandbox.publish(ckan.TOPICS.FPX_TICKET_CREATED, data.result);
    }
  };
});
