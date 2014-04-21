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



   <div class="container">

           <script>
            function getCitationURL(){
                return "${api_url}mendeley/getCitation/"
            }
            function getExportBaseURL(){
                return "${api_url}mendeley/getExport/"
            }
            </script>

<div class="row mendeley-options-top">

                <a href="${api_url}mendeley" type="button" class="btn btn-default"><span class="glyphicon glyphicon-home"></span>&nbsp; All Items</a>

                <form role="form" id="mendeleyCollectionForm" style="display: inline;">
                    <input type="hidden" id="mendeleyCollectionName" name="collection" value="">
                    <div class="btn-group">
                        <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                          <span class="glyphicon glyphicon-list"></span>&nbsp; Folders
                          <span class="caret"></span>
                        </button>
                        <ul class="dropdown-menu" role="menu">
                        % if len(folder_names) > 0:
                            % for name in folder_names:
                                <li onclick="$('#mendeleyCollectionName').val('${name}');$('#mendeleyCollectionForm').submit()">
                                    <a href="#">${name}</a>
                                </li>
                            % endfor
                        % else:
                            <li>
                                    <a href="#"><em>No Folders Found</em></a>
                                </li>

                        % endif
                        </ul>
                    </div>
                </form>

                <div class="btn-group">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                      <span class="glyphicon glyphicon-pencil"></span>&nbsp; Cite
                      <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu" role="menu">
                        % for style in citation_styles:
                            <li><a href="#" onclick="createCitation('${style}')">${style}</a></li>
                        % endfor
                    </ul>
                </div>

                <div class="btn-group">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                      <span class="glyphicon glyphicon-export"></span>&nbsp; Export
                      <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu" role="menu">
                        % for format in export_formats:
                            <li><a href="#" onclick="window.open(getExportURL('${format}'), '_blank')">${format}</a></li>
                        % endfor
                    </ul>
                </div>

             </div>

<div class="row">

    <!-- Main Item Table -->

    <table class="table table-bordered table-striped" id="all-items-table">
        <tr>
            <td class="mendeley-item-table-view-row" colspan="2"></td>
        </tr>
        <tr>
            <td><input type="checkbox" name="select-all" id="select-all-checkbox"></td>
             <td><strong>All Documents</strong></td>

        </tr>

       % for item in items:

         <tr>
            <td><input type="checkbox" name="${item['id']}"></td>
             <td>
                 <ul style="list-style: none;">
                    <li>
                        <a data-toggle="collapse" data-parent="#accordion" href=#${item['id']}>
                             ${item['title']}
                        </a>
                           <div id=${item['id']} class="panel-collapse collapse out">
                                <div class="panel-body">
                                     ${item['abstract']}
                                </div>
                           </div>

                    </li>
                    <li>${item['second_line']}</li>
                    <li>${item['third_line']}</li>
                    <li><a href="${item['url']}" target="_blank"> ${item['url']} </a></li>

                 </ul>
             </td>
        </tr>

       %endfor

    </table>
</div>




<!-- Display Citations Modal -->
<div class="modal fade" id="citationModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="citationModalTitle">Citation</h4>
      </div>
      <div class="modal-body" id="citationModalBody">

          Citation goes here

      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->

 </div>