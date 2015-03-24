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
  </head>
  <body>
    % get_menu()
    <div id="vis"></div>
  </body>
<script type="text/javascript">
// parse a spec and create a visualization view
function parse(spec)
{
    vg.parse.spec(spec, function(chart){ chart({el:"#vis"}).update(); });
}
$.ajax({ url: "/report/info/1", success: function() {
    parse("/report/graphdata/1", "line");  
} });

</script>
</html>