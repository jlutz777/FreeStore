% def get_menu():
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="/js/typeahead.jquery.min.js"></script>
<link rel="stylesheet" href="/css/bootstrap.min.css">
<link rel="stylesheet" href="/css/bootstrap-theme.min.css">
<script src="/js/bootstrap.min.js"></script>
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
      <a class="navbar-brand" href="/">Twice Blessed</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="/customer">Registration <span class="sr-only">(current)</span></a></li>
        <li><a href="#">Link</a></li>
        <!--<li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Dropdown <span class="caret"></span></a>
          <ul class="dropdown-menu" role="menu">
            <li><a href="#">Action</a></li>
            <li><a href="#">Another action</a></li>
            <li><a href="#">Something else here</a></li>
            <li class="divider"></li>
            <li><a href="#">Separated link</a></li>
            <li class="divider"></li>
            <li><a href="#">One more separated link</a></li>
          </ul>
        </li>-->
      </ul>
      <!--<form class="navbar-form navbar-left" role="search">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Search">
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>-->
      <ul class="nav navbar-nav navbar-right">
        <li><a href="/logout">Logout</a></li>
        <!--<li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Dropdown <span class="caret"></span></a>
          <ul class="dropdown-menu" role="menu">
            <li><a href="#">Action</a></li>
            <li><a href="#">Another action</a></li>
            <li><a href="#">Something else here</a></li>
            <li class="divider"></li>
            <li><a href="#">Separated link</a></li>
          </ul>
        </li>-->
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
% end

% def get_field_errors(field):
    % if field.errors:
        % for e in field.errors:
            <p class="help-block">{{ e }}</p>
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

% def render_multi_field(field, **kwargs):
    <div class="form-group fieldset" data-toggle="fieldset" id="dependent-fieldset">
        {{ kwargs["multi_field_label"] }}
        <div data-toggle="fieldset-entry">
        % for index, subfield in enumerate(field[0]):
            % render_field(subfield)
        % end
        </div>
        <button type="button" class="remove_button" data-toggle="fieldset-remove-row">-</button>
    </div>
    <button type="button" id="add_another_button">+</button>
% end

% def render_checkbox_field(field):
    <div class="checkbox">
        <label>
            {{! field(type='checkbox', **kwargs) }} {{ field.label }}
        </label>
    </div>
% end
 
% def render_radio_field(field):
    % for value, label, _ in field.iter_choices():
        <div class="radio">
            <label>
                <input type="radio" name="{{ field.id }}" id="{{ field.id }}" value="{{ value }}">{{ label }}
            </label>
        </div>
    % end
% end
 
% def render_form(form, action_url='', action_text='Submit', class_='form_horizontal', btn_class='btn btn-default'):
    <form method="POST" action="{{ action_url }}" role="form" class="{{ class_ }}">
        % for f in form:
            % if f.type == 'BooleanField':
                % render_checkbox_field(f)
            % elif f.type == 'RadioField':
                % render_radio_field(f)
            % elif f.type in ['FieldList', 'ModelFieldList']:
                % render_multi_field(f, multi_field_label=f.label.text)
            % else:
                % render_field(f)
            % end
        % end
        <button type="submit" class="{{ btn_class }}">{{ action_text }} </button>
    </form>
% end