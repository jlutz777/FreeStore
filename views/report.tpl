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
    <style type="text/css">
    .date
    {
      vertical-align: bottom;
      width: 125px;
    }

    .category
    {
      vertical-align: bottom;
      width: 150px;
    }

    .count
    {
      width: 50px;
    }
    
    #report_filter
    {
       height: 100px;
    }
    
    #title
    {
      margin-top: 30px;
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
            <input class="form-control" id="startdate" onkeydown="inputKeyDown()" name="startdate">
        </div>
    </div>
    </div>
    <div class="row">
    <div class="form-group ">
        <label for="enddate" class="col-sm-2 control-label">End Date:</label>
        <div class="col-sm-8">
            <input class="form-control" id="enddate" onkeydown="inputKeyDown()" name="enddate">
        </div>
    </div>
    </div>
    <h3 id="title"></h3>
    <div class="container-fluid">
        <div class="col-md-12">
            <div id="info"></div>
        </div>
        <div class="col-md-12">
            <div id="vis"></div>
        </div>
    </div>
  </body>
<script type="text/javascript">
function newParse(reportGraph)
{
    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = 600 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;

    // Parse the date / time
    var parseDate = d3.time.format("%m/%d/%Y").parse;
    
    // Set the ranges
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    // For multiple lines
    var color = d3.scale.category10();
    var line = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.count); });
    
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

    function singleLineGraph(data)
    {
        data.forEach(function(d)
        {
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
            var x0 = x.invert(d3.mouse(this)[0]);
            var i = bisectDate(data, x0, 1);
            var d0 = data[i - 1];
            var d1 = data[i];
            var d = x0 - d0.date > d1.date - x0 ? d1 : d0;
            focus.attr("transform", "translate(" + x(d.date) + "," + y(d.count) + ")");
            focus.select("text").html(d.count + " - " + (d.date.getMonth()+1) + "/" + d.date.getDate());
        }
    }
    
    function multiLineGraph(data)
    {
        data.forEach(function(d)
        {
            d.date = parseDate(d.date);
            //d.count = +d.count;
        });
        
        color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));
        
        var categories = color.domain().map(function(name) {
            return {
                name: name,
                values: data.map(function(d)
                {
                    return {date: d.date, count: +d[name]};
                })
            };
        });
    
        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([
            d3.min(categories, function(c) { return d3.min(c.values, function(v) { return v.count; }); }),
            d3.max(categories, function(c)
                {
                    if (c.name == 'Clothing')
                        return 0;
                    else
                        return d3.max(c.values, function(v) { return v.count; });
                })
        ]);
    
        // Add the valueline path.
        var city = svg.selectAll(".category")
                      .data(categories)
                      .enter().append("g")
                      .attr("class", "category");

        city.append("path")
            .attr("class", "line")
            .attr("d", function(d) { return line(d.values); })
            .style("stroke", function(d) { return color(d.name); });
    
        city.append("text")
            .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
            .attr("transform", function(d)
                               {
                                   return "translate(" + x(d.value.date) + "," + y(d.value.count) + ")";
                               })
            .attr("x", 3)
            .attr("dy", ".35em")
            .text(function(d) { return d.name; });

        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
    
        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);
    }
    
    var keys = d3.keys(reportGraph[0]);
    if (keys.length == 2)
    {
        singleLineGraph(reportGraph);
    }
    else
    {
        multiLineGraph(reportGraph);
    }
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
      reportData = reportInfo.data;
      reportGraph = reportInfo.graph;
      $("#title").text(reportData.title);
      $("#info").html(reportData.html);
      $("#vis").text('');
      if (reportGraph)
      {
         newParse(reportGraph);
      }
    } });
}

function inputKeyDown()
{
    if (event.keyCode == 13) {
        runReport();
    }
}

$(document).ready(function () {
    $('#startdate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
    $('#enddate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
    $("#reportselect")[0].selectedIndex = 0;
    runReport();
});
</script>
</html>
