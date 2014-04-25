<%inherit file="project/addon/user_settings.mako" />

<!-- Authorization -->
<div>
    % if authorized:
        <a id="mendeleyDelKey" class="btn btn-danger">Delete Access Token</a>
        <div style="padding-top: 10px;">
            Authorized by Mendeley user
            <a href="https://mendeley.com/profiles/${authorized_mendeley_user}" target="_blank">
                ${authorized_mendeley_user}
            </a>
        </div>
    % else:
        <a id="mendeleyAddKey" class="btn btn-primary">
            Create Access Token
        </a>
    % endif
</div>

<script type="text/javascript">

    $(document).ready(function() {

        $('#mendeleyAddKey').on('click', function() {
            % if authorized_user_id:
                $.ajax({
                    type: 'POST',
                    url: '/api/v1/profile/settings/oauth/',
                    contentType: 'application/json',
                    dataType: 'json',
                    success: function(response) {
                        window.location.reload();
                    }
                });
            % else:
                window.location.href = '/api/v1/settings/mendeley/oauth/';
            % endif
        });

        $('#mendeleyDelKey').on('click', function() {
            bootbox.confirm(
                             'Are you sure you want to delete your Mendeley access key? This will ' +
                             'revoke access to Mendeley for all projects you have authorized ' +
                             'and delete your acess token from Mendeley. Your OSF collaborators ' +
                             'will not be able to read your library that you have authorized',
                function(result) {
                    if (result) {
                        $.ajax({
                            url: '/api/v1/settings/mendeley/oauth/delete/',
                            type: 'POST',
                            contentType: 'application/json',
                            dataType: 'json',
                            success: function() {
                                window.location.reload();
                            }
                        });
                    }
                }
            )
        });
    });

</script>

<%def name="submit_btn()"></%def>
<%def name="on_submit()"></%def>