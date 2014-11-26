<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="/js/typeahead.jquery.min.js"></script>
<script type="text/javascript">
var customerSearch = function(q, cb) {
   return $.post('customersearch', { 'searchTerm': q}, function(data)
   {
      return cb(data);
   });
};
$(window).load(function()
{
$('#customername').typeahead({
  hint: true,
  highlight: true,
  minLength: 1
},
{
  name: 'customers',
  displayKey: 'lastName',
  source: customerSearch
});
});
</script>
<style>
/* custom font! */
/* ------------ */

@font-face {
  font-family: Prociono;
  src: url(../font/Prociono-Regular-webfont.ttf);
}

/* scaffolding */
/* ----------- */

html {
  overflow-y: scroll;
  *overflow-x: hidden;
}

.container {
  max-width: 750px;
  margin: 0 auto;
  text-align: center;
}

.tt-dropdown-menu,
.gist {
  text-align: left;
}

/* base styles */
/* ----------- */

html {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 18px;
  line-height: 1.2;
  color: #333;
}

a {
  color: #03739c;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.table-of-contents li {
  display: inline-block;
  *display: inline;
  zoom: 1;
}

.table-of-contents li a {
  font-size: 16px;
  color: #999;
}

.title,
.example-name {
  font-family: Prociono;
}

p + p {
  margin: 30px 0 0 0;
}

/* site theme */
/* ---------- */

.title {
  margin: 20px 0 0 0;
  font-size: 64px;
}

.example {
  padding: 30px 0;
}

.example-name {
  margin: 20px 0;
  font-size: 32px;
}

.demo {
  position: relative;
  *z-index: 1;
  margin: 50px 0;
}

.typeahead,
.tt-query,
.tt-hint {
  width: 396px;
  height: 30px;
  padding: 8px 12px;
  font-size: 24px;
  line-height: 30px;
  border: 2px solid #ccc;
  -webkit-border-radius: 8px;
     -moz-border-radius: 8px;
          border-radius: 8px;
  outline: none;
}

.typeahead {
  background-color: #fff;
}

.typeahead:focus {
  border: 2px solid #0097cf;
}

.tt-query {
  -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
     -moz-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
          box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
}

.tt-hint {
  color: #999
}

.tt-dropdown-menu {
  width: 422px;
  margin-top: 12px;
  padding: 8px 0;
  background-color: #fff;
  border: 1px solid #ccc;
  border: 1px solid rgba(0, 0, 0, 0.2);
  -webkit-border-radius: 8px;
     -moz-border-radius: 8px;
          border-radius: 8px;
  -webkit-box-shadow: 0 5px 10px rgba(0,0,0,.2);
     -moz-box-shadow: 0 5px 10px rgba(0,0,0,.2);
          box-shadow: 0 5px 10px rgba(0,0,0,.2);
}

.tt-suggestion {
  padding: 3px 20px;
  font-size: 18px;
  line-height: 24px;
}

.tt-suggestion.tt-cursor {
  color: #fff;
  background-color: #0097cf;

}

.tt-suggestion p {
  margin: 0;
}

.gist {
  font-size: 14px;
}

/* example specific styles */
/* ----------------------- */

#custom-templates .empty-message {
  padding: 5px 10px;
 text-align: center;
}

#multiple-datasets .league-name {
  margin: 0 20px 5px 20px;
  padding: 3px 0;
  border-bottom: 1px solid #ccc;
}

#scrollable-dropdown-menu .tt-dropdown-menu {
  max-height: 150px;
  overflow-y: auto;
}

#rtl-support .tt-dropdown-menu {
  text-align: right;
}
</style>
</head>
<body>
<div id="hbox">
  <div class="box">
      <h2>Search for Customer</h2>
      <form action="customersearch" method="post" name="customersearch">
        <div id="the-basics">
          <input class="typeahead" type="text" id="customername" name="customername" />
        </div>
          <button type="submit" >OK</button>
      </form>
      <br />
  </div>
  <br style="clear: left;" />
</div>
</body>
</html>