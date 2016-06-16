% include renders
% renders_namespace = _ 
% get_field_errors = renders_namespace['get_field_errors']
% get_bootstrap = renders_namespace['get_bootstrap']

<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
% get_bootstrap()
<script src="/js/jquery.mask.min.js"></script>
<script type="text/javascript">
    $(document).ready(function () {
        $('#phone').mask('(000) 000-0000', {clearIfNotMatch: true, placeholder: "(XXX) XXX-XXXX"});
        $('#zip').mask('00000', {clearIfNotMatch: true, placeholder: "XXXXX"});
        $('.dependent-birthdate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
    });
</script>
<div class="container-fluid">
    % if form.errors or not captcha_success:
    <div class="page-header">
        <h3 class="text-danger">Correct The Errors Below!</h3>
    </div>
    % end
    %if not captcha_success:
    <span class="help-block">Did you check the "I'm not a robot" box?</span>
    % end
    <form id="thisForm" method="POST" action="{{post_url}}" role="form">
        <input id="state" name="state" type="hidden" value="Ohio">
    <div class="page-header">
        <h3>Volunteer Signup</h3>
    % volunteer = form.dependents[0]
    </div>
    <input type="hidden" id="dependents-0-isPrimary" name="dependents-0-isPrimary" value="True">
    <div class="form-horizontal">
        <div class="form-group 
        % if volunteer.firstName.errors:
        has-error
        % end
        ">
            <label for="dependents-0-firstName" class="col-sm-2 control-label">First Name</label>
            <div class="col-sm-10">
                <input autofocus class="form-control" id="dependents-0-firstName" name="dependents-0-firstName" type="text" value="{{volunteer.firstName.data}}">
                % get_field_errors(volunteer.firstName)
            </div>
        </div>
        <div class="form-group 
        % if volunteer.lastName.errors:
        has-error
        % end
        ">
            <label for="dependents-0-lastName" class="col-sm-2 control-label">Last Name</label>
            <div class="col-sm-10">
                <input class="form-control" id="dependents-0-lastName" name="dependents-0-lastName" type="text" value="{{volunteer.lastName.data}}">
                % get_field_errors(volunteer.lastName)
            </div>
        </div>
        <div class="form-group 
        % if volunteer.birthdate.errors:
        has-error
        % end
        ">
            <label for="dependents-0-birthdate" class="col-sm-2 control-label">Birthday</label>
            <div class="col-sm-10">
                % if volunteer.birthdate.data is not None and not volunteer.birthdate.errors:
                <input class="form-control dependent-birthdate" id="dependents-0-birthdate" name="dependents-0-birthdate" type="datetime" value="{{form.birthdate.data.strftime("%m/%d/%Y")}}">
                % else:
                <input class="form-control dependent-birthdate" id="dependents-0-birthdate" name="dependents-0-birthdate" type="datetime" value="">
                % end
                % get_field_errors(volunteer.birthdate)
            </div>
        </div>
    <div class="form-group ">
        <label for="address" class="col-sm-2 control-label">Street Address</label>
        <div class="col-sm-10">
            <input class="form-control" id="address" name="address" type="text" value="{{form.address.data}}">
        </div>
    </div>
    <div class="form-group 
        % if form.city.errors:
        has-error
        % end
        ">
        <label for="city" class="col-sm-2 control-label">City</label>
        <div class="col-sm-10">
            <input class="form-control" id="city" name="city" required type="text" value="{{form.city.data}}">
            % get_field_errors(form.city)
        </div>
    </div>
    <div class="form-group 
        % if form.zip.errors:
        has-error
        % end
        ">
        <label for="zip" class="col-sm-2 control-label">Zip</label>
        <div class="col-sm-10">
            <input class="form-control" id="zip" name="zip" required type="text" value="{{form.zip.data}}">
            % get_field_errors(form.zip)
        </div>
    </div>
    <div class="form-group ">
        <label for="email" class="col-sm-2 control-label">Email</label>
        <div class="col-sm-10">
            <input class="form-control" id="email" name="email" type="text" value="{{form.email.data}}">
        </div>
    </div>
    <div class="form-group ">
        <label for="phone" class="col-sm-2 control-label">Phone</label>
        <div class="col-sm-10">
            <input class="form-control" id="phone" name="phone" type="text" value="{{form.phone.data}}">
        </div>
    </div>
    <script src='https://www.google.com/recaptcha/api.js'></script>
    <div class="g-recaptcha" data-sitekey="6LeAoiITAAAAANQ064h05TWYQJJZbAdv2iTca2TC"></div>
    <div class="row" style="margin-top:10px">
        <div class="form-group"> 
            <div class="col-sm-10">
                <button type="submit" class="btn btn-default">Register</button>
            </div>
        </div>
    </div>
    </form>
</div>
</body>
</html>
