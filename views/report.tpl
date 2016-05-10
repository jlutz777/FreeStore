% include renders
% renders_namespace = _
% get_field_errors = renders_namespace['get_field_errors']
% get_menu = renders_namespace['get_menu']

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta content="text/html; charset=utf-8" http-equiv="content-type">
    <title>Report</title>
    <script src="//cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js" charset="utf-8"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/d3-geo-projection/0.2.9/d3.geo.projection.min.js" charset="utf-8"></script>
    <script src="//wrobstory.github.io/vega/vega.v1.3.3.js"></script>
    <style type="text/css">
    td.date
    {
      width: 125px;
    }

    td.category
    {
      width: 150px;
    }

    td.count
    {
      width: 50px;
    }

    #report_filter
    {
       height: 100px;
    }
    
    #title
    {
      margin-bottom: 10px;
    }

    #info
    {
      margin-bottom: 10px;
      float:left;
    }
    
    /* new styles */
path { 
    stroke: steelblue;
    stroke-width: 2;
    fill: none;
}

.axis path,
.axis line {
    fill: none;
    stroke: grey;
    stroke-width: 1;
    shape-rendering: crispEdges;
}

.overlay {
  fill: none;
  pointer-events: all;
}

.focus circle {
  fill: none;
  stroke: steelblue;
}
    /* end new styles */
    </style>
  </head>
  <body>
    % get_menu()
    <script src="/js/jquery.mask.min.js"></script>
    <div class="row">
    <div class="form-group ">
        <label for="reportselect" class="col-sm-2 control-label">Choose a report:</label>
        <div class="col-sm-8">
            <select id="reportselect" onchange="runReport()">
            % for key, value in report_options.items():
                <option value="{{key}}">{{value.description}}</option>
            % end
            </select>
        </div>
    </div>
    </div>
    <div class="row">
    <div class="form-group ">
        <label for="startdate" class="col-sm-2 control-label">Start Date:</label>
        <div class="col-sm-8">
            <input class="form-control" id="startdate" name="startdate">
        </div>
    </div>
    </div>
    <div class="row">
    <div class="form-group ">
        <label for="enddate" class="col-sm-2 control-label">End Date:</label>
        <div class="col-sm-8">
            <input class="form-control" id="enddate" name="enddate">
        </div>
    </div>
    </div>
    <div id="title"></div>
    <div id="info"></div>
    <div id="vis"></div>
  </body>
<script type="text/javascript">
/*
https://leanpub.com/D3-Tips-and-Tricks/read#leanpub-auto-starting-with-a-basic-graph
*/
function newParse(reportNum)
{
// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 600 - margin.left - margin.right,
    height = 270 - margin.top - margin.bottom;

// Parse the date / time
var parseDate = d3.time.format("%m/%d/%Y").parse;
var MAndD = d3.time.format("%M/%d").parse;

// Set the ranges
var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);

// Define the axes
var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);

var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

// Define the line
var valueline = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.count); });
    
// Adds the svg canvas
var svg = d3.select("#vis")
    .append("svg")
        .attr("width", width + margin.left + margin.right+60)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");

$.ajax({ url: 'report/data/' + reportNum, success: function(data) {
    data.forEach(function(d) {
        d.date = parseDate(d.date);
        d.count = +d.count;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.count; })]);

    // Add the valueline path.
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));
        
    /*svg.append("svg:title")
   .text(function(d) {
       debugger;
       return d.x; });*/


    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

var focus = svg.append("g")
      .attr("class", "focus")
      .style("display", "none");

  focus.append("circle")
      .attr("r", 4.5);

  focus.append("text")
      .attr("x", 9)
      .attr("dy", ".35em");

    svg.append("rect")
      .attr("class", "overlay")
      .attr("width", width)
      .attr("height", height)
      .on("mouseover", function() { focus.style("display", null); })
      .on("mouseout", function() { focus.style("display", "none"); })
      .on("mousemove", mousemove);

    bisectDate = d3.bisector(function(d) { return d.date; }).left;
    function mousemove() {
    var x0 = x.invert(d3.mouse(this)[0]),
        i = bisectDate(data, x0, 1),
        d0 = data[i - 1],
        d1 = data[i],
        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
    focus.attr("transform", "translate(" + x(d.date) + "," + y(d.count) + ")");
    focus.select("text").html(d.count + " - " + (d.date.getMonth()+1) + "/" + d.date.getDate());
  }

}});
}
// parse a spec and create a visualization view
function parse(spec)
{
    vg.parse.spec(spec, function(chart){ chart({el:"#vis"}).update(); });
}

function runReport()
{
    var selectedReportNum = $("#reportselect").val();
    var startDate = $("#startdate").val();
    var endDate = $("#enddate").val();
    var reportUrl = "/report/info/" + selectedReportNum + "?";
    if (startDate !== "")
    {
        reportUrl += "startDate=" + startDate + "&";
    }
    if (endDate !== "")
    {
        reportUrl += "endDate=" + endDate;
    }
    
    $.ajax({ url: reportUrl, success: function(reportInfo) {
      $("#title").text(reportInfo.title);
      $("#info").html(reportInfo.html);
      $("#vis").text('');
      if (!reportInfo.nograph)
      {
         if (selectedReportNum == 1 || selectedReportNum == 2
             || selectedReportNum == 3 || selectedReportNum == 4)
         {
             newParse(selectedReportNum);
         }
         else
         {
             parse("/report/graphdata/"+selectedReportNum, "line");
         }
      }
    } });
}

$(document).ready(function () {
    $('#startdate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
    $('#enddate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
    $("#reportselect")[0].selectedIndex = 0;
    runReport();
});
</script>
</html>
