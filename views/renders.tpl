% def render_field(field, label_visible=True, **kwargs):
    <div class="form-group \\
    % if field.errors:
has-error\\
    % end
{{ kwargs.pop('class_', '') }}">
        % if (field.type != 'HiddenField' or field.type !='CSRFTokenField') and label_visible:
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
            % else:
                % render_field(f)
            % end
        % end
        <button type="submit" class="{{ btn_class }}">{{ action_text }} </button>
    </form>
% end