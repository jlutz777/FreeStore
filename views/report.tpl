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

$(document).ready(function () {
    $('#startdate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
    $('#enddate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
    $("#reportselect")[0].selectedIndex = 0;
    runReport();
});
</script>
</html>
