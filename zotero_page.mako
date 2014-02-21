<%inherit file="project/addon/page.mako" />


<!-- BEGIN ADDON TEMPLATE -->

% if error_statement:

    <div class="alert alert-danger"><strong>Error</strong> ${error_statement} </div>

% else:

    <div class="container">

            <script>
            function getCitationURL(){
                return "${url}zotero/citation/"
            }
            function getExportBaseURL(){
                return "${url}zotero/export/"
            }
            </script>

            <div class="row zotero-options-top">

                <a href="${url}zotero/" type="button" class="btn btn-default"><span class="glyphicon glyphicon-home"></span>&nbsp; All Items</a>

                <form role="form" id="zoteroCollectionForm" style="display: inline;">
                    <input type="hidden" id="zoteroCollectionName" name="collection" value="">
                    <div class="btn-group">
                        <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                          <span class="glyphicon glyphicon-list"></span>&nbsp; Collections
                          <span class="caret"></span>
                        </button>
                        <ul class="dropdown-menu" role="menu">
                        % if len(collection_names) > 0:
                            % for name in collection_names:
                                <li onclick="$('#zoteroCollectionName').val('${name}');$('#zoteroCollectionForm').submit()">
                                    <a href="#">${name}</a>
                                </li>
                            % endfor
                        % else:
                            <li>
                                    <a href="#"><em>No Collections Found</em></a>
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

   ##             <a href="#" type="button" class="btn btn-default" onclick="exportItems()"><span class="glyphicon glyphicon-export"></span>&nbsp; Export</a>

             </div>

            <div class="row">

                <!-- Main Item Table -->

                <table class="table table-bordered table-striped" id="all-items-table">
                    <tr>
                        <td class="zoltero-item-table-view-row" colspan="3"><strong>${view_string}<strong></td>
                    </tr>
                    <tr>
                        <td><input type="checkbox" name="select-all" id="select-all-checkbox">&nbsp;&nbsp;<strong>Name</strong></td>
                         <td><strong>Creator</strong></td>
                         <td><strong>Date Modified</strong></td>
                    </tr>
                % for item in items:
                    <tr>
                        <td><input type="checkbox" name="${item['key']}">&nbsp;&nbsp;${item['title']} </td>
                        <td> ${item['creator']} </td>
                        <td> ${item['date']} </td>
                     </tr>
                % endfor

                </table>
            </div>

            <!-- Display Citations Modal -->
            <div class="modal fade" id="citationModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title" id="citationModalTitle"></h4>
                  </div>
                  <div class="modal-body" id="citationModalBody">

                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                  </div>
                </div><!-- /.modal-content -->
              </div><!-- /.modal-dialog -->
            </div><!-- /.modal -->

        </div>
    </div>
    </div>


% endif ## if error_statement

