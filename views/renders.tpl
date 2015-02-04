% def get_menu():
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<link rel="stylesheet" href="/css/bootstrap.min.css">
<link rel="stylesheet" href="/css/bootstrap-theme.min.css">
<script src="/js/bootstrap.min.js"></script>
<style>
.navbar-default .navbar-nav>.active>a
{
    background-color: rgb(0, 88, 110);
    color: #FDFDFD;
    background-image:inherit;
}
.navbar-default .navbar-nav>.active>a:hover
{
    background-color: rgb(0, 78, 100);
    color: #FDFDFD;
    background-image:inherit;
}
</style>
<nav class="navbar navbar-default" role="navigation">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <!--<a class="navbar-brand" href="/">Twice Blessed</a>-->
    </div>
    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        % isCheckin = ""
        % isCustomer = ""
        % isCheckoutSearch = ""
        % isAdmin = ""
        % if page == "/":
        % isCheckoutSearch = "active"
        % elif page == "/checkin":
        % isCheckin = "active"
        % elif page == "/customer":
        % isCustomer = "active"
        % elif page == "/admin":
        % isAdmin = "active"
        % end
        <li class="{{isCheckin}}"><a href="/checkin">Check In</a>
        <li class="{{isCustomer}}"><a href="/customer">Registration</a></li>
        <li class="{{isCheckoutSearch}}"><a href="/">Check Out</a>
        % if aaa.current_user.role == 'admin':
        <li class="{{isAdmin}}"><a href="/admin">Admin</a></li>
        % end
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="/logout">Logout</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
% end

% def get_field_errors(field):
    % if field.errors:
        % for e in field.errors:
            <p class="help-block" style="margin-left:20px">{{ e }}</p>
        % end
    % end
% end
        
% def render_field(field, label_visible=True, **kwargs):
    <div class="form-group \\
    % if field.errors:
has-error\\
    % end
{{ kwargs.pop('class_', '') }}">
        % if (field.type != 'HiddenField' or field.type !='CSRFTokenField') and label_visible and field.widget.input_type != 'hidden':
        <label for="{{ field.id }}" class="col-sm-2 control-label">{{ field.label.text }}</label>
        % end
        <div class="col-sm-10">
            {{! field(class_='form-control', **kwargs) }}
        </div>
        % if field.errors:
            % for e in field.errors:
        <p class="help-block">{{ e }}</p>
            % end
        % end
    </div>
% end
