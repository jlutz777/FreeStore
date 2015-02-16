<html>
  <head>
    <title>Vega Scaffold</title>
    <script src="//cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js" charset="utf-8"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/d3-geo-projection/0.2.9/d3.geo.projection.min.js" charset="utf-8"></script>
    <script src="//wrobstory.github.io/vega/vega.v1.3.3.js"></script>
  </head>
  <body>
    <div id="vis"></div>
  </body>
<script type="text/javascript">
// parse a spec and create a visualization view
function parse(spec) {
  vg.parse.spec(spec, function(chart) { chart({el:"#vis"}).update(); });
}
parse("/report/1", "bar")
</script>
</html>