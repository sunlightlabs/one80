/// <reference path="jquery-1.2.6-vsdoc.js" />
(function($) {

    $.deparam || ($.deparam = function(qs) {
      var params, pieces;
      params = {};
      if (!qs) {
        return params;
      }
      pieces = qs.split(/[&=]/);
      $.each(pieces, function(idx, val) {
        if (idx % 2) {
          return params[pieces[idx - 1]] = val;
        }
      });
      return params;
    });

    $.fn.annotateImage = function(options) {
        /// <summary>
        ///   Creates annotations on the given image.
        ///   Images are loaded from the "getUrl" propety passed into the options.
        /// </summary>
        var opts = $.extend({}, $.fn.annotateImage.defaults, options);
        var image = this;

        this.image = this;
        this.mode = 'view';

        // Assign defaults
        this.getUrl = opts.getUrl;
        this.saveUrl = opts.saveUrl;
        this.deleteUrl = opts.deleteUrl;
        this.editable = opts.editable;
        this.useAjax = opts.useAjax;
        this.notes = opts.notes;

        // Add the canvas
        this.canvas = $('<div class="image-annotate-canvas">\
                           <div class="image-annotate-view"></div>\
                           <div class="image-annotate-edit"><div class="image-annotate-edit-area"></div></div>\
                         </div>');
        this.canvas.children('.image-annotate-edit').hide();
        this.canvas.children('.image-annotate-view').hide();
        this.image.after(this.canvas);

        // Give the canvas and the container their size and background
        this.canvas.height(this.height());
        this.canvas.width(this.width());
        this.canvas.css('background-image', 'url("' + this.attr('src') + '")');
        this.canvas.children('.image-annotate-view, .image-annotate-edit').height(this.height());
        this.canvas.children('.image-annotate-view, .image-annotate-edit').width(this.width());

        // Add the behavior: hide/show the notes when hovering the picture
        this.canvas.hover(function() {
            if ($(this).children('.image-annotate-edit').css('display') == 'none') {
                $(this).children('.image-annotate-view').stop().show();
            }
        }, function() {
            $(this).children('.image-annotate-view').stop().hide();
        });

        this.canvas.children('.image-annotate-view').hover(function() {
            $(this).stop().show();
        }, function() {
            $(this).stop().hide();
        });

        // load the notes
        if (this.useAjax) {
            $.fn.annotateImage.ajaxLoad(this);
        } else {
            $.fn.annotateImage.load(this);
        }

        // Add the "Add a note" button
        if (this.editable) {
            this.button = $('<a class="image-annotate-add" id="image-annotate-add" href="#">Add Note</a>');
            this.button.click(function(evt) {
                evt.preventDefault();
                var opts = {}
                if($(evt.target).hasClass('image-annotate-view')){
                    opts.left = (evt.layerX || evt.offsetX) - 30;
                    opts.top = (evt.layerY || evt.offsetY) - 30;
                }
                var editable = new $.fn.annotateEdit(image, null, opts);
                $.fn.annotateImage.add(image, editable);
            });
            this.canvas.after(this.button);
        }

        // Hide the original
        this.hide();

        return this;
    };

    /**
    * Plugin Defaults
    **/
    $.fn.annotateImage.defaults = {
        getUrl: 'your-get.rails',
        saveUrl: 'your-save.rails',
        deleteUrl: 'your-delete.rails',
        editable: true,
        useAjax: true,
        notes: new Array()
    };

    $.fn.annotateImage.clear = function(image) {
        /// <summary>
        ///   Clears all existing annotations from the image.
        /// </summary>
        for (var i = 0; i < image.notes.length; i++) {
            image.notes[image.notes[i]].destroy();
        }
        image.notes = new Array();
    };

    $.fn.annotateImage.ajaxLoad = function(image) {
        /// <summary>
        ///   Loads the annotations from the "getUrl" property passed in on the
        ///     options object.
        /// </summary>
        $.getJSON(image.getUrl + ((image.getUrl.match(/\?/)) ? '&' : '?') + 'ticks=' + $.fn.annotateImage.getTicks(), function(data) {
            image.notes = data;
            $.fn.annotateImage.load(image);
        });
    };

    $.fn.annotateImage.load = function(image) {
        /// <summary>
        ///   Loads the annotations from the notes property passed in on the
        ///     options object.
        /// </summary>
        for (var i = 0; i < image.notes.length; i++) {
            image.notes[image.notes[i]] = new $.fn.annotateView(image, image.notes[i]);
        }
    };

    $.fn.annotateImage.getTicks = function() {
        /// <summary>
        ///   Gets a count og the ticks for the current date.
        ///     This is used to ensure that URLs are always unique and not cached by the browser.
        /// </summary>
        var now = new Date();
        return now.getTime();
    };

    $.fn.annotateImage.add = function(image, editable) {
        /// <summary>
        ///   Adds a note to the image.
        /// </summary>
        if (image.mode == 'view') {
            image.mode = 'edit';

            // Create/prepare the editable note elements
            if(!editable){
              var editable = new $.fn.annotateEdit(image);
            }

            $.fn.annotateImage.createSaveButton(editable, image);
            $.fn.annotateImage.createCancelButton(editable, image);
        }
    };

    $.fn.annotateImage.createSaveButton = function(editable, image, note) {
        /// <summary>
        ///   Creates a Save button on the editable note.
        /// </summary>
        var ok = $('<button class="replace" id="image-annotate-edit-ok"><span>OK</span></button>');

        ok.click(function(evt) {
            evt.preventDefault();
            var form = $('#image-annotate-edit-form form');
            $.fn.annotateImage.appendPosition(form, editable);

            image.mode = 'view';

            // Save via AJAX
            if (image.useAjax) {
                $.ajax({
                    url: image.saveUrl,
                    data: form.serialize(),
                    error: function(e) { alert("An error occured saving your note.") },
                    success: function(data) {
                      if (data.id != undefined) {
                        $.extend(editable.note, data);
                        // Add to canvas
                        if (!note) {
                            editable.note.editable = true;
                            note = new $.fn.annotateView(image, editable.note)
                            image.notes.push(editable.note);
                        }

                        note.resetPosition(editable);

                        editable.destroy();
                        image.trigger('mouseenter');
                      }
                    },
                    dataType: "json"
                });
            }
        });
        editable.form.find('form div.clear:last').before(ok);
    };

    $.fn.annotateImage.createCancelButton = function(editable, image) {
        /// <summary>
        ///   Creates a Cancel button on the editable note.
        /// </summary>
        var cancel = $('<button class="replace" id="image-annotate-edit-close"><span>Cancel</span></button>');
        cancel.click(function(evt) {
            evt.preventDefault()
            editable.destroy();
            image.mode = 'view';
        });
        editable.form.find('form div.clear:last').before(cancel);
    };

    $.fn.annotateImage.saveAsHtml = function(image, target) {
        var element = $(target);
        var html = "";
        for (var i = 0; i < image.notes.length; i++) {
            html += $.fn.annotateImage.createHiddenField("first_" + i, image.notes[i].first);
            html += $.fn.annotateImage.createHiddenField("last_" + i, image.notes[i].last);
            html += $.fn.annotateImage.createHiddenField("org_" + i, image.notes[i].org);
            html += $.fn.annotateImage.createHiddenField("title_" + i, image.notes[i].title);
            html += $.fn.annotateImage.createHiddenField("top_" + i, image.notes[i].top);
            html += $.fn.annotateImage.createHiddenField("left_" + i, image.notes[i].left);
            html += $.fn.annotateImage.createHiddenField("height_" + i, image.notes[i].height);
            html += $.fn.annotateImage.createHiddenField("width_" + i, image.notes[i].width);
        }
        element.html(html);
    };

    $.fn.annotateImage.createHiddenField = function(name, value) {
        return '&lt;input type="hidden" name="' + name + '" value="' + value + '" /&gt;<br />';
    };

    $.fn.annotateEdit = function(image, note, opts) {
        /// <summary>
        ///   Defines an editable annotation area.
        /// </summary>
        this.image = image;

        if (note) {
            this.note = note;
        } else {
            var newNote = new Object();
            newNote.id = "new";
            newNote.top = (opts && opts.top) || (this.image.height() - 60) / 2;
            newNote.left = (opts && opts.left) || (this.image.width() - 60) / 2;
            newNote.width = 60;
            newNote.height = 60;
            newNote.first_name = "";
            newNote.last_name = "";
            newNote.organization = "";
            newNote.title = "";
            this.note = newNote;
        }

        // Set area
        var area = image.canvas.children('.image-annotate-edit').children('.image-annotate-edit-area');
        this.area = area;
        this.area.css('height', this.note.height + 'px');
        this.area.css('width', this.note.width + 'px');
        this.area.css('left', this.note.left + 'px');
        this.area.css('top', this.note.top + 'px');

        // Show the edition canvas and hide the view canvas
        image.canvas.children('.image-annotate-view').stop().hide();
        image.canvas.children('.image-annotate-edit').show();

        // Add the note (which we'll load with the form afterwards)
        var form = $('<div id="image-annotate-edit-form">\
                        <form>\
                          <h4 id="image-annotate-edit-form-header">Who is this?</h4>\
                          <ul class="clearfix">\
                          <li><label for="image-annotate-first">First name:</label>\
                            <input type="text" class="required" id="image-annotate-first" placeholder="first name" name="first" value="' + this.note.first_name + '" />\
                          </li>\
                          <li class="last"><label for="image-annotate-last">Last name:</label>\
                            <input type="text" class="required" id="image-annotate-last" placeholder="last name" name="last" value="' + this.note.last_name + '" />\
                          </li>\
                          <li><label for="image-annotate-title">Title:</label>\
                            <input type="text" class="required" id="image-annotate-title" placeholder="title" name="title" value="' + this.note.title + '" />\
                          </li>\
                          <li class="last"><label for="image-annotate-org">Organization:</label>\
                            <input type="text" class="required" id="image-annotate-org" placeholder="organization" name="org" value="' + this.note.organization + '" />\
                          </li>\
                          </ul>\
                          <input type="hidden" class="suggest-hint" value="" />\
                          <div class="clear"></div>\
                        </form>\
                      </div>');
        this.form = form;

        $('body').append(this.form);
        this.form.css('left', this.image.canvas.offset().left + this.note.left - 35);
        this.form.css('top', this.image.canvas.offset().top + this.note.top + this.note.height + 5);

        // Set the area as a draggable/resizable element contained in the image canvas.
        // Would be better to use the containment option for resizable but buggy
        area.resizable({
            handles: 'all',

            stop: function(e, ui) {
                form.css('left', area.offset().left + 'px');
                form.css('top', (parseInt(area.offset().top) + parseInt(area.height()) + 2) + 'px');
            }
        })
        .draggable({
            containment: image.canvas,
            drag: function(e, ui) {
                form.css('left', area.offset().left + 'px');
                form.css('top', (parseInt(area.offset().top) + parseInt(area.height()) + 2) + 'px');
            },
            stop: function(e, ui) {
                form.css('left', area.offset().left + 'px');
                form.css('top', (parseInt(area.offset().top) + parseInt(area.height()) + 2) + 'px');
            }
        });
        return this;
    };

    $.fn.annotateEdit.prototype.destroy = function() {
        /// <summary>
        ///   Destroys an editable annotation area.
        /// </summary>
        this.image.canvas.children('.image-annotate-edit').hide();
        this.area.resizable('destroy');
        this.area.draggable('destroy');
        this.area.css('height', '');
        this.area.css('width', '');
        this.area.css('left', '');
        this.area.css('top', '');
        this.form.remove();
    }

    $.fn.annotateView = function(image, note) {
        /// <summary>
        ///   Defines a annotation area.
        /// </summary>
        this.image = image;

        this.note = note;

        this.editable = (note.editable && image.editable);

        // Add the area
        this.area = $('<div data-id="' +
                      note.id +
                      '" class="image-annotate-area' +
                      (this.editable ? ' image-annotate-area-editable' : '') +
                      '"><div>' +
                      (note.url? '<a target="_blank" href="' + note.url + '"></a>': '') +
                      '</div></div>');
        if (!note.is_public)
          this.area.addClass('needs-approval');
        image.canvas.children('.image-annotate-view').prepend(this.area);

        // Add the note
        this.form = this.formatForm(note);
        this.form.hide();
        image.canvas.children('.image-annotate-view').append(this.form);
        this.form.children('span.actions').hide();

        // Set the position and size of the note
        this.setPosition();

        // Add the behavior: hide/display the note when hovering the area
        var annotation = this;
        this.area.hover(function() {
            annotation.show();
        }, function() {
            annotation.hide();
        });

        // Edit a note feature
        if (this.editable) {
            var form = this;
            this.area.click(function(e) {
                e.preventDefault();
                e.stopPropagation();
                form.edit();
            });
        }
        window.annot = this;
    };

    $.fn.annotateView.prototype.formatForm = function(note) {
      var approval_text='', approval_class='';
      if (!note.is_public){
        approval_class = ' needs-approval';
        approval_text = ' <span class="needs-approval">(Unapproved)</span>';
      }
      return $('<div class="image-annotate-note' + approval_class + '"><span class="name">' +
               note.display_name + approval_text +
               '</span><span class="org">'+
               note.position + '</span>' +
               ((note.url)? '<a href="' + note.url + '">' + note.url.split('/')[2] + '</a>' : '') +
               '</div>');
      }

    $.fn.annotateView.prototype.setPosition = function() {
        /// <summary>
        ///   Sets the position of an annotation.
        /// </summary>
        this.area.children('div').height((parseInt(this.note.height) - 2) + 'px');
        this.area.children('div').width((parseInt(this.note.width) - 2) + 'px');
        this.area.css('left', (this.note.left) + 'px');
        this.area.css('top', (this.note.top) + 'px');
        this.form.css('left', (this.note.left) + 'px');
        this.form.css('top', (parseInt(this.note.top) + parseInt(this.note.height) + 7) + 'px');
    };

    $.fn.annotateView.prototype.show = function() {
        /// <summary>
        ///   Highlights the annotation
        /// </summary>
        this.form.fadeIn(250);
        if (!this.editable) {
            this.area.addClass('image-annotate-area-hover');
        } else {
            this.area.addClass('image-annotate-area-editable-hover');
        }
    };

    $.fn.annotateView.prototype.hide = function() {
        /// <summary>
        ///   Removes the highlight from the annotation.
        /// </summary>
        this.form.fadeOut(250);
        this.area.removeClass('image-annotate-area-hover');
        this.area.removeClass('image-annotate-area-editable-hover');
    };

    $.fn.annotateView.prototype.destroy = function() {
        /// <summary>
        ///   Destroys the annotation.
        /// </summary>
        this.area.remove();
        this.form.remove();
    }

    $.fn.annotateView.prototype.edit = function() {
        /// <summary>
        ///   Edits the annotation.
        /// </summary>
        if (this.image.mode == 'view') {
            this.image.mode = 'edit';
            var annotation = this;

            // Create/prepare the editable note elements
            var editable = new $.fn.annotateEdit(this.image, this.note);

            $.fn.annotateImage.createSaveButton(editable, this.image, annotation);

            // Add the delete button
            var del = $('<button class="replace" id="image-annotate-edit-delete"><span>Delete</span></button>');
            del.click(function(evt) {
                evt.preventDefault();
                var form = $('#image-annotate-edit-form form');

                $.fn.annotateImage.appendPosition(form, editable)

                if (annotation.image.useAjax) {
                    $.ajax({
                        url: annotation.image.deleteUrl,
                        data: form.serialize(),
                        error: function(e) { alert("An error occured deleting that note.") }
                    });
                }

                annotation.image.mode = 'view';
                editable.destroy();
                annotation.destroy();
            });
            editable.form.find('form div.clear:last').before(del);

            $.fn.annotateImage.createCancelButton(editable, this.image);
        }
    };

    $.fn.annotateImage.appendPosition = function(form, editable) {
        /// <summary>
        ///   Appends the annotations coordinates to the given form that is posted to the server.
        /// </summary>
        var areaFields = $('<input type="hidden" value="' + editable.area.height() + '" name="height"/>' +
                           '<input type="hidden" value="' + editable.area.width() + '" name="width"/>' +
                           '<input type="hidden" value="' + editable.area.position().top + '" name="top"/>' +
                           '<input type="hidden" value="' + editable.area.position().left + '" name="left"/>' +
                           '<input type="hidden" value="' + editable.note.id + '" name="id"/>');
        form.append(areaFields);
    }

    $.fn.annotateView.prototype.resetPosition = function(editable) {;
        /// <summary>
        ///   Sets the position of an annotation.
        /// </summary>
        this.form.html(this.formatForm(editable.note).children());
        this.form.hide();

        // Resize
        this.area.children('div').height(editable.area.height() + 'px');
        this.area.children('div').width((editable.area.width() - 2) + 'px');
        this.area.css('left', (editable.area.position().left) + 'px');
        this.area.css('top', (editable.area.position().top) + 'px');
        this.form.css('left', (editable.area.position().left) + 'px');
        this.form.css('top', (parseInt(editable.area.position().top) + parseInt(editable.area.height()) + 7) + 'px');

        // Save new position to note
        this.note.top = editable.area.position().top;
        this.note.left = editable.area.position().left;
        this.note.height = editable.area.height();
        this.note.width = editable.area.width();
        this.note.last_name = editable.note.last_name;
        this.note.first_name = editable.note.first_name;
        this.note.title = editable.note.title;
        this.note.organization = editable.note.organization;
        this.note.id = editable.note.id;
        this.editable = true;
    };

})(jQuery);