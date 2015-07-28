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

    #title
    {
      margin-bottom: 10px;
    }

    #info
    {
      margin-bottom: 10px;
      float:left;
    }
    </style>
  </head>
  <body>
    % get_menu()
    <select id="reportSelect" onchange="runReport()">
    % for key, value in report_options.items():
    <option value="{{key}}">{{value.description}}</option>
    % end
    </select>

    <div id="title"></div>
    <div id="info"></div>
    <div id="vis"></div>
  </body>
<script type="text/javascript">
// parse a spec and create a visualization view
function parse(spec)
{
    vg.parse.spec(spec, function(chart){ chart({el:"#vis"}).update(); });
}

function runReport()
{
    var selectedReportNum = document.getElementById("reportSelect").value;
    $.ajax({ url: "/report/info/"+selectedReportNum, success: function(reportInfo) {
      $("#title").text(reportInfo.title);
      $("#info").html(reportInfo.html);
      if (!reportInfo.nograph)
      {
         parse("/report/graphdata/"+selectedReportNum, "line");
      }
      else
      {
         $("#vis").text('');
      }
    } });
}

$("#reportSelect")[0].selectedIndex = 0;
runReport();
</script>
</html>
