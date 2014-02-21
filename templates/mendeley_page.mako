
<%inherit file="project/addon/page.mako" />


% if user['can_edit']:

    % if not has_auth:

        <div class="alert alert-warning">
            This Mendeley add-on has not been authorized. To enable file uploads and deletion,
            browse to the <a href="${node['url']}settings/">settings</a> page and authorize this add-on.
        </div>

    % elif not has_access:

        <div class="alert alert-warning">
            Your Mendeley authorization does not have access to this library. To enable file uploads
            and deletion, authorize using a Mendeley account that has access to this library, or
            ask one of its owners to grant access to your Mendeley account.
        </div>

    % endif

% endif


<div class="row">

    <!-- Main Item Table -->

    <table class="table table-bordered table-striped" id="all-items-table">
        <tr>
            <td class="mendeley-item-table-view-row" colspan="3"></td>
        </tr>
        <tr>
            <td><input type="checkbox" name="select-all" id="select-all-checkbox">&nbsp;&nbsp;<strong>Title</strong></td>
             <td><strong>Publisher</strong></td>
             <td><strong>Type</strong></td>
        </tr>
       % for item in items:
         <tr>
            <td><input type="checkbox" name="select-all" id="select-all-checkbox">&nbsp;&nbsp;${item['title']}</td>
             <td>${item['publisher']}</td>
             <td>${item['type']}</td>
        </tr>
       % endfor


    </table>
</div>