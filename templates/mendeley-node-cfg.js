var MendeleyConfigHelper = (function(){

    var updateHidden = function(val){
        var folderParts = val.split('/');
        $('#mendeleyUser').val($.trim(folderParts[0]));
        $('#mendeleyFolder').val($.trim(folderParts[1]));

    };

    $(document).ready(function(){
        $('#mendeleySelectFolder').on('change', function(){
            var value = $(this).val();
            if (value) {
                updateHidden(value);
            }
        });

        $('#mendeleyImportToken').on('click', function(){
            $.ajax({
                type: 'POST',
                url: nodeApiUrl + 'mendeley/user_auth',
                contentType: 'application/json',
                dataType: 'json',
                success: function(response){
                    window.location.reload();
                }
            });
        });

        $('#mendeleyCreateToken').on('click', function(){
            window.location.href = nodeApiUrl + 'mendeley/oauth/';
        });

        $('mendeleyRemoveToken').on('click', function(){
            bootbox.confirm('Are you sure you want to remove this Mendeley authorization?', function(confirm){
                if (confirm){
                    $.ajax({
                        type: 'DELETE',
                        url: nodeApiUrl + 'mendeley/oauth/',
                        success: function(response){
                            window.location.reload();
                        }
                    });
                }
            });
        });

        $('#addonSettingsMendeley .addon-settings-submit').on('click', function(){
            if (!$('#mendeleyFolder').val()){
                return false;
            }
        });
    });
});