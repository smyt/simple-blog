$(document).ready(function () {
    $(".header-btn a").click(function (e) {
        e.preventDefault(), $(".header-menu ul").toggleClass("active")
    });

    // click button for load additional records
    $(".blog-btn").click(function (event) {
        var lastPublished = this.dataset.lastPublished;
        var self = this;
        event.preventDefault();
        $.get("", {
            lastPublished: lastPublished
        }).done(function (r) {
            self.dataset.lastPublished = r.lastPublished;
            if (!r.has_more) {
                $(self).remove();
            }
            $(".blog .container > .posts").append(r.content);
            setTimeout(hljs.initHighlighting, 200);
        })
    });

});
