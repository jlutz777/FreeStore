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
<script src="/js/jquery.mask.min.js"></script>
<script type="text/javascript">
$(document).ready(function () {
    // TODO: haven't tested to make sure this works right on POST!!
    $('#checkin').mask("00/00/0000 00:00", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY hh:mm"});
    $('#checkout').mask("00/00/0000 00:00", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY hh:mm"});
});
</script>
<div class="container-fluid">
    % if form.errors:
    <div class="page-header">
        <h3 class="text-danger">Correct The Errors Below!</h3>
        % for field, errors in form.errors.items():
        % for error in errors:
        {{error}}
        % end
        % end
    </div>
    % end
<form id="thisForm" method="POST" action="{{post_url}}" role="form">
    <div class="page-header">
        <h3 class="text">
        % for dependent in family.dependents:
            % if dependent.isPrimary:
                {{dependent.firstName}} {{dependent.lastName}}
                % break
            % end
        % end
        </h3>
    </div>
    <input id="family_id" name="family_id" type="hidden" value="{{form.family_id.data}}">
    % if form.id.data is not None:
    <input id="id" name="id" type="hidden" value="{{form.id.data}}">
    % end
    <div class="form-group 
        % if form.checkin.errors:
        has-error
        % end
        ">
            <label for="checkin" class="col-sm-2 control-label">Checkin</label>
            <div class="col-sm-10">
                % if form.checkin.data is not None:
                <input autofocus class="form-control" id="checkin" name="checkin" type="text" value="{{form.checkin.data}}">
                % else:
                <input autofocus class="form-control" id="checkin" name="checkin" type="text" value="">
                % end
                % get_field_errors(form.checkin)
            </div>
        </div>
    <div class="form-group 
        % if form.checkout.errors:
        has-error
        % end
        ">
            <label for="checkout" class="col-sm-2 control-label">Checkout</label>
            <div class="col-sm-10">
                % if form.checkout.data is not None:
                <input class="form-control" id="checkout" name="checkout" type="text" value="{{form.checkout.data}}">
                % else:
                <input class="form-control" id="checkout" name="checkout" type="text" value="">
                % end
                % get_field_errors(form.checkout)
            </div>
        </div>
    <div class="row" style="margin-top:10px">
        <div class="form-group"> 
            <div class="col-sm-10">
                <button type="submit" class="btn btn-success">Save</button>
            </div>
        </div>
    </div>
    </form>
</body>
</html>