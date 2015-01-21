% include renders
% renders_namespace = _ 
% get_field_errors = renders_namespace['get_field_errors']
% get_menu = renders_namespace['get_menu']

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
% get_menu()
<div id='main'>
    <h2>Cork - Administration page</h2>
    <div id='commands'>
      <p>Create new user:</p>
      <form action="create_user" method="post">
          <p><label>Username</label> <input type="text" name="username" /></p>
          <p><label>Role</label> <input type="text" name="role" /></p>
          <p><label>Password</label> <input type="password" name="password" /></p>
          <div class="row">
          <div class="form-group">
          <div class="col-sm-2"><button type="submit" class="btn btn-default">OK</button></div>
          <div class="col-sm-2"><button type="button" class="btn">Cancel</button></div>
          </div>
          </div>
      </form>
      <br />
      <p>Delete user:</p>
      <form action="delete_user" method="post">
          <p><label>Username</label> <input type="text" name="username" /></p>
          <div class="row">
          <div class="form-group">
          <div class="col-sm-2"><button type="submit" class="btn btn-default">OK</button></div>
          <div class="col-sm-2"><button type="button" class="btn">Cancel</button></div>
          </div>
          </div>
      </form>
      <br />
      <p>Create new role:</p>
      <form action="create_role" method="post">
          <p><label>Role</label> <input type="text" name="role" /></p>
          <p><label>Level</label> <input type="text" name="level" /></p>
          <div class="row">
          <div class="form-group">
          <div class="col-sm-2"><button type="submit" class="btn btn-default">OK</button></div>
          <div class="col-sm-2"><button type="button" class="btn">Cancel</button></div>
          </div>
          </div>
      </form>
      <br />
      <p>Delete role:</p>
      <form action="delete_role" method="post">
          <p><label>Role</label> <input type="text" name="role" /></p>
          <div class="row">
          <div class="form-group">
          <div class="col-sm-2"><button type="submit" class="btn btn-default">OK</button></div>
          <div class="col-sm-2"><button type="button" class="btn">Cancel</button></div>
          </div>
          </div>
      </form>
    </div>
    <div id="users">
        <table>
            <tr><th>Username</th><th>Role</th><th>Email</th><th>Description</th></tr>
            %for u in users:
            <tr><td>{{u[0]}}</td><td>{{u[1]}}</td><td>{{u[2]}}</td><td>{{u[2]}}</td></tr>
            %end
        </table>
        <br/>
        <table>
            <tr><th>Role</th><th>Level</th></tr>
            %for r in roles:
            <tr><td>{{r[0]}}</td><td>{{r[1]}}</td></tr>
            %end
        </table>
        <p>(Reload page to refresh)</p>
    </div>

    <div class="clear"></div>

    <div id='status'><p>Ready.</p></div>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
    <script>
        // Prevent form submission, send POST asynchronously and parse returned JSON
        $('form').submit(function() {
            $("div#status").fadeIn(100);
            z = $(this);
            $.post($(this).attr('action'), $(this).serialize(), function(j){
              if (j.ok) {
                $("div#status").css("background-color", "#f0fff0");
                $("div#status p").text('Ok.');
              } else {
                $("div#status").css("background-color", "#fff0f0");
                $("div#status p").text(j.msg);
              }
              $("div#status").delay(800).fadeOut(500);
            }, "json");
            return false;
        });
    </script>
</div>
<style>
div#commands { width: 45%%; float: left}
div#users { width: 45%; float: right}
div#main {
    color: #777;
    margin: auto;
    margin-left: 5em;
    font-size: 80%;
}
input {
    background: #f8f8f8;
    border: 1px solid #777;
    margin: auto;
}
input:hover { background: #fefefe}
label {
  width: 8em;
  float: left;
  text-align: right;
  margin-right: 0.5em;
  display: block
}
button {
    margin-left: 13em;
}
button.close {
    margin-left: .1em;
}
div#status {
    border: 1px solid #999;
    padding: .5em;
    margin: 2em;
    width: 15em;
    -moz-border-radius: 10px;
    border-radius: 10px;
}
.clear { clear: both;}
</style>
</body>
</html>