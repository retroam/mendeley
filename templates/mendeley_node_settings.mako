<%inherit file="project/addon/settings.mako" />

<!-- Authorization -->
<div>
    <div class="alert alert-danger alert-dismissable">
    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
        Authorizing this Mendeley add-on will grant all contributors on this ${node['category']}
        permission to upload, modify, and delete files on the associated Mendeley library.
    </div>
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
        If one of your collaborators removes you from this ${node['category']},
        your authorization for Mendeley will automatically be revoked.
    </div>
    % if authorized_user_id:
        <a id="mendeleyDelKey" class="btn btn-danger">Unauthorize: Detach Access Token</a>
        <div style="padding-top: 10px">
            Authorized by OSF user
            <a href="${domain}/${authorized_user_id}" target="_blank">
                ${authorized_user_name}
            </a>
            on behalf of Mendeley user
            <a href="https://mendeley.com/${authorized_mendeley_user}" target="_blank">
                ${authorized_mendeley_user}
            </a>
        </div>
    % else:
        <div>

            Adding a Mendeley access token allows you and your collaborators to
            update and delete files on your linked library, and view its files
            if this library is private. If you do not add an access token, you
            will be able to view and download files within the library if it
            is public.
        </div>
        <br />
        <a id="mendeleyAddKey" class="btn btn-primary">
            % if user_has_authorization:
                Authorize: Import Access Token from Profile
            % else:
                Authorize: Create Access Token
            % endif
        </a>
    % endif
</div>

<br />

<%doc><div class="form-group">
    <label for="mendeleyUser">Collection</label>
    <input class="form-control" id="mendeleyUser" name="mendeley_user" value="${mendeley_user}" ${'disabled' if disabled else ''} />
</div></%doc>
<%doc><div class="form-group">
    <label for="mendeleyRepo">Mendeley Repo</label>
    <input class="form-control" id="mendeleyRepo" name="mendeley_repo" value="${mendeley_repo}" ${'disabled' if disabled else ''} />
</div></%doc>


<script type="text/javascript">

    $(document).ready(function() {

        $('#mendeleyAddKey').on('click', function() {
            % if authorized_user_id:
                $.ajax({
                    type: 'POST',
                    url: nodeApiUrl + 'mendeley/user_auth/',
                    contentType: 'application/json',
                    dataType: 'json',
                    success: function(response) {
                        window.location.reload();
                    }
                });
            % else:
                window.location.href = nodeApiUrl + 'mendeley/oauth/';
            % endif
        });

        $('#mendeleyDelKey').on('click', function() {
            bootbox.confirm(
                'Are you sure you want to detach your Mendeley access key? This will ' +
                    'revoke the ability to modify and upload files to Mendeley. If ' +
                    'the associated library is private, this will also disable viewing ' +
                    'and downloading files from Mendeley. This will not remove your ' +
                    'Mendeley authorization from your <a href="/settings/">user settings</a> ' +
                    'page.',
                function(result) {
                    if (result) {
                        $.ajax({
                            url: nodeApiUrl + 'mendeley/oauth/delete/',
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
