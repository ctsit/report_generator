
var util = {

   showDialog: function(title, msg, callbackOk, callbackCancel) {
      var win = $('<div>');
      var p = $('<p>').text(msg).appendTo(win);
      var close = function() {
         win.dialog( "close" );
      };

      win.dialog({
         title: title,
         position: ['center', 50],
         closeOnEscape: true,
         modal: true,
         buttons: {
            OK       : ( typeof callbackOk      === 'function' ? function() { callbackOk();     close(); } : close),
            Cancel   : ( typeof callbacCancel   === 'function' ? function() { callbackCancel(); close(); } : close)
         },
         maxHeight: 800,
         width: 800,
      });
   },

   /**
   * Displays a list of errors.
   * @see #showSuccess()
   */
   showErrors: function (errors, callback) {
      var win = $('<div id="createErrors">');
      var errorsList = $('<ul>');

      if ($.isArray(errors)) {
         for (i = 0; i < errors.length; ++i) {
            $('<li>').text(errors[i]).appendTo(errorsList);
         }
      }
      else {
         $('<li>').text(errors).appendTo(errorsList);
      }
      errorsList.appendTo(win);

      win.dialog({
         title: "Please fix the following errors",
         dialogClass: '',
         position: ['center', 50],
         closeOnEscape: true,
         modal: true,
         buttons: {
            OK: function() {
               $( this ).dialog( "close" );
               callback();
            }
         },
         maxHeight: 600,
         width: 600,
      });
   },

   handleResponse: function(request, msgSuccess, callback) {
      request.success( function( json ) {
         if (json.hasOwnProperty('errors') ) {
            util.showErrors(json.errors);
            callback(false);
         }
         else {
            util.showSuccess(msgSuccess, callback(true));
         }
      });
      request.fail( function( jqXHR, textStatus, error ) {
         console.log('Failed in handleResponse(): ' + textStatus + " " + error);
      });

   },

   /**
   * Displays a custom success message.
   * @see #showErrors()
   */
   showSuccess: function(msg, callback) {
      util.showWindow('Success', msg, callback);
   },

   showWindow: function(title, msg, callback) {
      var win = $('<div id="createSuccess">');
      $('<p>').text(msg).appendTo(win);

      win.dialog({
         title: title,
         dialogClass: '',
         position: ['center', 50],
         closeOnEscape: true,
         modal: true,
         buttons: {
            OK: function() {
               $( this ).dialog( "close" );

               if (typeof callback === 'function') {
                  callback();
               }
            }
         },
         maxHeight: 600,
         width: 600,
      });
   },

/*
var el = document.createElement('a');
el.href = "http://www.somedomain.com/account/search?filter=a#top";

el.host        // www.somedomain.com (includes port if there is one[1])
el.hostname    // www.somedomain.com
el.hash        // #top
el.href        // http://www.somedomain.com/account/search?filter=a#top
el.pathname    // /account/search
el.port        // (port if there is one[1])
el.protocol    // http:
el.search      // ?filter=a
*/

   getLinkHash: function(urlString) {
      var url = document.createElement('a').href(urlString);
      return url.hash;
   },

   getLinkEleHash: function(urlEle) {
      return urlEle.hash;
   },

   getPathFragments: function(urlEle) {
      return urlEle.pathname.split('/');
   },

   getLastPathFragment: function(urlEle) {
      var fragments = this.getPathFragments(urlEle);
      // console.log(fragments);
      return fragments[fragments.length - 1];
   },

   print_r: function (o) {
      return JSON.stringify(o,null,'\t').replace(/\n/g,'<br>').replace(/\t/g,'&nbsp;&nbsp;&nbsp;');
   },

   array_keys: function(obj) {
      list = [];
      for(var key in obj) {
         list.push(key);
      }
      return list;
   },

   getQueryVarFromUrl: function(url, varName) {
      var query = url.split('?');
      query = query[1];

      var vars = query.split("&");
      for (var i = 0; i < vars.length; ++i) {
         var pair = vars[i].split("=");
         if (pair[0] == varName) {
            return pair[1];
         }
      }
      return(false);
   },

   showFlotDemo: function() {
      var sin = [],
         cos = [];

      for (var i = 0; i < 14; i += 0.5) {
         sin.push([i, Math.sin(i)]);
         cos.push([i, Math.cos(i)]);
      }

      var plot = $.plot(
         "#placeholder",
         [
            { data: sin, label: "sin(x)"},
            // { data: cos, label: "cos(x)"}
         ],
         {
            series: {
               bars: { show: true, barWidth: 0.4, align: "center" },
               // lines: { show: true },
               points: { show: true }
            },
            grid: {
               hoverable: true,
               clickable: true
            },
            yaxis: {
               min: -1.2,
               max: 1.2
            }
         }
      );

      $("<div id='tooltip'></div>").css({
         position: "absolute",
         display: "none",
         border: "1px solid #fdd",
         padding: "2px",
         "background-color": "#fee",
         opacity: 0.80
      }).appendTo("body");

      $("#placeholder").bind("plothover", function (event, pos, item) {

         if ($("#enablePosition:checked").length > 0) {
            var str = "(" + pos.x.toFixed(2) + ", " + pos.y.toFixed(2) + ")";
            $("#hoverdata").text(str);
         }

         if ($("#enableTooltip:checked").length > 0) {
            if (item) {
               var x = item.datapoint[0].toFixed(2),
                  y = item.datapoint[1].toFixed(2);

               $("#tooltip").html(item.series.label + " of " + x + " = " + y)
                  .css({top: item.pageY+5, left: item.pageX+5})
                  .fadeIn(200);
            } else {
               $("#tooltip").hide();
            }
         }
      });

      $("#placeholder").bind("plotclick", function (event, pos, item) {
         if (item) {
            $("#clickdata").text(" - click point " + item.dataIndex + " in " + item.series.label);
            plot.highlight(item.series, item.datapoint);
         }
      });

      // Add the Flot version string to the footer

      $("#footer").prepend("Flot " + $.plot.version + " &ndash; ");
   },

   invertTable: function(tableEle) {
      // from http://stackoverflow.com/questions/16071864/how-to-create-tables-from-column-data-instead-of-row-data-in-html
      tableEle.each(function () {
        var $this = $(this);
        var newrows = [];
        $this.find("tr").each(function () {
            var i = 0;
            $(this).find("td,th").each(function () {
                i++;
                if (newrows[i] === undefined) {
                    newrows[i] = $("<tr></tr>");
                }
                newrows[i].append($(this));
            });
        });
        $this.find("tr").remove();
        $.each(newrows, function () {
            $this.append(this);
        });
    });

   },

};
