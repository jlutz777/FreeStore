% include renders
% renders_namespace = _ 
% get_field_errors = renders_namespace['get_field_errors']
% get_menu = renders_namespace['get_menu']

<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
% get_menu()
<div class="container-fluid">
<div class="page-header">
    <h3>Administration</h3>
</div>
<!-- Ractive practice -->
<script src='/js/ractive.min.js'></script>
<script src='/js/admin.js'></script>
<script id="user_li_template" type="text/ractive">
[[#users:name]]
    <li class="list-group-item" data-toggle="modal" data-user-id="[[name]]" data-target="#user_modal"><span>[[name]]</span></li>
[[/users]]
</script>
<script id="user_template" type="text/ractive">
    <form id="user_form" action="[[#if existing]]edit_user[[else]]create_user[[/if]]" data-target="#user_modal" method="post">
        <div class="form-horizontal">
        <div class="form-group">
            <label for="username" class="col-sm-4 control-label">User name</label>
            <div class="col-sm-8">
                <input class="form-control" [[#if existing]]readonly[[/if]] id="username" type="text" name="username" value="[[name]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="description" class="col-sm-4 control-label">Description</label>
            <div class="col-sm-8">
                <input class="form-control" [[#if existing]]readonly[[/if]] id="description" type="text" name="description" value="[[description]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="role" class="col-sm-4 control-label">Role</label>
            <div class="col-sm-8">
                <select id="role" name="role" class="form-control" value='[[role]]'>
                  [[#roles:name]]
                    <option value='[[name]]'>[[name]]</option>
                  [[/roles]]
                </select>
            </div>
        </div>
        <div class="form-group">
            <label for="email" class="col-sm-4 control-label">Email</label>
            <div class="col-sm-8">
                <input class="form-control" id="email" type="text" name="email" value="[[email]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="password" class="col-sm-4 control-label">Password</label>
            <div class="col-sm-8">
                <input class="form-control" id="password" type="password" name="password" value="[[password]]" />
            </div>
        </div>
        </div>
      </form>
</script>
<script id="role_li_template" type="text/ractive">
[[#roles:name]]
    <li class="list-group-item" data-toggle="modal" data-role-id="[[name]]" data-target="#role_modal"><span>[[name]]</span></li>
[[/roles]]
</script>
<script id="role_template" type="text/ractive">
    <form id="role_form" action="[[#if existing]]edit_role[[else]]create_role[[/if]]" data-target="#role_modal" method="post">
        <div class="form-horizontal">
        <div class="form-group">
            <label for="role" class="col-sm-4 control-label">Name</label>
            <div class="col-sm-8">
                <input class="form-control" [[#if existing]]readonly[[/if]] id="role" type="text" name="role" value="[[name]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="level" class="col-sm-4 control-label">Level (0-100)</label>
            <div class="col-sm-8">
                <input class="form-control" id="level" type="text" name="level" value="[[level]]" />
            </div>
        </div>
</script>

<script type="text/javascript">
    var users = {};
    var roles = {};
    
    %for u in users:
    users["{{u[0]}}"] = {
            name: "{{u[0]}}",
            role: "{{u[1]}}",
            email: "{{u[2]}}",
            description: "{{u[3]}}",
            password: "",
            existing: true
        };
    %end
    
    %for r in roles:
    roles["{{r[0]}}"] = {
            name: "{{r[0]}}",
            level: "{{r[1]}}"
        };
    %end
</script>
<div id="user_modal" class="modal fade">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Edit User</h4>
      </div>
      <div id="user_modal_body" class="modal-body">
      </div>
      <div class="modal-footer">
        <button id="delete_user" type="button" class="btn btn-warning">Delete</button>
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button id="save_user" type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
<div id="role_modal" class="modal fade">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Edit Role</h4>
      </div>
      <div id="role_modal_body" class="modal-body">
      </div>
      <div class="modal-footer">
        <button id="delete_role" type="button" class="btn btn-warning">Delete</button>
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button id="save_role" type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
<div class="container-fluid" style="width:90%">
    <div class="panel panel-default">
        <div class="panel-heading">Users</div>
        <div class="panel-body">
            <ul id="user_list" class="list-group">
                %for u in users:
                <li class="list-group-item" data-toggle="modal" data-="{{u[0]}}" data-target="#user_modal"><span>{{u[0]}}</span></li>
                %end
            </ul>
        </div>
        <div class="panel-footer">
            <button id="add_user" type="button" class="btn btn-primary">Add</button>
        </div>
    </div>
    <!--<div class="panel panel-default">
        <div class="panel-heading">Roles</div>
        <div class="panel-body">
            <ul id="role_list" class="list-group">
                %for r in roles:
                <li class="list-group-item" data-toggle="modal" data-="{{r[0]}}" data-target="#role_modal"><span>{{r[0]}}</span></li>
                %end
            </ul>
        </div>
        <div class="panel-footer">
            <button id="add_role" type="button" class="btn btn-primary">Add</button>
        </div>
    </div>-->
</div>
</body>
</html>