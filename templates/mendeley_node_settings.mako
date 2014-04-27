<%inherit file="../../project/addon/node_settings.mako" />

<script type="text/javascript" src="/static/addons/mendeley/mendeley-node-cfg.js"></script>

% if node_has_auth:
      <input type="hidden" id="mendeleyUser" name="mendeley_user" value="${mendeley_user}}"/>
      <input type="hidden" id="mendeleyFolder" name="mendeleyFolder" value="${mendeley_folder}"/>

      <div class="well well-sm">
          Authorized by <a href="${auth_osf_url}}">${auth_osf_name}}</a>
          on behalf of Mendeley user <a target="_blank" href="${mendeley_user_url}">${mendeley_user_name}}</a>

          % if user_has_auth:
              <a id ="mendeleyRemoveToken" class="text-danger pull-right" style="cursor: pointer">Deauthorize</a>
          % endif
     </div>

    <div class="row">
        <div class="col-md-6">
            <select id="mendeleySelectFolder" class="form-control" ${'disabled' if not is_owner or is_registration else ''}>
                <option>----</option>
                %if is_owner:
                    %for folder_name in folder_names:
                    <option value="${folder_name}" ${'selected' if folder_name == mendeley_folder_full_name else ''}>${repo_name}</option>
                    %endfor
                % else:
                    <option selected>${mendeley_folder_full_name}</option>
                %endif

            </select>
        </div>
    </div>

 %elif user_has_auth:
    <a id="mendeleyImportToken" class="btn btn-primary">
        Authorize: Import Access Token from Profile
    </a>

 %else:
    <a id="mendeleyCreateToken" class="btn btn-primary">
        Authorize: Create Access Token
    </a>

% endif

<%def name="submit_btn()">
    % if node_has_auth:
        ${parent.submit_btn()}
    % endif
</%def>