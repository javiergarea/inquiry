bootstrap_alert = function() {}
bootstrap_alert.warning = function(message) {
    $('#alert_placeholder').html('<div class="alert col-6 w-25"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
}

function submitform() {
    if ( document.getElementById("id_title").value != ''  || 
         document.getElementById("id_authors").value != '' ||
         document.getElementById("id_abstract").value != '' || 
         document.getElementById("id_content").value != ''){
            return (true);
        }
    bootstrap_alert.warning('You must enter at least one field!')
    return (false);
}