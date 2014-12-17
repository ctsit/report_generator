/**
* This script retrieves the REDI data stored in SiteRunData
* sqlite table and  and renders it for exploration.
*
* @author:
*     Andrei Sura
*     Nicholas Rejack
*/

function RediReporter() {
   console.log('Create reporter...');
}

/**
*  Generate a proper url for invoking API functions
*  @TODO: make the url configurable
*/
function apiPath(callType) {
   return 'http://127.0.0.1:5000' + callType;
}

RediReporter.prototype = {
   init: function() {
      this.progressHide();
      this.projectSitesListHide();
      this.siteDataGraphHide();
      this.initListeners();
      this.loadProjects();
      // util.showFlotDemo();
   },

   /**
   *  Bind the user clicks to specific actions
   */
   initListeners: function() {
      var self = this;

      // Clicking on a project url displays the list of sites
      $("#projects").on('click', 'a[class="getProjectSites"]', function(e) {
         e.preventDefault();
         // var prjID = util.getLastPathFragment(this);
         var prjID = util.getQueryVarFromUrl(this.href, 'prjID');
         self.loadSites(prjID);
     });

      // clicking on a site url displays details
      $("#sites").on('click', 'a[class="drawSiteData"]', function(e) {
         e.preventDefault();
         var siteID = util.getQueryVarFromUrl(this.href, 'siteID');
         console.log('siteID: ' + siteID)
         self.drawSiteData(siteID);
         self.printSiteDataForLastTwoWeeks(siteID);
      });
   },

   /**
   *  Load the list of projects in the database
   *  and display it as an unordered list
   */
   loadProjects: function() {
      var self = this;

      $.ajax({
         url: apiPath('/api/projects/'),
         type: 'POST',
         data: '',
         dataType: 'json',
         success: function( json ) {
            $.each(json, function(i, obj) {
               url = '?prjID=' + obj.prjID;
               ele = $('<a href="' + url + '" class="getProjectSites">').text(obj.prjName)
               $('#projects').append(
                  $('<li>').append(ele)
               );
            });
          }
      });
   },

   /**
   *  Display a list of sites for a project
   */
   loadSites: function(prjID) {
      var self = this;

      console.log('loadSites for prjID: ' + prjID);
      $.ajax({
         url: apiPath('/api/project_sites/' + prjID),
         type: 'POST',
         data: '',
         dataType: 'json',
         success: function( json ) {
            var container = $('#sites');
            container.empty();
            $.each(json, function(i, obj) {
               url = '?siteID=' + obj.siteID;
               ele = $('<a href="' + url + '" class="drawSiteData">').text(obj.siteName)
               container.append(
                  $('<li>').append(ele)
               );

               // self.drawSiteData(obj.siteID);
            });
          }
      });
   },

   getSiteDetails: function(siteID) {
      return 'Site: ' + siteID;
   },

   /**
   *  Create a flot graph for the specified siteID
   */
   drawSiteData: function(siteID) {
      console.log('drawSiteData for siteID: ' + siteID);
      this.progressShow();
      this.siteDataGraphShow();
      // this.projectSitesListHide();

      var siteName = this.getSiteDetails(siteID);

      // erase old data
      var container = $("#placeholder");
      container.empty();
      var siteData = [], siteTicks = [];

      $.ajax({
         url: apiPath('/api/site_data/by_week/' + siteID),
         type: 'POST',
         data: '',
         dataType: 'json',
         success: function( json ) {
            console.log( json );
            var max = 0;

            $.each(json, function(i, obj) {
               max = Math.max(max, obj.subjects);
               siteData.push( [i, obj.subjects] );
               siteTicks.push( [i, obj.time_period] );
            });

            // console.log('site data:' + siteData);
            // console.log('site ticks:' + siteTicks);

      var plot = $.plot(
         "#placeholder",
         [
            {  data: siteData,
               label: siteName,
            },
            // { data: cos, label: "cos(x)"}
         ],
         {
            series: {
               // bars: { show: true, barWidth: 0.4, align: "center" },
               lines: { show: true },
               points: { show: true },

            },
            grid: {
               hoverable: true,
               clickable: true
            },
            xaxis: {
               ticks: siteTicks,
            },
            yaxis: {
               min: 0,
               // max: 300 //max - uncomment to scale individually
               max: max
            }
         });
            plot.setupGrid();
            plot.draw();
         }
      });
      this.progressHide();
   },

   /**
   * Create an html table listing run data for the last two
   * periods for the specified siteID
   */
   printSiteDataForLastTwoWeeks: function(siteID) {
      console.log('print siteID: ' + siteID);
      var self = this;
      var container = $("#site-table-container");

      $.ajax({
         url: apiPath('/api/site_data/last_two_periods/' + siteID),
         type: 'POST',
         data: '',
         dataType: 'json',
         success: function( json ) {
            console.log(json);
            var html = self.generateSiteDataForLastTwoWeeks(json);
            container.empty();
            container.append(html);
            // util.invertTable($("#site-table"));
            $("#site-table").tablesorter();
         }
      });
   },

   /**
   *  Helper method for printSiteDataForLastTwoWeeks()
+-----------------+---------+---------+------------+
| Lab Type        | Last    | Change  | Current    |
+-----------------+---------+---------+------------+
| demographics    |  2      | 3       | 5          |
+-----------------+---------+---------+------------+
| cbc             |  3      | 4       | 7          |
+==================================================+
| Total           |  5      | 7       | 12         |
+-----------------+---------+---------+------------+
   *
   */
   generateSiteDataForLastTwoWeeks: function( json ) {
      console.log(json);
      var html = '<table border="1" cellpadding="4" cellspacing="4" id="site-table" class="tablesorter">'
         + '<caption> Lab counts - comparison for the last two weeks  </caption>'
         + '<thead><tr>'
         + '   <th> Lab Type</th> <th> Last Week </th> <th> Change </th> <th> Current Week </th>'
         + '   </tr></thead>'
         + '<tbody>';

      $.each(json, function(i, obj) {
         var prefix = '', suffix = '';
         if (json.length -1 == i) {
            prefix = '<tfoot>';
            suffix = '</tfoot>';
         }
         row = '\n<tr> <td>' + obj.form + '</td>'
            + ' <td>' + obj.p1 + '</td>'
            + ' <td>' + obj.diff + '</td>'
            + ' <td>' + obj.p2 + '</td>'
            + '\n</tr>';
         html += prefix + row + suffix;
      });

      html += '</tbody></table>';
      return html;
   },

   // Show/hide a spinning wheel
   progressShow: function() {
      $("#progress").show();
   },
   progressHide: function() {
      $("#progress").hide();
   },

   projectSitesListShow: function() {
      $("#sites-container").show();
   },
   projectSitesListHide: function() {
      // $("#sites-container").css( {'color' : 'red'});
      $("#sites-container").hide();
   },

   siteDataGraphShow: function() {
      $(".demo-container").show();
   },
   siteDataGraphHide: function() {
      $(".demo-container").hide();
   },

}; // RediReporter


// =======================
// ====== Misc functions

if (! Array.prototype.indexOf) {
   Array.prototype.indexOf = function(elem) {
      return $.inArray(elem, this);
   };
}
Array.prototype.remove = function(v) {
   this.splice(this.indexOf(v) == -1
      ? this.length
      : this.indexOf(v), 1);
}

Array.prototype.get = function(name) {
   for (var i = 0, len = this.length; i < len; ++i) {
      if (typeof this[i] != "object") {
         continue;
      }
      if (this[i].name === name) {
         return this[i].value;
      }
   }
}

Array.prototype.contains = function(obj) {
   var i = this.length;
   while (i--) {
      if (this[i] === obj) {
         return true;
      }
   }
   return false;
}

// @TODO: make as part of the prototype
function serializeArray(arr) {
   var s = "";
   for (i = 0; i < arr.length; ++i) {
      s += arr[i] + ",";
   }
   return s;
}
// ========== end misc functions

$(document).ready(function() {
   var reporter = new RediReporter();
   reporter.init();
});
